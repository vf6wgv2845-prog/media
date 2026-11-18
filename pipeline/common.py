import math, random, subprocess, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
OUT = os.path.dirname(os.path.abspath(__file__))
FD = "/usr/share/fonts/opentype/inter/"
def F(w, s): return ImageFont.truetype(FD + f"Inter-{w}.otf", s)
EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

_emoji_cache = {}
def emoji(ch, size):
    k = (ch, size)
    if k not in _emoji_cache:
        f = ImageFont.truetype(EMOJI_FONT, 109)
        im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((80, 80), ch, font=f, embedded_color=True, anchor="mm")
        im = im.crop(im.getbbox())
        r = size / max(im.size)
        _emoji_cache[k] = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)
    return _emoji_cache[k]

def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def back(x):
    x = max(0.0, min(1.0, x)); c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

def gradient(top, bot):
    a = np.linspace(0, 1, H)[:, None, None]
    g = (np.array(top)[None, None] * (1 - a) + np.array(bot)[None, None] * a)
    g = np.repeat(g, W, axis=1).astype(np.uint8)
    return Image.fromarray(g, "RGB").convert("RGBA")

# ---------- helpers ----------
def text_layer(lines, size, weight="Black", color=(255, 255, 255), spacing=1.12, shadow=True, maxw=940):
    f = F(weight, size)
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    rows = []
    for ln in lines:
        rows.append((ln if isinstance(ln, tuple) else (ln, color)))
    lh = int(size * spacing); hgt = lh * len(rows) + 30
    im = Image.new("RGBA", (W, hgt), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (t, c) in enumerate(rows):
        y = 10 + i * lh + lh // 2
        if shadow:
            d.text((W // 2 + 4, y + 5), t, font=f, fill=(0, 0, 0, 150), anchor="mm")
        d.text((W // 2, y), t, font=f, fill=c, anchor="mm")
    if shadow:
        sh = im.filter(ImageFilter.GaussianBlur(0))
    return im

def paste_anim(base, layer, y, t0, t, dur=0.35, rise=50, pop=False):
    p = (t - t0) / dur
    if p <= 0: return
    e = ease(p)
    lay = layer
    if pop:
        s = 0.6 + 0.4 * back(p)
        lay = layer.resize((max(1, int(layer.width * s)), max(1, int(layer.height * s))), Image.BILINEAR)
    if e < 1:
        a = np.array(lay); a[..., 3] = (a[..., 3] * e).astype(np.uint8); lay = Image.fromarray(a)
    x = (W - lay.width) // 2
    yy = int(y + (1 - e) * rise + (layer.height - lay.height) / 2)
    base.alpha_composite(lay, (x, yy))

def pill(text, size, fg, bg, pad=(34, 16), weight="ExtraBold"):
    f = F(weight, size)
    bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), text, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    im = Image.new("RGBA", (tw + pad[0] * 2, th + pad[1] * 2 + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=im.height // 2, fill=bg)
    d.text((im.width // 2, im.height // 2), text, font=f, fill=fg, anchor="mm")
    return im

def center_paste(base, im, cy, alpha=1.0):
    if alpha < 1:
        a = np.array(im); a[..., 3] = (a[..., 3] * alpha).astype(np.uint8); im = Image.fromarray(a)
    base.alpha_composite(im, ((W - im.width) // 2, int(cy - im.height / 2)))

rs = random.Random(3)
SNOW = [(rs.uniform(0, W), rs.uniform(0, H), rs.uniform(2, 6), rs.uniform(40, 110), rs.uniform(0, 6.28)) for _ in range(110)]
def snow(base, t, alpha=200):
    d = ImageDraw.Draw(base)
    for x, y, r, v, ph in SNOW:
        yy = (y + v * t) % H; xx = x + math.sin(t * 0.8 + ph) * 18
        d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=(255, 255, 255, int(alpha * (r / 6) ** .5)))

