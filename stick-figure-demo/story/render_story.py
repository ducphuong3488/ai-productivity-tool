"""Stick-figure remake of the reel "Nhà toàn người sai thì hạnh phúc,
nhà toàn người đúng thì tan vỡ" (~100s, 1080x1920, 30fps).

Visuals are drawn frame by frame with Pillow and synced to the voice track
via timing.json (made by align.py). Captions pop in word by word as they are
spoken; the current word is highlighted and keywords get a gold gradient
with glow.

Usage: python3 render_story.py voice.wav out.mp4 [--frames t1,t2,...]
"""
import json, math, os, subprocess, sys
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, SS = 1080, 1920, 30, 2
HERE = os.path.dirname(os.path.abspath(__file__))
BIG = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
BOLD = "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf"
SEMI = "/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf"
INK = (34, 30, 48)
GROUND = 1250
PHRASES = json.load(open(os.path.join(HERE, "timing.json")))
WORDS = [w for p in PHRASES for w in p]

_fonts = {}
def font(path, size):
    key = (path, int(size))
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, max(1, int(size)))
    return _fonts[key]

def clamp(x, a=0.0, b=1.0):
    return min(max(x, a), b)

def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)

def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3

def back_out(x):
    x = clamp(x)
    return 1 + 2.9 * (x - 1) ** 3 + 1.9 * (x - 1) ** 2

def window(t, a, b, fade=0.2):
    """1 inside [a, b], easing in/out over `fade` seconds."""
    return smooth((t - a) / fade) * smooth((b - t) / fade)

def speaking(t, a, b):
    """Mouth-flap amount while a word in [a, b] is being spoken."""
    for w in WORDS:
        if a <= w["s"] <= b and w["s"] <= t <= w["e"] + 0.05:
            return 0.35 + 0.65 * abs(math.sin(t * 17))
    return 0.0

def mix(c1, c2, k):
    return tuple(int(a + (b - a) * k) for a, b in zip(c1, c2))

# ---------------------------------------------------------------- canvas (supersampled)
class Canvas:
    def __init__(self, img):
        self.img = img
        self.d = ImageDraw.Draw(img)

    def line(self, pts, fill, width, round_caps=True):
        p = [(x * SS, y * SS) for x, y in pts]
        w = int(width * SS)
        self.d.line(p, fill=fill, width=w, joint="curve")
        if round_caps:
            for x, y in (p[0], p[-1]):
                self.d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=fill)

    def circle(self, cx, cy, r, fill=None, outline=None, width=0):
        self.d.ellipse([(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS],
                       fill=fill, outline=outline, width=int(width * SS))

    def ellipse(self, box, fill=None, outline=None, width=0):
        self.d.ellipse([v * SS for v in box], fill=fill, outline=outline, width=int(width * SS))

    def poly(self, pts, fill, outline=None, width=0):
        self.d.polygon([(x * SS, y * SS) for x, y in pts], fill=fill, outline=outline, width=int(width * SS))

    def rect(self, box, fill):
        self.d.rectangle([v * SS for v in box], fill=fill)

    def rrect(self, box, r, fill=None, outline=None, width=0):
        self.d.rounded_rectangle([v * SS for v in box], radius=int(r * SS), fill=fill, outline=outline,
                                 width=int(width * SS))

    def arc(self, box, a0, a1, fill, width):
        self.d.arc([v * SS for v in box], a0, a1, fill=fill, width=int(width * SS))

    def chord(self, box, a0, a1, fill):
        self.d.chord([v * SS for v in box], a0, a1, fill=fill)

    def text(self, xy, s, path, size, fill, anchor="mm", stroke=0, stroke_fill=None):
        self.d.text((xy[0] * SS, xy[1] * SS), s, font=font(path, size * SS), fill=fill, anchor=anchor,
                    stroke_width=int(stroke * SS), stroke_fill=stroke_fill)

def rot(pts, cx, cy, a):
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]

# ---------------------------------------------------------------- characters
# pose = [x, dy, lean, lthigh, lknee, rthigh, rknee, larm, lelbow, rarm, relbow]
# angles: 0 = straight down, positive = toward the way the figure faces.
def P(x, dy=0.0, lean=0.0, legs=(9, 4, -9, 4), la=-12, le=8, ra=12, re=8):
    return np.array([x, dy, lean, *legs, la, le, ra, re], float)

def idle(t, x, **kw):
    return P(x, dy=3 * math.sin(t * 5), **kw)

def walk_cycle(t, x, speed=1.0, run=False):
    p = t * 2 * math.pi * (1.7 if run else 1.25) * speed
    s, c = math.sin(p), math.cos(p)
    amp, knee, arm = (38, 55, 45) if run else (24, 32, 26)
    return P(x, dy=-abs(s) * (14 if run else 6), lean=12 if run else 3,
             legs=(amp * s, 10 + knee * max(0, -c), -amp * s, 10 + knee * max(0, c)),
             la=-arm * s, le=70 if run else 15, ra=arm * s, re=70 if run else 15)

def move(t, x0, x1, t0, t1, run=False):
    """Walk from x0 to x1 between t0 and t1; returns (pose, facing)."""
    face = 1 if x1 >= x0 else -1
    if t <= t0:
        return idle(t, x0), face
    if t >= t1:
        return idle(t, x1), face
    k = (t - t0) / (t1 - t0)
    x = x0 + (x1 - x0) * (0.5 - 0.5 * math.cos(k * math.pi) if not run else ease_out(k) * 0.3 + k * 0.7)
    return walk_cycle(t, x, run=run), face

def sit(t, x, **kw):
    return P(x, dy=56 + 2 * math.sin(t * 4), lean=-3, legs=(60, 60, 55, 55), **kw)

def blend(a, b, k):
    k = smooth(k)
    return a * (1 - k) + b * k

GESTURES = {
    "rest": dict(la=-12, le=8, ra=12, re=8),
    "akimbo": dict(la=-40, le=95, ra=40, re=-95),
    "point": dict(la=-15, le=10, ra=95, re=-5),
    "bow": dict(la=30, le=20, ra=35, re=15),
    "chest": dict(la=-12, le=8, ra=30, re=-160),
    "touch": dict(la=-12, le=8, ra=100, re=-15),
    "drink": dict(la=-12, le=8, ra=120, re=-235),
    "scratch": dict(la=-12, le=8, ra=150, re=-300),
    "cry": dict(la=115, le=-230, ra=125, re=-240),
    "hands": dict(la=-48, le=0, ra=48, re=0),
    "open": dict(la=-55, le=-30, ra=65, re=-40),
    "up": dict(la=-150, le=-15, ra=150, re=15),
    "place": dict(la=-12, le=8, ra=60, re=10),
}

