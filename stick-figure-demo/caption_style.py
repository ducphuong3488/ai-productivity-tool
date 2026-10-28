"""Re-frame the stick-figure demo in a 'tutorial reel' style: dark background,
glowing numbered badge, glowing card, and two-line captions with a big
gradient + glow headline (white small line above, cyan-blue big line below)."""
import subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H, FPS, DUR = 1080, 1920, 30, 10.0
SRC = sys.argv[1] if len(sys.argv) > 1 else "stick_figure_demo.mp4"
OUT = sys.argv[2] if len(sys.argv) > 2 else "stick_figure_caption_style.mp4"
BIG = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
SMALL = "/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf"
CYAN = (120, 230, 255)

# (start, end, badge number, badge label, small line, big line)
SCENES = [
    (0.0, 3.6, 1, "Chạy vào", "đầu tiên thì nó sẽ", "CHẠY VÀO,"),
    (3.6, 8.0, 2, "Vẫy tay", "sau đó thì nó sẽ", "VẪY TAY CHÀO,"),
    (8.0, 10.0, 3, "Nhảy lên", "và cuối cùng là", "NHẢY LÊN!"),
]

CARD_W, CARD_H, CARD_Y = 720, 1000, 380
CROP_Y, CROP_H = 320, 1500  # region of the source video shown inside the card

