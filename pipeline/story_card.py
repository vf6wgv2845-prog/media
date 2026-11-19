"""Make a 1080x1920 story JPEG in the retention format (RUNBOOK 3b): HUD tiles, flip-calendar, real comment card,
sticker headline, optional stat bars + day log, CTA sticker. Every story on every account uses this.
Usage: python3 -I pipeline/story_card.py spec.json
spec = {"image": "theo_gaming.jpg",                 # from pipeline/assets
        "out": "stories/2026-11-20_theo_tracker.jpg",  # relative to the repo root
        "hud": [{"label": "DAYS LEFT", "value": "26", "color": [255,214,102]}, ...],   # same tiles as the Reel
        "calendar": "26",                            # optional flip-calendar (big days-left number)
        "headline": ["DAY 4", "THE GYM"],            # optional: big title + coloured sticker
        "comment": {"user": "handle", "text": "verbatim", "likes": 3},   # optional: a REAL comment
        "stats": [["Hair", 2], ...], "accent": [214,48,64],              # optional bars
        "log": [["❌", "Day 1", "Cut from varsity"], ...],               # optional day log (max 4)
        "cta": "VOTE ON THE NEWEST REEL"}            # sticker at the bottom
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from common import *
from extras import Extras, scaled
from PIL import ImageEnhance

class _S(Extras):
    def __init__(self): self.c = {}

def main(spec):
    x = _S(); root = os.path.dirname(HERE)
    src = Image.open(os.path.join(HERE, "assets", spec["image"])).convert("RGB")
    k = max(W / src.width, H / src.height); r = src.resize((int(src.width * k) + 1, int(src.height * k) + 1), Image.LANCZOS)
    ox = (r.width - W) // 2; oy = int((r.height - H) * 0.3); im = r.crop((ox, oy, ox + W, oy + H))
    has_body = bool(spec.get("stats") or spec.get("log"))
    im = ImageEnhance.Brightness(im).enhance(0.75 if not has_body else 0.6).convert("RGBA")
    y = np.linspace(0, 1, H)[:, None]; a = np.clip((y - 0.38) / 0.4, 0, 1) * 0.85
    ov = np.zeros((H, W, 4), np.uint8); ov[..., 3] = (a * 255).astype(np.uint8).repeat(W, 1); im.alpha_composite(Image.fromarray(ov))
    if spec.get("hud"):
        xx = 24
        for t in spec["hud"]:
            tile = x.tile_img(t, t["value"]); im.alpha_composite(tile, (xx, 200)); xx += tile.width + 12
    if spec.get("calendar"):
        cal = scaled(x.calendar_img({"text": spec["calendar"], "angle": 5}), 0.8); im.alpha_composite(cal, (W - cal.width - 30, 380))
    cy = 860 if spec.get("calendar") else 620
    if spec.get("headline"):
        h = spec["headline"]; big = Image.new("RGBA", (W, 280), (0, 0, 0, 0)); d = ImageDraw.Draw(big)
        d.text((W // 2, 140), h[0], font=F("Black", 190), fill=(255, 214, 102), anchor="mm", stroke_width=13, stroke_fill=(12, 12, 14))
        center_paste(im, big.rotate(-3, resample=Image.BICUBIC), cy); cy += 170
        if len(h) > 1:
            st = x.sticker_img({"text": h[1], "bg": spec.get("headline_color", [236, 110, 160]), "size": 70, "angle": -3})
            center_paste(im, st, cy); cy += st.height // 2 + 40
    if spec.get("comment"):
        card = x.comment_img(spec["comment"]); center_paste(im, card, cy + card.height // 2); cy += card.height + 30
    if spec.get("stats"):
        acc = tuple(spec.get("accent", [214, 48, 64])); n = len(spec["stats"])
        box = (70, cy, 1010, cy + 60 + n * 72); L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.rounded_rectangle(box, radius=40, fill=(10, 10, 16, 200))
        for i, (lab, v) in enumerate(spec["stats"]):
            yy = cy + 66 + i * 72
            d.text((120, yy), lab, font=F("Bold", 42), fill=(255, 255, 255), anchor="lm")
            d.rounded_rectangle([460, yy - 14, 840, yy + 14], radius=14, fill=(255, 255, 255, 55))
            d.rounded_rectangle([460, yy - 14, max(488, 460 + 380 * v / 10), yy + 14], radius=14, fill=acc)
            d.text((960, yy), f"{v}/10", font=F("ExtraBold", 42), fill=(255, 255, 255), anchor="rm")
        im.alpha_composite(L); cy = box[3] + 30
    if spec.get("log"):
        rows = spec["log"][-4:]; L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); box = (70, cy, 1010, cy + 40 + 86 * len(rows))
        d.rounded_rectangle(box, radius=40, fill=(10, 10, 16, 200)); ems = []
        for i, (e, day, txt) in enumerate(rows):
            yy = cy + 63 + i * 86; ems.append((emoji(e, 54), yy))
            d.text((190, yy), day, font=F("ExtraBold", 44), fill=(255, 214, 102), anchor="lm")
            d.text((350, yy), txt, font=F("Medium", 40), fill=(255, 255, 255), anchor="lm")
        im.alpha_composite(L)
        for em, yy in ems: im.alpha_composite(em, (110, yy - em.height // 2))
        cy = box[3] + 30
    if spec.get("cta"):
        st = x.sticker_img({"text": spec["cta"], "bg": [102, 200, 92], "size": 58, "angle": -2})
        center_paste(im, st, max(cy + st.height // 2 + 10, 1560))
    out = os.path.join(root, spec["out"]); os.makedirs(os.path.dirname(out), exist_ok=True)
    im.convert("RGB").save(out, quality=92); print(out)

if __name__ == "__main__":
    main(json.load(open(sys.argv[1])))