def gesture(p, name, t=0.0, wiggle=0.0):
    g = GESTURES[name]
    q = p.copy()
    q[7], q[8], q[9], q[10] = g["la"], g["le"], g["ra"], g["re"]
    if wiggle:
        q[9] += wiggle * math.sin(t * 9)
        q[7] -= wiggle * 0.6 * math.sin(t * 7 + 1)
    return q

def mix_gesture(p, a, b, k, t=0.0):
    return blend(gesture(p, a, t), gesture(p, b, t), k)

HUSBAND = dict(k=1.0, hair="short", tie=(60, 120, 235))
FRIEND = dict(k=1.0, cap=(60, 170, 95))
WIFE = dict(k=0.93, hair="long", dress=(240, 110, 150))
SON = dict(k=0.62, hair="tuft", shirt=(255, 150, 40))

def draw_person(c, pose, ch, facing=1, face="happy", talk=0.0, t=0.0, ground=GROUND, ink=INK):
    k = ch["k"]
    hx, hdy, lean, lt, lk, rt, rk, la, le, ra, re = pose
    T, S_, TO, N, HD, U, F = 135 * k, 135 * k, 230 * k, 25 * k, 58 * k, 115 * k, 105 * k

    def vec(o, ang, length):
        r = math.radians(ang)
        return (o[0] + facing * math.sin(r) * length, o[1] + math.cos(r) * length)

    hip = (hx, ground - (T + S_ - 12 * k) + hdy * k)
    sh = vec(hip, 180 - lean, TO)
    neck = vec(sh, 180 - lean, N)
    head = vec(neck, 180 - lean, HD)
    lw = 16 * k
    if ch.get("hair") == "long":  # hair behind the head
        c.poly([(head[0] - 62 * k, head[1] - 10 * k), (head[0] + 62 * k, head[1] - 10 * k),
                (head[0] + 58 * k, head[1] + 120 * k),
                (head[0] - 58 * k, head[1] + 120 * k)], fill=(70, 45, 40))
    joints = {}
    for side, (th, kn) in (("l", (lt, lk)), ("r", (rt, rk))):
        knee = vec(hip, th, T)
        foot = vec(knee, th - kn, S_)
        foot = (foot[0], min(foot[1], ground))
        c.line([hip, knee, foot], ink, lw)
        joints[side + "foot"] = foot
    c.line([hip, neck], ink, lw)
    if ch.get("dress"):
        top = vec(hip, 180 - lean, TO * 0.75)
        c.poly([(top[0] - 22 * k, top[1]), (top[0] + 22 * k, top[1]),
                (hip[0] + 62 * k, hip[1] + 75 * k), (hip[0] - 62 * k, hip[1] + 75 * k)], fill=ch["dress"])
    if ch.get("shirt"):
        c.line([vec(hip, 180 - lean, 10 * k), vec(hip, 180 - lean, TO - 10 * k)], ch["shirt"], 44 * k)
    if ch.get("tie"):
        a = vec(neck, 180 - lean, -8 * k)
        c.poly([(a[0] - 9 * k, a[1]), (a[0] + 9 * k, a[1]), (a[0] + 12 * k, a[1] + 70 * k),
                (a[0], a[1] + 88 * k), (a[0] - 12 * k, a[1] + 70 * k)], fill=ch["tie"])
    for side, (ar, el) in (("l", (la, le)), ("r", (ra, re))):
        elbow = vec(sh, ar, U)
        hand = vec(elbow, ar + el, F)
        c.line([sh, elbow, hand], ink, lw)
        joints[side + "hand"] = hand
    cx, cy, r = head[0], head[1], HD
    c.circle(cx, cy, r, fill=(255, 255, 255), outline=ink, width=lw)
    # hair / hats
    if ch.get("hair") == "short":
        c.chord([cx - r, cy - r, cx + r, cy + 0.1 * r], 180, 360, fill=(60, 45, 40))
        c.circle(cx, cy, r, outline=ink, width=lw)
    elif ch.get("hair") == "long":
        c.chord([cx - r - 2, cy - r - 4, cx + r + 2, cy + r * 0.15], 180, 360, fill=(70, 45, 40))
        c.circle(cx, cy, r, outline=ink, width=lw)
    elif ch.get("hair") == "tuft":
        for dx in (-14, 0, 14):
            c.line([(cx + dx * k, cy - r), (cx + dx * k * 1.8, cy - r - 26 * k)], ink, 9 * k)
    if ch.get("cap"):
        c.chord([cx - r - 2, cy - r - 6, cx + r + 2, cy + r * 0.15], 180, 360, fill=ch["cap"])
        bx = cx + facing * r * 0.4
        c.rrect([min(bx, bx + facing * 70 * k), cy - 30 * k, max(bx, bx + facing * 70 * k), cy - 18 * k], 6 * k,
                fill=mix(ch["cap"], (0, 0, 0), 0.25))
        c.circle(cx, cy, r, outline=ink, width=lw)
    # face
    fx = facing * 14 * k
    ey = cy - 8 * k
    eyes = [(cx + fx - 16 * k, ey), (cx + fx + 18 * k, ey)]
    er = 7 * k
    if face == "cry":
        for ex, eyy in eyes:
            c.arc([ex - 10 * k, eyy - 6 * k, ex + 10 * k, eyy + 10 * k], 200, 340, ink, 5 * k)
            for i in range(2):  # falling tears
                ph = (t * 1.8 + i * 0.5) % 1
                c.ellipse([ex - 5 * k, eyy + (10 + ph * 70) * k, ex + 5 * k, eyy + (24 + ph * 70) * k],
                          fill=(90, 170, 255))
    else:
        big = 1.5 if face == "surprised" else 1.0
        for ex, eyy in eyes:
            c.circle(ex, eyy, er * big, fill=ink)
    if face == "angry":
        for i, (ex, eyy) in enumerate(eyes):
            s = 1 if i == 0 else -1
            c.line([(ex - 13 * k, eyy - 24 * k + s * 7 * k), (ex + 13 * k, eyy - 24 * k - s * 7 * k)], ink, 6 * k)
    if face in ("sad", "cry"):
        for i, (ex, eyy) in enumerate(eyes):
            s = 1 if i == 0 else -1
            c.line([(ex - 12 * k, eyy - 20 * k - s * 6 * k), (ex + 12 * k, eyy - 20 * k + s * 6 * k)], ink, 5 * k)
    mx, my = cx + fx, cy + 22 * k
    if talk > 0.15 or face in ("cry", "surprised"):
        o = max(talk, 0.9 if face == "cry" else 0.6 if face == "surprised" else 0)
        c.ellipse([mx - 13 * k, my - (4 + 10 * o) * k, mx + 13 * k, my + (4 + 10 * o) * k], fill=(120, 40, 50))
    elif face in ("sad", "angry"):
        c.arc([mx - 18 * k, my - 2 * k, mx + 18 * k, my + 24 * k], 200, 340, ink, 6 * k)
    else:
        c.arc([mx - 20 * k, my - 22 * k, mx + 20 * k, my + 8 * k], 25, 155, ink, 6 * k)
    if face in ("happy", "sad") and talk <= 0.15:  # blush
        c.ellipse([cx + fx - 40 * k, cy + 6 * k, cx + fx - 24 * k, cy + 14 * k], fill=(255, 180, 185))
        c.ellipse([cx + fx + 30 * k, cy + 6 * k, cx + fx + 46 * k, cy + 14 * k], fill=(255, 180, 185))
    joints["head"] = head
    joints["r"] = r
    return joints