def ease_out(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3

def pop(x):
    """0 -> slight overshoot -> 1 over x in [0, 1]."""
    x = min(max(x, 0.0), 1.0)
    return ease_out(x) * (1 + 0.15 * np.sin(x * np.pi))

def text_mask(text, font, tracking):
    """Render text with custom letter spacing into an L mask, tightly cropped."""
    widths = [font.getlength(c) for c in text]
    total = int(sum(widths) + tracking * (len(text) - 1)) + 40
    asc, desc = font.getmetrics()
    m = Image.new("L", (total, asc + desc + 40), 0)
    d = ImageDraw.Draw(m)
    x = 20
    for c, w in zip(text, widths):
        d.text((x, 20), c, font=font, fill=255)
        x += w + tracking
    return m.crop(m.getbbox())

def glow_layer(size, mask, pos, color, radius, strength):
    canvas = Image.new("L", size, 0)
    canvas.paste(mask, pos)
    blur = canvas.filter(ImageFilter.GaussianBlur(radius))
    blur = blur.point(lambda v: min(255, int(v * strength)))
    layer = Image.new("RGB", size, color)
    return layer, blur

def paste_gradient_text(img, mask, cx, cy, top, bottom, glow_color):
    w, h = mask.size
    pos = (int(cx - w / 2), int(cy - h / 2))
    for radius, strength in ((28, 1.4), (10, 1.0)):
        layer, a = glow_layer(img.size, mask, pos, glow_color, radius, strength)
        img.paste(layer, (0, 0), a)
    g = np.linspace(0, 1, h)[:, None, None]
    grad = (np.array(top) * (1 - g) + np.array(bottom) * g).astype(np.uint8)
    grad = Image.fromarray(np.repeat(grad, w, axis=1), "RGB")
    img.paste(grad, pos, mask)

def paste_plain_text(img, mask, cx, cy, color):
    w, h = mask.size
    pos = (int(cx - w / 2), int(cy - h / 2))
    shadow = Image.new("L", img.size, 0)
    shadow.paste(mask, (pos[0], pos[1] + 4))
    img.paste((0, 0, 0), (0, 0), shadow.filter(ImageFilter.GaussianBlur(6)))
    img.paste(Image.new("RGB", mask.size, color), pos, mask)

def scaled(mask, s):
    if s <= 0.02:
        return None
    return mask.resize((max(1, int(mask.width * s)), max(1, int(mask.height * s))), Image.LANCZOS)

def background():
    y, x = np.mgrid[0:H, 0:W]
    # dark navy with a soft teal glow around the card
    d = np.sqrt(((x - W / 2) / W) ** 2 + ((y - (CARD_Y + CARD_H / 2)) / H) ** 2)
    glow = np.clip(1 - d * 2.2, 0, 1)[..., None]
    base = np.array([6, 14, 26]) * (1 - glow) + np.array([10, 52, 72]) * glow
    img = base.astype(np.uint8)
    img[:80] = 0  # black status-bar strip like a phone screen recording
    return Image.fromarray(img, "RGB")

def rounded_mask(w, h, r):
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
    return m

def glowing_outline(size, box, r, width, color, blur):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle(box, r, outline=255, width=width)
    return m.filter(ImageFilter.GaussianBlur(blur)), m

def make_badge(num, label):
    f_num = ImageFont.truetype(BIG, 46)
    f_lab = ImageFont.truetype(BIG, 46)
    lab = text_mask(label, f_lab, 0)
    bw, bh = lab.width + 140, 86
    pad = 40
    img = Image.new("RGBA", (bw + 2 * pad, bh + 2 * pad), (0, 0, 0, 0))
    box = [pad, pad, pad + bw, pad + bh]
    soft, hard = glowing_outline(img.size, box, bh // 2, 4, CYAN, 12)
    img.paste((60, 200, 255, 255), (0, 0), soft)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, bh // 2, fill=(8, 30, 60, 255))
    img.paste((150, 235, 255, 255), (0, 0), hard)
    # blue square with the step number
    sq = [pad + 14, pad + 14, pad + 14 + 58, pad + 14 + 58]
    d.rounded_rectangle(sq, 12, fill=(40, 120, 255, 255))
    d.text(((sq[0] + sq[2]) / 2, (sq[1] + sq[3]) / 2), str(num), font=f_num, fill="white", anchor="mm")
    img.paste((120, 210, 255, 255), (pad + 92, pad + (bh - lab.height) // 2), lab)
    return img

def main():
    bg = background()
    card_round = rounded_mask(CARD_W, CARD_H, 28)
    soft, hard = glowing_outline((W, H), [W // 2 - CARD_W // 2 - 4, CARD_Y - 4,
                                          W // 2 + CARD_W // 2 + 4, CARD_Y + CARD_H + 4], 32, 5, CYAN, 18)
    bg.paste((40, 200, 255), (0, 0), soft.point(lambda v: min(255, v * 2)))
    bg.paste((170, 240, 255), (0, 0), hard)

    f_small = ImageFont.truetype(SMALL, 68)
    f_big = ImageFont.truetype(BIG, 150)
    assets = []
    for s in SCENES:
        small = text_mask(s[4], f_small, -3)
        big = text_mask(s[5], f_big, -5)
        if big.width > W - 80:  # shrink long headlines to fit
            big = scaled(big, (W - 80) / big.width)
        assets.append((make_badge(s[2], s[3]), small, big))

    dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", SRC, "-vf",
                            f"crop=1080:{CROP_H}:0:{CROP_Y},scale={CARD_W}:{CARD_H}",
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                            "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", OUT],
                           stdin=subprocess.PIPE)
    fsize = CARD_W * CARD_H * 3
    for f in range(int(DUR * FPS)):
        t = f / FPS
        raw = dec.stdout.read(fsize)
        img = bg.copy()
        if len(raw) == fsize:
            img.paste(Image.frombytes("RGB", (CARD_W, CARD_H), raw), (W // 2 - CARD_W // 2, CARD_Y), card_round)
        i = next(k for k, s in enumerate(SCENES) if s[0] <= t < s[1] or k == len(SCENES) - 1)
        st = t - SCENES[i][0]
        badge, small, big = assets[i]

        b = scaled(badge, pop(st / 0.35))
        if b:
            img.paste(b, (W // 2 - b.width // 2, 300 - b.height // 2), b)
        sm = scaled(small, ease_out((st - 0.05) / 0.3))
        if sm:
            paste_plain_text(img, sm, W / 2, 1490, (240, 245, 250))
        bg_ = scaled(big, pop((st - 0.3) / 0.35))
        if bg_:
            paste_gradient_text(img, bg_, W / 2, 1610, (190, 245, 255), (40, 140, 255), (30, 150, 255))
        enc.stdin.write(img.tobytes())
    enc.stdin.close()
    enc.wait()
    dec.stdout.close()
    dec.wait()

if __name__ == "__main__":
    main()
