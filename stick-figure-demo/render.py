"""Render a 10s stick-figure demo video (1080x1920, 30fps) with Pillow + ffmpeg."""
import math, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, DUR = 1080, 1920, 30, 10.0
SS = 2  # supersampling for anti-aliased lines
GROUND = 1450
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
OUT = sys.argv[1] if len(sys.argv) > 1 else "stick_figure_demo.mp4"

THIGH, SHIN, TORSO, NECK, HEAD = 135, 135, 230, 25, 58
UPPER, FORE = 115, 105
LINE = 16

def smooth(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)

def ease_out(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3

# pose = [hip_x, hip_dy, lean, lthigh, lknee, rthigh, rknee, larm, lelbow, rarm, relbow]
# Angles in degrees; 0 = pointing down, positive = toward the right (forward).
def run_pose(t):
    p = t * 2 * math.pi * 1.6
    s = math.sin(p)
    x = -200 + (W / 2 + 200) * ease_out(t / 4.0)
    return np.array([x, -abs(math.sin(p)) * 18, 12,
                     38 * s, 15 + 55 * max(0, -math.cos(p)),
                     -38 * s, 15 + 55 * max(0, math.cos(p)),
                     -45 * s, 70, 45 * s, 70])

def idle_pose(t):
    b = math.sin(t * 2 * math.pi * 0.8)
    return np.array([W / 2, 4 * b, 0, 10, 4, -10, 4, -12, 8, 12, 8])

def wave_pose(t):
    w = math.sin((t - 5.0) * 2 * math.pi * 2.2)
    pose = idle_pose(t)
    pose[9], pose[10] = 140, 20 + 28 * w  # right arm up, forearm waving
    return pose

def jump_pose(t):
    pose = idle_pose(t)
    lt = t - 8.2
    if lt < 0.35:  # crouch
        c = smooth(lt / 0.35)
        pose[1] = 60 * c
        pose[3:7] = [35 * c + 10, 70 * c, 35 * c - 10, 70 * c]
        pose[7:11] = [-35 * c, 20, 35 * c, 20]
    elif lt < 1.0:  # airborne
        a = (lt - 0.35) / 0.65
        pose[1] = -320 * 4 * a * (1 - a)
        pose[3:7] = [25, 45, 5, 45]
        pose[7:11] = [-150, -15, 150, 15]
    else:  # land
        c = 1 - smooth((lt - 1.0) / 0.4)
        pose[1] = 45 * c
        pose[3:7] = [10 + 25 * c, 4 + 55 * c, -10 + 25 * c, 4 + 55 * c]
        pose[7:11] = [-12 - 60 * c, 8, 12 + 60 * c, 8]
    return pose

SEGMENTS = [(0.0, 3.7, run_pose), (3.7, 5.0, idle_pose), (5.0, 8.0, wave_pose), (8.0, 10.1, jump_pose)]
BLEND = 0.3

def pose_at(t):
    for i, (a, b, fn) in enumerate(SEGMENTS):
        if a <= t < b:
            cur = fn(t)
            if i > 0 and t < a + BLEND:
                k = smooth((t - a) / BLEND)
                return SEGMENTS[i - 1][2](t) * (1 - k) + cur * k
            return cur
    return SEGMENTS[-1][2](t)

def vec(origin, ang, length):
    r = math.radians(ang)
    return (origin[0] + math.sin(r) * length, origin[1] + math.cos(r) * length)

def draw_figure(d, pose, color):
    hx, hdy, lean, lt, lk, rt, rk, la, le, ra, re = pose
    leg = THIGH + SHIN - 12
    hip = (hx, GROUND - leg + hdy)
    sh = vec(hip, 180 - lean, TORSO)
    neck = vec(sh, 180 - lean, NECK)
    head = vec(neck, 180 - lean, HEAD)
    segs = []
    for th, kn in ((lt, lk), (rt, rk)):
        knee = vec(hip, th, THIGH)
        foot = vec(knee, th - kn, SHIN)
        foot = (foot[0], min(foot[1], GROUND))
        segs += [(hip, knee), (knee, foot)]
    for ar, el in ((la, le), (ra, re)):
        elbow = vec(sh, ar, UPPER)
        hand = vec(elbow, ar + el, FORE)
        segs += [(sh, elbow), (elbow, hand)]
    segs.append((hip, neck))
    lw = LINE * SS
    for a, b in segs:
        a2, b2 = (a[0] * SS, a[1] * SS), (b[0] * SS, b[1] * SS)
        d.line([a2, b2], fill=color, width=lw)
        for p in (a2, b2):
            d.ellipse([p[0] - lw / 2, p[1] - lw / 2, p[0] + lw / 2, p[1] + lw / 2], fill=color)
    cx, cy, r = head[0] * SS, head[1] * SS, HEAD * SS
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255), outline=color, width=lw)
    # face looks toward the direction of travel
    ex = 14 * SS
    for dx in (-18, 18):
        d.ellipse([cx + (dx + 10) * SS - ex / 2, cy - 12 * SS - ex / 2, cx + (dx + 10) * SS + ex / 2, cy - 12 * SS + ex / 2], fill=color)
    d.arc([cx - 18 * SS, cy - 8 * SS, cx + 38 * SS, cy + 32 * SS], 20, 160, fill=color, width=8 * SS)
    return hip

def background():
    top, bot = np.array([255, 236, 210]), np.array([255, 190, 170])
    g = np.linspace(0, 1, H * SS)[:, None]
    col = (top * (1 - g) + bot * g).astype(np.uint8)
    img = np.repeat(col[:, None, :], W * SS, axis=1)
    img[GROUND * SS:] = (90, 70, 110)
    return Image.fromarray(img, "RGB")

def draw_text(d, text, y, t0, t, size, color):
    if t < t0:
        return
    k = (t - t0) / 0.35
    scale = ease_out(k) * (1 + 0.12 * math.sin(min(k, 1) * math.pi))
    if scale <= 0.02:
        return
    font = ImageFont.truetype(FONT, int(size * scale * SS))
    d.text((W / 2 * SS, y * SS), text, font=font, fill=color, anchor="mm",
           stroke_width=int(10 * SS * scale), stroke_fill=(255, 255, 255))

def main():
    bg = background()
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", OUT]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    ink = (40, 30, 60)
    for f in range(int(DUR * FPS)):
        t = f / FPS
        img = bg.copy()
        d = ImageDraw.Draw(img)
        pose = pose_at(t)
        # shadow shrinks while the figure is in the air
        air = max(0.0, -pose[1]) / 320
        sw = (110 - 50 * air) * SS
        cx = pose[0] * SS
        d.ellipse([cx - sw, (GROUND - 14) * SS, cx + sw, (GROUND + 14) * SS], fill=(70, 52, 90))
        draw_figure(d, pose, ink)
        draw_text(d, "Xin chào!", 420, 5.1, t, 150, (230, 80, 90))
        draw_text(d, "Video người que", 1650, 8.4, t, 82, ink)
        draw_text(d, "làm thử 10 giây", 1760, 8.7, t, 66, (230, 80, 90))
        frame = img.resize((W, H), Image.LANCZOS)
        proc.stdin.write(frame.tobytes())
    proc.stdin.close()
    proc.wait()

if __name__ == "__main__":
    main()