def shadow(c, x, k=1.0, ground=GROUND, air=0.0):
    sw = (95 - 40 * air) * k
    c.ellipse([x - sw, ground - 10 * k, x + sw, ground + 10 * k], fill=(0, 0, 0, 40))

# ---------------------------------------------------------------- props & effects
def heart(c, cx, cy, s, fill):
    pts = []
    for i in range(40):
        a = i / 40 * 2 * math.pi
        x = 16 * math.sin(a) ** 3
        y = -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
        pts.append((cx + x * s / 16, cy + y * s / 16))
    c.poly(pts, fill=fill)

def floating_hearts(c, t, x0, y0, spread=200, n=6, t0=0.0, color=(255, 90, 120)):
    if t < t0:
        return
    for i in range(n):
        ph = ((t - t0) * 0.45 + i / n) % 1
        x = x0 + (i / max(1, n - 1) - 0.5) * spread + 20 * math.sin(t * 2 + i)
        y = y0 - ph * 320
        a = math.sin(ph * math.pi)
        heart(c, x, y, 16 + 12 * a, mix((255, 255, 255), color, a))

def star_burst(c, cx, cy, r, fill, n=12, inner=0.55, rot_=0.0):
    pts = []
    for i in range(n * 2):
        a = rot_ + i * math.pi / n
        rr = r if i % 2 == 0 else r * inner
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    c.poly(pts, fill=fill)

def comic(c, t, t0, cx, cy, word, color=(255, 210, 40), dur=0.9):
    lt = t - t0
    if not 0 <= lt <= dur:
        return
    s = back_out(lt / 0.25) * smooth((dur - lt) / 0.2)
    star_burst(c, cx, cy, 150 * s, color, rot_=0.2)
    star_burst(c, cx, cy, 115 * s, (255, 255, 255), rot_=0.2 + 0.26)
    c.text((cx, cy), word, BIG, 62 * s, (230, 50, 60), stroke=5 * s, stroke_fill=(255, 255, 255))

def bubble(c, t, t0, t1, head, r, text=None, icon=None, side=1, width=380, color=(255, 255, 255)):
    """Speech bubble above-beside a head. side=+1 puts it to the right."""
    a = window(t, t0, t1, 0.18)
    if a <= 0.01:
        return
    s = back_out(clamp((t - t0) / 0.3)) if t < t0 + 0.3 else 1.0
    s *= 0.85 + 0.15 * a
    lines = []
    if text:
        f = font(BOLD, 44)
        cur = ""
        for w in text.split():
            nxt = (cur + " " + w).strip()
            if f.getlength(nxt) > width - 60 and cur:
                lines.append(cur)
                cur = w
            else:
                cur = nxt
        lines.append(cur)
    bw = width * s
    bh = ((len(lines) * 56 + 44) if text else 150) * s
    bx = head[0] + side * (r + 30) - (bw if side < 0 else 0)
    by = head[1] - r - 60 - bh
    bx = clamp(bx, 24, W - 24 - bw)
    tip = (head[0] + side * r * 0.6, head[1] - r - 6)
    base_x = clamp(tip[0] + side * 50, bx + 30, bx + bw - 30)
    c.poly([(base_x - 22, by + bh - 4), (base_x + 22, by + bh - 4), tip], fill=INK)
    c.rrect([bx - 5, by - 5, bx + bw + 5, by + bh + 5], 34 * s + 5, fill=INK)
    c.rrect([bx, by, bx + bw, by + bh], 34 * s, fill=color)
    c.poly([(base_x - 15, by + bh - 6), (base_x + 15, by + bh - 6), (tip[0] - side * 4, tip[1] - 10)], fill=color)
    cx, cy = bx + bw / 2, by + bh / 2
    if text:
        for i, ln in enumerate(lines):
            c.text((cx, cy + (i - (len(lines) - 1) / 2) * 56 * s), ln, BOLD, 44 * s, INK)
    if icon:
        icon(c, cx, cy, s, t)

def icon_question(c, x, y, s, t):
    c.text((x, y + 4 * math.sin(t * 6)), "?", BIG, 110 * s, (60, 120, 235))

def icon_home_heart(c, x, y, s, t):
    house(c, x - 50 * s, y + 52 * s, 90 * s, (255, 214, 160), (220, 90, 70), lit=True)
    heart(c, x + 60 * s, y - 10 * s + 5 * math.sin(t * 5), 34 * s, (255, 80, 110))

def icon_storm(c, x, y, s, t):
    cloud(c, x, y - 10 * s, 0.55 * s, (130, 135, 150))
    if int(t * 6) % 2 == 0:
        bolt(c, x, y + 20 * s, 0.6 * s)

def icon_cup(c, x, y, s, t):
    cup(c, x, y, 1.6 * s)

def house(c, x, base, w, wall, roof, lit=False):
    h = w * 0.75
    c.rect([x - w / 2, base - h, x + w / 2, base], wall)
    c.poly([(x - w * 0.62, base - h), (x + w * 0.62, base - h), (x, base - h - w * 0.55)], fill=roof)
    win = (255, 225, 110) if lit else (80, 90, 110)
    ws = w * 0.18
    for dx in (-0.27, 0.27):
        c.rect([x + dx * w - ws / 2, base - h * 0.75, x + dx * w + ws / 2, base - h * 0.75 + ws], win)
    c.rect([x - w * 0.1, base - h * 0.45, x + w * 0.1, base], mix(roof, (0, 0, 0), 0.25))

def cloud(c, x, y, s, fill):
    for dx, dy, r in ((-70, 10, 55), (0, -20, 75), (75, 5, 60), (30, 25, 55), (-30, 28, 50)):
        c.circle(x + dx * s, y + dy * s, r * s, fill=fill)

def bolt(c, x, y, s, fill=(255, 220, 60)):
    pts = [(0, 0), (40, 0), (15, 60), (50, 60), (-20, 160), (5, 85), (-30, 85)]
    c.poly([(x + (px - 10) * s, y + py * s) for px, py in pts], fill=fill)

def cup(c, x, y, s=1.0, angle=0.0, water=True):
    """Glass with bottom-center at (x, y)."""
    body = [(-17, -44), (17, -44), (13, 0), (-13, 0)]
    c.poly(rot([(px * s, py * s) for px, py in body], x, y, angle), fill=(215, 235, 255), outline=(90, 130, 190),
           width=3 * s)
    if water:
        wv = [(-15, -26), (15, -26), (12.5, -3), (-12.5, -3)]
        c.poly(rot([(px * s, py * s) for px, py in wv], x, y, angle), fill=(120, 185, 255))

SHARDS = [(np.random.default_rng(i).uniform(-1, 1), np.random.default_rng(i + 50).uniform(0.4, 1.0),
           np.random.default_rng(i + 99).uniform(0, 6.28)) for i in range(11)]
def shards(c, t, t0, x, y=GROUND):
    lt = t - t0
    if lt < 0:
        return
    for i, (dirx, sp, a0) in enumerate(SHARDS):
        k = ease_out(lt / 0.45)
        px = x + dirx * 170 * sp * k
        py = y - 4 - math.sin(min(1, lt / 0.45) * math.pi) * 70 * sp
        a = a0 + k * 4 * dirx
        tri = [(0, -14), (11, 8), (-9, 10)]
        c.poly(rot([(u * (0.6 + sp), v * (0.6 + sp)) for u, v in tri], px, py, a), fill=(200, 230, 255),
               outline=(90, 130, 190), width=2)
    if lt < 0.6:  # water splash
        for i in range(8):
            a = math.pi + i / 7 * math.pi
            rr = 30 + lt * 300
            c.circle(x + math.cos(a) * rr, y + math.sin(a) * rr * 0.5, 9 * (1 - lt / 0.6), fill=(120, 185, 255))

def steam(c, t, head, r):
    for i in range(3):
        ph = (t * 1.6 + i / 3) % 1
        x = head[0] + (i - 1) * 40
        y = head[1] - r - 20 - ph * 110
        c.circle(x + 8 * math.sin(ph * 9), y, 14 + 20 * ph, fill=mix((255, 120, 120), (255, 235, 235), ph))

def rays(c, cx, cy, t, color, n=14, r=900):
    for i in range(n):
        a = t * 0.15 + i * 2 * math.pi / n
        c.poly([(cx, cy), (cx + math.cos(a - 0.09) * r, cy + math.sin(a - 0.09) * r),
                (cx + math.cos(a + 0.09) * r, cy + math.sin(a + 0.09) * r)], fill=color)

# ---------------------------------------------------------------- backgrounds
def grad_img(w, h, top, bottom):
    g = np.linspace(0, 1, h)[:, None]
    col = (np.array(top) * (1 - g) + np.array(bottom) * g).astype(np.uint8)
    return Image.fromarray(np.repeat(col[:, None, :], w, axis=1), "RGB")

def sky_ground(sky_top, sky_bot, g_top, g_bot):
    img = Image.new("RGB", (W * SS, H * SS))
    img.paste(grad_img(W * SS, GROUND * SS, sky_top, sky_bot), (0, 0))
    img.paste(grad_img(W * SS, (H - GROUND) * SS, g_top, g_bot), (0, GROUND * SS))
    return img

def bg_houses():
    img = sky_ground((170, 215, 255), (255, 232, 210), (140, 205, 125), (70, 120, 80))
    c = Canvas(img)
    for x, y, s in ((180, 300, 0.8), (820, 230, 1.0), (560, 420, 0.6)):
        cloud(c, x, y, s, (255, 255, 255))
    c.ellipse([-200, GROUND - 90, 700, GROUND + 90], fill=(120, 190, 110))
    c.ellipse([400, GROUND - 70, 1300, GROUND + 90], fill=(110, 180, 105))
    house(c, 280, GROUND + 10, 380, (255, 214, 160), (220, 90, 70), lit=True)
    house(c, 800, GROUND + 10, 380, (185, 188, 200), (110, 112, 130))
    return img

def bg_park():
    img = sky_ground((160, 210, 255), (230, 245, 255), (150, 210, 130), (80, 140, 90))
    c = Canvas(img)
    c.circle(880, 260, 80, fill=(255, 225, 120))
    for x, y, s in ((200, 240, 0.9), (620, 330, 0.7)):
        cloud(c, x, y, s, (255, 255, 255))
    c.ellipse([-300, GROUND - 260, 600, GROUND + 200], fill=(130, 195, 120))
    c.ellipse([350, GROUND - 200, 1400, GROUND + 200], fill=(120, 185, 115))
    for x, s in ((120, 1.0), (980, 1.2)):
        c.rect([x - 18 * s, GROUND - 260 * s, x + 18 * s, GROUND], (130, 90, 60))
        for dx, dy, r in ((0, -330, 120), (-80, -260, 90), (80, -260, 90)):
            c.circle(x + dx * s, GROUND + dy * s, r * s, fill=(70, 160, 90))
    c.ellipse([60, GROUND - 25, 1020, GROUND + 60], fill=(225, 205, 165))
    # bench
    wood, dark = (190, 120, 70), (120, 75, 45)
    for x in (300, 780):
        c.rect([x - 10, 1056, x + 10, GROUND], dark)
    for y in (880, 940):
        c.rrect([270, y, 810, y + 28], 8, fill=wood)
    for x in (320, 760):
        c.rect([x - 8, 880, x + 8, 1060], dark)
    c.rrect([260, 1050, 820, 1082], 8, fill=wood)
    return img

def bg_home(cold=False):
    wall = ((240, 230, 222), (215, 218, 232)) if not cold else ((150, 156, 175), (118, 122, 140))
    floor = ((210, 160, 115), (160, 110, 75)) if not cold else ((110, 100, 100), (70, 64, 70))
    img = sky_ground(wall[0], wall[1], floor[0], floor[1])
    c = Canvas(img)
    c.rect([0, GROUND - 14, W, GROUND], mix(floor[0], (0, 0, 0), 0.3))
    for y in range(GROUND + 70, H, 110):
        c.rect([0, y, W, y + 4], mix(floor[0], (0, 0, 0), 0.18))
    # window
    sky = ((150, 210, 255), (230, 245, 255)) if not cold else ((60, 66, 84), (95, 100, 118))
    c.rrect([90, 360, 470, 780], 16, fill=(250, 250, 250) if not cold else (170, 172, 185))
    img.paste(grad_img(340 * SS, 380 * SS, sky[0], sky[1]), (110 * SS, 380 * SS))
    c.rect([276, 380, 284, 760], (250, 250, 250) if not cold else (170, 172, 185))
    c.rect([110, 566, 450, 574], (250, 250, 250) if not cold else (170, 172, 185))
    if not cold:
        c.circle(380, 470, 40, fill=(255, 225, 120))
    else:
        cloud(Canvas(img), 280, 470, 0.7, (80, 84, 100))
    # shelf (kệ) with plates
    c.rect([700, 700, 1010, 716], (150, 100, 65) if not cold else (90, 80, 80))
    for x, col in ((750, (120, 180, 230)), (820, (240, 140, 120)), (930, (255, 255, 255))):
        c.ellipse([x - 32, 640, x + 32, 702], fill=col if not cold else mix(col, (110, 110, 120), 0.6))
    # plant
    if not cold:
        c.rrect([560, 690, 620, 760], 10, fill=(230, 120, 90))
        for a in (-0.6, -0.2, 0.2, 0.6):
            c.line([(590, 690), (590 + math.sin(a) * 80, 690 - math.cos(a) * 90)], (80, 160, 90), 14)
    # table
    top = (180, 120, 75) if not cold else (100, 85, 80)
    c.rrect([630, 1000, 1010, 1028], 8, fill=top)
    for x in (660, 980):
        c.rect([x - 10, 1028, x + 10, GROUND], mix(top, (0, 0, 0), 0.3))
    return img

def bg_lesson():
    return sky_ground((255, 190, 150), (255, 235, 200), (150, 205, 125), (80, 130, 90))

def bg_end():
    y, x = np.mgrid[0:H * SS, 0:W * SS].astype(np.float32) / SS
    d = np.sqrt(((x - W / 2) / W) ** 2 + ((y - 820) / H) ** 2)
    g = np.clip(1 - d * 2.0, 0, 1)[..., None]
    base = np.array([10, 12, 30]) * (1 - g) + np.array([70, 40, 80]) * g
    return Image.fromarray(base.astype(np.uint8), "RGB")

_bgs = {}
def background(key):
    if key not in _bgs:
        _bgs[key] = {"houses": bg_houses, "park": bg_park, "home_good": bg_home, "home_bad": lambda: bg_home(True),
                     "lesson": bg_lesson, "end": bg_end}[key]()
    return _bgs[key].copy()

# ---------------------------------------------------------------- scenes
def scene_houses(c, t):
    k = back_out((t - 0.7) / 0.35)
    floating_hearts(c, t, 280, 900, spread=260, t0=0.9)
    if k > 0:
        c.rrect([280 - 150 * k, 1290, 280 + 150 * k, 1290 + 80 * k], 40 * k, fill=(255, 255, 255))
        c.text((280, 1290 + 40 * k), "NGƯỜI SAI", BIG, 40 * k, (60, 160, 90))
    k = back_out((t - 2.6) / 0.35)
    if k > 0:
        c.rrect([800 - 160 * k, 1290, 800 + 160 * k, 1290 + 80 * k], 40 * k, fill=(255, 255, 255))
        c.text((800, 1290 + 40 * k), "NGƯỜI ĐÚNG", BIG, 40 * k, (220, 60, 70))
    if t > 2.5:
        cloud(c, 800, 640 + 6 * math.sin(t * 3), 1.0, (120, 124, 140))
        if 3.5 < t < 3.7 or 4.0 < t < 4.15:
            bolt(c, 790, 700, 1.0)
    p = smooth((t - 3.5) / 0.6)
    if p > 0:  # crack through the "right" house
        pts = [(800, 760), (780, 860), (825, 930), (790, 1030), (830, 1120), (805, 1260)]
        n = 1 + p * (len(pts) - 1)
        seg = pts[:int(n)] + ([tuple(np.array(pts[int(n) - 1]) + (np.array(pts[min(int(n), len(pts) - 1)]) -
                                                                np.array(pts[int(n) - 1])) * (n - int(n)))]
                              if int(n) < len(pts) else [])
        c.line(seg, (40, 40, 50), 12)

def scene_park(c, t):
    # B = friend (left, faces right), A = husband (right, faces left)
    bt = speaking(t, 7.3, 14.7) + speaking(t, 20.1, 23.3)
    at = speaking(t, 15.2, 19.9) + speaking(t, 23.9, 27.2)
    pb = sit(t, 330)
    if 7.3 < t < 14.7:
        pb = gesture(pb, "open" if t < 12.6 else "point", t, wiggle=12)
    elif 20.1 < t < 23.4:
        pb = gesture(pb, "scratch", t)
    pa = sit(t + 1.3, 750)
    if 15.2 < t < 19.9 or 23.9 < t < 27.3:
        pa = gesture(pa, "open", t, wiggle=14)
    fb = "sad" if 12.7 < t < 14.7 else ("surprised" if 20.1 < t < 21.2 else "happy")
    jb = draw_person(c, pb, FRIEND, facing=1, face=fb, talk=bt, t=t)
    ja = draw_person(c, pa, HUSBAND, facing=-1, face="happy", talk=at, t=t)
    bubble(c, t, 8.4, 12.4, jb["head"], jb["r"], icon=icon_home_heart, side=-1, width=300)
    bubble(c, t, 12.7, 14.8, jb["head"], jb["r"], icon=icon_storm, side=-1, width=300)
    bubble(c, t, 16.0, 19.9, ja["head"], ja["r"], text="Nhà tôi toàn người SAI!", side=1, width=400)
    bubble(c, t, 21.1, 23.4, jb["head"], jb["r"], icon=icon_question, side=-1, width=220)
    bubble(c, t, 24.0, 26.2, ja["head"], ja["r"], text="Ví dụ nhé...", side=1, width=330)
    bubble(c, t, 26.2, 27.4, ja["head"], ja["r"], icon=icon_cup, side=1, width=220)

TABLE_TOP, CUP_EDGE = 1000, 662

def scene_home_good(c, t):
    # husband: drinks, leaves cup at the edge, walks off
    if t < 30.3:
        ph = idle(t, 560)
        if t < 28.6:
            ph = gesture(ph, "drink")
        else:
            ph = mix_gesture(ph, "drink", "place", (t - 28.6) / 0.5)
        fh = 1
    else:
        ph, fh = move(t, 560, 250, 30.3, 31.6)
        if t > 31.6:
            fh = 1
    if 40.6 < t:
        ph, _ = move(t, 250, 400, 40.6, 42.3)
        fh = 1
    if 42.7 < t < 47.8:
        ph = gesture(ph, "chest", t, wiggle=6)
    elif 47.8 < t < 49.4:
        ph = gesture(ph, "touch")
    hface = "sad" if 42.7 < t < 47.8 else ("surprised" if 34.3 < t < 35.4 or 51.7 < t < 52.6 else "happy")
    # wife: walks in, bumps the cup, apologizes
    pw, fw = move(t, -120, 545, 31.4, 33.95)
    fw_face = "happy"
    if t > 34.2:
        fw = -1
        pw = idle(t, 545)
        fw_face = "surprised" if t < 35.3 else "sad"
        if 35.3 < t < 42.6:
            pw = gesture(pw, "bow")
            pw[2] = 22 * smooth((t - 35.3) / 0.4) * smooth((42.6 - t) / 0.4)
        if t > 47.8:
            fw_face = "happy"
    if 33.6 < t < 34.2:
        pw = gesture(pw, "place")
    # son: runs in, steps on glass, apologizes
    ps, fs = move(t, -100, 690, 50.4, 51.75, run=True)
    sface = "happy"
    if 51.75 < t < 52.9:
        ps = idle(t, 690)
        ps[3], ps[4], ps[5], ps[6] = 70, 110, -5, 4
        ps[1] = -25 * abs(math.sin((t - 51.75) * 9))
        ps = gesture(ps, "up", t, wiggle=20)
        sface = "cry"
    elif t >= 52.9:
        fs = -1
        ps = idle(t, 690)
        if t < 56.8:
            ps = gesture(ps, "bow")
            ps[2] = 18
            sface = "sad"
    if t > 55.6:
        floating_hearts(c, t, 540, 820, spread=380, n=7, t0=55.6)
    if 47.9 < t < 49.6:
        floating_hearts(c, t, 470, 840, spread=60, n=2, t0=47.9)
    shadow(c, ph[0])
    shadow(c, pw[0], 0.93)
    if t > 50.3:
        shadow(c, ps[0], 0.62)
    jh = draw_person(c, ph, HUSBAND, facing=fh, face=hface, talk=speaking(t, 42.7, 49.3), t=t)
    jw = None
    if t > 31.3:
        jw = draw_person(c, pw, WIFE, facing=fw, face=fw_face, talk=speaking(t, 37.1, 40.6), t=t)
    if t > 50.3:
        js = draw_person(c, ps, SON, facing=fs, face=sface, talk=speaking(t, 52.9, 56.8), t=t)
    # cup: hand -> table edge -> falls -> shards
    if t < 29.1:
        hx, hy = jh["rhand"]
        if t < 28.6:
            cup(c, hx + 10, hy + 18, 1.0)
        else:
            k = smooth((t - 28.6) / 0.5)
            cup(c, hx + 10 + (CUP_EDGE - hx - 10) * k, hy + 18 + (TABLE_TOP - hy - 18) * k)
    elif t < 34.0:
        cup(c, CUP_EDGE, TABLE_TOP)
        if 29.2 < t < 31.2:  # highlight "mép bàn"
            pulse = (t * 2.5) % 1
            c.circle(CUP_EDGE, TABLE_TOP - 22, 50 + 40 * pulse, outline=(255, 80, 80, 255), width=6 * (1 - pulse) + 1)
    elif t < 34.45:
        k = (t - 34.0) / 0.45
        cup(c, CUP_EDGE - 40 * k, TABLE_TOP + (GROUND - TABLE_TOP) * k * k, angle=-k * 2.4)
    shards(c, t, 34.45, CUP_EDGE - 40)
    comic(c, t, 34.45, 760, 820, "XOẢNG!")
    comic(c, t, 51.8, 850, 900, "ÁI DA!", color=(255, 160, 60))
    if jw:
        bubble(c, t, 37.1, 40.6, jw["head"], jw["r"], text="Em xin lỗi!", side=1, width=320)
    bubble(c, t, 42.7, 47.7, jh["head"], jh["r"], text="Lỗi là do anh!", side=-1, width=340)
    bubble(c, t, 47.8, 49.4, jh["head"], jh["r"], text="Em có sao không?", side=-1, width=380)
    if t > 52.9:
        bubble(c, t, 52.9, 56.8, js["head"], js["r"], text="Con xin lỗi ạ!", side=1, width=330)

def scene_lesson(c, t):
    lt = t - 57.2
    rays(c, 540, 700, t, (255, 220, 170))
    c.circle(540, 700, 150, fill=(255, 210, 120))
    house(c, 540, GROUND + 10, 460, (255, 214, 160), (220, 90, 70), lit=True)
    k = back_out((lt - 4.3) / 0.4)
    if k > 0:
        heart(c, 540, 470 + 6 * math.sin(t * 4), 120 * k * (1 + 0.05 * math.sin(t * 8)), (255, 80, 110))
    floating_hearts(c, t, 540, 1000, spread=700, n=9, t0=57.5)
    hop = lambda ph: -abs(math.sin(t * 4 + ph)) * 10
    ph = gesture(P(380, dy=hop(0)), "hands")
    pw = gesture(P(700, dy=hop(1)), "hands")
    ps = gesture(P(540, dy=hop(2)), "up" if 63.1 < t < 65 else "hands")
    for x, k_ in ((380, 1), (700, 0.93), (540, 0.62)):
        shadow(c, x, k_)
    draw_person(c, ph, HUSBAND, facing=1, t=t)
    draw_person(c, pw, WIFE, facing=-1, t=t)
    draw_person(c, ps, SON, facing=1, t=t)

def scene_home_bad(c, t):
    dark = smooth((t - 92.9) / 1.0)
    # husband stands left with hands on hips, wife enters and bumps the cup
    ph = gesture(idle(t, 250), "akimbo")
    fh, hface = 1, "angry"
    if 78.9 < t < 83.2:
        ph = gesture(ph, "point", t, wiggle=8)
    pw, fw = move(t, -120, 545, 70.8, 72.6)
    if t < 70.8:
        pw, fw = idle(t, -200), 1
    wface = "angry" if t > 73.3 else "happy"
    if 72.2 < t < 72.7:
        pw = gesture(pw, "place")
    if t > 73.0:
        fw = -1
        pw = gesture(idle(t, 545), "point" if 73.4 < t < 78.6 else "akimbo", t, wiggle=8)
    ps, fs = move(t, -100, 690, 83.6, 85.6, run=True)
    sface = "happy"
    if 85.6 < t < 86.6:
        ps = idle(t, 690)
        ps[3], ps[4], ps[5], ps[6] = 70, 110, -5, 4
        ps[1] = -25 * abs(math.sin((t - 85.6) * 9))
        ps = gesture(ps, "up", t, wiggle=20)
        sface = "cry"
    elif t >= 86.6:
        ps = gesture(idle(t, 690), "cry")
        ps[1] = 6 * math.sin(t * 14)
        sface, fs = "cry", -1
    if t > 93.6:  # everyone turns away from each other
        fh, fw = -1, 1
        ph = gesture(ph, "akimbo")
        pw = gesture(idle(t, 545), "akimbo")
    if 66.5 < t < 71.9:  # opening: storm cloud, both already cold
        cloud(c, 540, 300 + 5 * math.sin(t * 2), 1.2, (110, 112, 128))
        if 70.3 < t < 70.45 or 70.9 < t < 71.0:
            bolt(c, 520, 380, 1.1)
    shadow(c, ph[0])
    if t > 70.8:
        shadow(c, pw[0], 0.93)
    if t > 83.6:
        shadow(c, ps[0], 0.62)
    jh = draw_person(c, ph, HUSBAND, facing=fh, face=hface, talk=speaking(t, 78.9, 83.0), t=t)
    if t > 70.8:
        jw = draw_person(c, pw, WIFE, facing=fw, face=wface, talk=speaking(t, 73.4, 78.5), t=t)
    if t > 83.6:
        js = draw_person(c, ps, SON, facing=fs, face=sface, talk=0, t=t)
    if t < 72.7:
        cup(c, CUP_EDGE, TABLE_TOP)
    elif t < 73.15:
        k = (t - 72.7) / 0.45
        cup(c, CUP_EDGE - 40 * k, TABLE_TOP + (GROUND - TABLE_TOP) * k * k, angle=-k * 2.4)
    shards(c, t, 73.15, CUP_EDGE - 40)
    comic(c, t, 73.15, 780, 820, "XOẢNG!")
    comic(c, t, 85.65, 850, 900, "ÁI DA!", color=(255, 160, 60))
    if t > 73.4 and t < 78.6:
        steam(c, t, jw["head"], jw["r"])
    if 78.9 < t < 83.2:
        steam(c, t, jh["head"], jh["r"])
    if t > 70.8:
        bubble(c, t, 74.5, 78.5, jw["head"], jw["r"], text="Anh để cốc kiểu gì vậy?!", side=-1, width=420,
               color=(255, 235, 235))
    bubble(c, t, 80.0, 83.1, jh["head"], jh["r"], text="Em có mù đâu?!", side=1, width=360, color=(255, 235, 235))
    if t > 83.6:
        bubble(c, t, 92.2, 94.0, js["head"], js["r"], text="Đau quá!", side=-1, width=270, color=(235, 245, 255))
    if dark > 0:
        cloud(c, 540, 260 + 5 * math.sin(t * 2), 1.4 * dark, (70, 72, 88))
        if 94.0 < t < 94.15 or 96.4 < t < 96.55:
            bolt(c, 520, 360, 1.3)

def scene_end(c, t):
    lt = t - 97.6
    rays(c, 540, 800, t, (60, 40, 75), n=16, r=1300)
    k = back_out(lt / 0.5)
    heart(c, 540, 800, 260 * k * (1 + 0.04 * math.sin(t * 6)), (255, 80, 110))
    floating_hearts(c, t, 540, 1100, spread=700, n=8, t0=97.6)

SCENES = [  # key, start, header label, draw fn
    ("houses", 0.0, "Câu chuyện hôm nay", scene_houses),
    ("park", 4.4, "Hai người bạn", scene_park),
    ("home_good", 27.25, "Nhà toàn người SAI", scene_home_good),
    ("lesson", 57.2, "Bài học", scene_lesson),
    ("home_bad", 66.55, "Nhà toàn người ĐÚNG", scene_home_bad),
    ("end", 97.6, None, scene_end),
]
DUR = 100.6
TRANS = 0.55

def scene_index(t):
    return max(i for i, s in enumerate(SCENES) if s[1] <= t)

def render_scene(i, t):
    key, start, label, fn = SCENES[i]
    img = background(key)
    c = Canvas(img)
    c.d = ImageDraw.Draw(img, "RGBA")
    fn(c, t)
    out = img.reduce(SS)
    if key == "home_bad":
        dark = smooth((t - 92.9) / 1.0) * 0.35 + 0.12
        flash = 1.0 if (94.0 < t < 94.12 or 96.4 < t < 96.5) else 0.0
        out = Image.blend(out, Image.new("RGB", out.size, (20, 20, 40)), dark)
        if flash:
            out = Image.blend(out, Image.new("RGB", out.size, (255, 255, 255)), 0.45)
    return out

# ---------------------------------------------------------------- captions
STROKE = (18, 16, 28)
CAP_SIZE, CAP_Y, CAP_MAXW = 90, 1555, W - 110
_sprites = {}

def sprite(word, style):
    key = (word, style)
    if key in _sprites:
        return _sprites[key]
    f = font(BIG, CAP_SIZE * (1.12 if style == "key" else 1.0))
    pad = 40
    bbox = f.getbbox(word, stroke_width=9)
    w, h = bbox[2] - bbox[0] + 2 * pad, int(CAP_SIZE * 1.6) + 2 * pad
    org = (pad - bbox[0], pad + int(CAP_SIZE * 0.25))
    m_fill = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m_fill).text(org, word, font=f, fill=255)
    m_stroke = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m_stroke).text(org, word, font=f, fill=255, stroke_width=9, stroke_fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sh = m_stroke.filter(ImageFilter.GaussianBlur(8)).point(lambda v: int(v * 0.6))
    out.paste((0, 0, 0, 255), (0, 8), sh)
    if style == "key":
        glow = m_stroke.filter(ImageFilter.GaussianBlur(18)).point(lambda v: min(255, int(v * 1.3)))
        out.paste((255, 70, 60, 255), (0, 0), glow)
    out.paste(STROKE + (255,), (0, 0), m_stroke)
    if style == "key":
        top, bot = org[1] + CAP_SIZE * 0.05, org[1] + CAP_SIZE * 1.15
        g = np.clip((np.arange(h)[:, None] - top) / (bot - top), 0, 1)
        col = (np.array([255, 240, 150]) * (1 - g) + np.array([255, 95, 60]) * g).astype(np.uint8)
        grad = Image.fromarray(np.repeat(col[:, None, :], w, axis=1).reshape(h, w, 3), "RGB")
        out.paste(grad, (0, 0), m_fill)
    else:
        out.paste((255, 222, 40, 255) if style == "hl" else (255, 255, 255, 255), (0, 0), m_fill)
    res = (out, pad, bbox[2] - bbox[0])
    _sprites[key] = res
    return res

def layout(ph):
    words = [w["w"].upper() for w in ph]
    widths = [sprite(w, "key" if x["key"] else "plain")[2] for w, x in zip(words, ph)]
    space = CAP_SIZE * 0.26
    lines, cur, cw = [], [], 0
    for i, wd in enumerate(widths):
        add = wd + (space if cur else 0)
        if cur and cw + add > CAP_MAXW:
            lines.append((cur, cw))
            cur, cw = [], 0
            add = wd
        cur.append(i)
        cw += add
    lines.append((cur, cw))
    pos = {}
    lh = CAP_SIZE * 1.3
    y0 = CAP_Y - (len(lines) - 1) * lh / 2
    for li, (idx, lw) in enumerate(lines):
        x = W / 2 - lw / 2
        for i in idx:
            pos[i] = (x + widths[i] / 2, y0 + li * lh)
            x += widths[i] + space
    return words, pos

_layouts = {}
def draw_captions(img, t):
    cur = None
    for pi, ph in enumerate(PHRASES):
        nxt = PHRASES[pi + 1][0]["s"] if pi + 1 < len(PHRASES) else 1e9
        if ph[0]["s"] - 0.08 <= t < min(nxt - 0.02, ph[-1]["e"] + 0.9):
            cur = pi
    if cur is None:
        return
    ph = PHRASES[cur]
    if cur not in _layouts:
        _layouts[cur] = layout(ph)
    words, pos = _layouts[cur]
    end_fade = smooth((ph[-1]["e"] + 0.9 - t) / 0.2)
    for i, (w, info) in enumerate(zip(words, ph)):
        p = (t - info["s"] + 0.08) / 0.18
        if p <= 0:
            continue
        active = info["s"] - 0.08 <= t <= info["e"] + 0.05
        style = "key" if info["key"] else ("hl" if active else "plain")
        spr, pad, ww = sprite(w, style)
        s = (0.6 + 0.4 * ease_out(p)) * (1 + 0.25 * (1 - ease_out(p))) if p < 1 else 1.0
        if active and info["key"]:
            s *= 1.0 + 0.06 * math.sin(clamp((t - info["s"]) / (info["e"] - info["s"] + 0.01)) * math.pi)
        a = smooth(p * 2) * end_fade
        im = spr if abs(s - 1) < 0.01 else spr.resize((max(1, int(spr.width * s)), max(1, int(spr.height * s))),
                                                         Image.BILINEAR)
        if a < 0.99:
            al = im.getchannel("A").point(lambda v: int(v * a))
            im = im.copy()
            im.putalpha(al)
        x, y = pos[i]
        y += 18 * (1 - ease_out(p))
        img.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))

# ---------------------------------------------------------------- overlays
_header = {}
def header_img(label):
    if label in _header:
        return _header[label]
    f = font(BIG, 44)
    tw = int(f.getlength(label))
    bw, bh, pad = tw + 80, 84, 40
    img = Image.new("RGBA", (bw + 2 * pad, bh + 2 * pad), (0, 0, 0, 0))
    box = [pad, pad, pad + bw, pad + bh]
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle(box, bh // 2, outline=255, width=4)
    img.paste((60, 200, 255, 255), (0, 0), m.filter(ImageFilter.GaussianBlur(12)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, bh // 2, fill=(10, 24, 50, 235))
    img.paste((150, 235, 255, 255), (0, 0), m)
    d.text((pad + bw / 2, pad + bh / 2), label, font=f, fill=(140, 220, 255), anchor="mm")
    _header[label] = img
    return img

_bottom = None
def bottom_shade():
    global _bottom
    if _bottom is None:
        a = np.clip((np.arange(H) - 1300) / 300, 0, 1) * 150
        alpha = np.repeat(a[:, None], W, axis=1).astype(np.uint8)
        _bottom = Image.new("RGBA", (W, H), (8, 8, 20, 0))
        _bottom.putalpha(Image.fromarray(alpha))
    return _bottom

def end_text(img, t):
    lt = t - 97.6
    d = ImageDraw.Draw(img)
    for txt, y, t0, size, grad in (("Nhận sai một chút", 1390, 0.3, 70, False),
                                    ("NHÀ SẼ ẤM ÊM!", 1530, 0.8, 118, True)):
        p = (lt - t0) / 0.35
        if p <= 0:
            continue
        s = back_out(p)
        f = font(BIG if grad else BOLD, size * s)
        if grad:
            m = Image.new("L", (W, 300), 0)
            ImageDraw.Draw(m).text((W / 2, 150), txt, font=f, fill=255, anchor="mm")
            glow = m.filter(ImageFilter.GaussianBlur(26)).point(lambda v: min(255, int(v * 1.6)))
            img.paste((255, 130, 30), (0, y - 150), glow)
            top, bot = 150 - size * s * 0.5, 150 + size * s * 0.4
            g = np.clip((np.arange(300)[:, None] - top) / max(1, bot - top), 0, 1)
            col = (np.array([255, 248, 190]) * (1 - g) + np.array([255, 150, 40]) * g).astype(np.uint8)
            img.paste(Image.fromarray(np.repeat(col[:, None, :], W, axis=1).reshape(300, W, 3), "RGB"),
                      (0, y - 150), m)
        else:
            d.text((W / 2, y), txt, font=f, fill=(245, 245, 255), anchor="mm")

def iris(old, new, k):
    """Reveal `new` through a growing circle."""
    r = 1200 * ease_out(k)
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).ellipse([W / 2 - r, H * 0.42 - r, W / 2 + r, H * 0.42 + r], fill=255)
    out = old.copy()
    out.paste(new, (0, 0), m)
    ring = Image.new("L", (W, H), 0)
    ImageDraw.Draw(ring).ellipse([W / 2 - r, H * 0.42 - r, W / 2 + r, H * 0.42 + r], outline=255, width=14)
    out.paste((255, 255, 255), (0, 0), ring)
    return out

def frame(t):
    i = scene_index(t)
    img = render_scene(i, t)
    lt = t - SCENES[i][1]
    if i > 0 and lt < TRANS:
        img = iris(render_scene(i - 1, t), img, lt / TRANS)
    img = img.convert("RGBA")
    if SCENES[i][0] != "end":
        img.alpha_composite(bottom_shade())
    label = SCENES[i][2]
    if label:
        k = back_out((lt - 0.15) / 0.4)
        hi = header_img(label)
        if k > 0.02:
            hs = hi.resize((max(1, int(hi.width * k)), max(1, int(hi.height * k))), Image.BILINEAR)
            img.alpha_composite(hs, (W // 2 - hs.width // 2, 150 - hs.height // 2))
    if SCENES[i][0] == "end":
        rgb = img.convert("RGB")
        end_text(rgb, t)
        img = rgb.convert("RGBA")
    else:
        draw_captions(img, t)
    # progress bar
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 10], fill=(0, 0, 0, 90))
    d.rectangle([0, 0, int(W * t / DUR), 10], fill=(90, 210, 255, 255))
    return img.convert("RGB")

def frame_bytes(f):
    return frame(f / FPS).tobytes()

def main():
    voice, out = sys.argv[1], sys.argv[2]
    if "--frames" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--frames") + 1].split(",")]
        for t in ts:
            frame(t).save(f"{out}_{t:06.2f}.png")
        return
    n = int(DUR * FPS)
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error",
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", voice, "-filter:a", "afade=t=out:st=97.45:d=0.5,apad",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "160k", "-t", f"{DUR}", "-movflags", "+faststart", out],
                           stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for k, b in enumerate(pool.imap(frame_bytes, range(n), chunksize=6)):
            enc.stdin.write(b)
            if k % 300 == 0:
                print(f"{k}/{n}", flush=True)
    enc.stdin.close()
    enc.wait()

if __name__ == "__main__":
    main()
