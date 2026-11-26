"""Retention features learned from top glow-up series (see RUNBOOK 3b). All optional, driven by the episode JSON:

"hud":        always-on score tiles, top-left, every frame (replaces the day pill)
              {"tiles": [{"label": "DAYS LEFT", "value": "27", "color": [255,214,102]},
                         {"label": "GLOW-UP", "value": "40%", "from": "34%", "at": ["s2", 0], "color": [120,225,120]},
                         {"label": "AURA", "value": "21/100", "from": "10/100", "at": ["sb", -1], "color": [235,80,95]}]}
              A tile with "from" shows the old value until scene/line "at", then pops to the new one.
"stickers" kind "calendar": {"scene": "s1", "line": 0, "kind": "calendar", "text": "26", "y": 700, "hold": 3} = the flip-calendar DAYS LEFT prop
"cover_title": ["DAY 4", "THE GYM"] -> designed cover (big title over the hero frame) instead of a frame grab
"cover_image": "jess_d06_walter.jpg" -> hero frame for the cover (default: the last beat image)
"captions":   word-by-word voice captions (2-3 words at a time, keywords coloured)
              {"scenes": ["s1","sb","s3","s4"], "y": 1500, "keywords": ["maya","aura"], "color": [255,214,102]}
"stickers":   tilted pop-in labels / sound-effect cards (+ a pop sound)
              [{"scene": "s3", "line": 1, "text": "CLANK", "bg": [190,195,205], "fg": [20,20,20], "y": 560, "angle": -5, "hold": 1.8, "size": 120}]
"comments":   real viewer comment cards (handle + likes), e.g. the winning vote (+ a ding)
              [{"scene": "s1", "line": 0, "user": "someone", "text": "fix his hair pls", "likes": 12, "y": 470, "hold": 3.0}]
"scoreboard": the "LAST EPISODE" scene ("sb", inserted after s2) turning real engagement into points
              {"title": "LAST EPISODE", "label": "AURA", "from": 10, "to": 21, "max": 100,
               "rows": [["COMMENTS", "+1 each", "6", 6], ["LIKES", "+1 each", "2", 2], ["SHARES", "+5 each", "0", 0], ["VIEWS", "+1 per 100", "318", 3]]}
              Script key "sb": line 0 = title, one line per row, last line = the total.
"""
import math, re
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from common import W, H, FPS, F, ease, back, center_paste

SR = 24000
def _sfx():
    tt = np.arange(int(0.18 * SR)) / SR
    pop = 0.30 * np.sin(2 * np.pi * (900 * tt - 1800 * tt ** 2)) * np.exp(-tt * 28)
    t2 = np.arange(int(0.6 * SR)) / SR
    ding = 0.14 * (np.sin(2 * np.pi * 1046.5 * t2) + 0.6 * np.sin(2 * np.pi * 1568 * t2)) * np.exp(-t2 * 7)
    t3 = np.arange(int(0.09 * SR)) / SR
    tick = 0.12 * np.sin(2 * np.pi * 1400 * t3) * np.exp(-t3 * 45)
    return {"pop": pop, "ding": ding, "tick": tick}
SFX = _sfx()

def col(c, d=(255, 255, 255)):
    return tuple(c) if c else d

def fade(im, a):
    if a >= 1: return im
    x = np.array(im); x[..., 3] = (x[..., 3] * max(0, a)).astype(np.uint8); return Image.fromarray(x)

def scaled(im, s):
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)

def wrap(d, text, font, maxw):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: out.append(cur); cur = w
    return out + [cur] if cur else out


class Extras:
    # ---------- timing helpers ----------
    def line_t(self, scene, line):
        st = self.TM.get(scene) or [0.0]
        return st[line if -len(st) <= line < len(st) else -1]

    def sfx_times(self, n):
        ev = [("pop", self.line_t(n, s.get("line", 0)) + s.get("delay", 0)) for s in self.c.get("stickers", []) if s["scene"] == n]
        ev += [("ding", self.line_t(n, s.get("line", 0)) + s.get("delay", 0)) for s in self.c.get("comments", []) if s["scene"] == n]
        if n == "sb" and self.c.get("scoreboard"):
            st = self.TM["sb"]; ev += [("tick", st[min(i + 1, len(st) - 1)]) for i in range(len(self.c["scoreboard"]["rows"]))]
            ev.append(("ding", st[-1]))
        return ev

    # ---------- build ----------
    def build_extras(self):
        c = self.c
        self.STICK = [(s, self.sticker_img(s)) for s in c.get("stickers", [])]
        self.CARDS = [(s, self.comment_img(s)) for s in c.get("comments", [])]
        self.HUD = None
        if c.get("hud"):
            self.HUD = [(t, self.tile_img(t, t.get("from", t["value"])), self.tile_img(t, t["value"])) for t in c["hud"]["tiles"]]
        self.build_captions()

    def tile_img(self, t, value):
        fl, fv = F("Bold", 32), F("Black", 76)
        d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        w = int(max(d.textlength(t["label"], font=fl), d.textlength(value, font=fv)) + 52); h = 148
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=22, fill=(16, 18, 30, 238), outline=(70, 72, 92, 255), width=3)
        d.text((w // 2, 36), t["label"], font=fl, fill=(240, 240, 245), anchor="mm")
        d.text((w // 2, 98), value, font=fv, fill=col(t.get("color"), (255, 214, 102)), anchor="mm")
        return im

    def sticker_img(self, s):
        if s.get("kind") == "calendar": return self.calendar_img(s)
        f = F("Black", s.get("size", 120)); d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        bb = d.textbbox((0, 0), s["text"], font=f); tw, th = bb[2] - bb[0], bb[3] - bb[1]
        px, py = 46, 30; w, h = tw + 2 * px, th + 2 * py
        im = Image.new("RGBA", (w + 30, h + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([12, 16, w + 12, h + 16], radius=26, fill=(0, 0, 0, 150))  # drop shadow
        d.rounded_rectangle([2, 2, w, h], radius=26, fill=col(s.get("bg"), (102, 200, 92)), outline=(15, 15, 18), width=9)
        d.text((2 + w // 2, 2 + h // 2), s["text"], font=f, fill=col(s.get("fg")), anchor="mm")
        return im.rotate(s.get("angle", -4), resample=Image.BICUBIC, expand=True)

    def calendar_img(self, s):
        w, h = 440, 470; im = Image.new("RGBA", (w + 40, h + 50), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([22, 40, w + 22, h + 40], radius=34, fill=(0, 0, 0, 140))
        d.rounded_rectangle([6, 22, w + 6, h + 22], radius=34, fill=(250, 250, 250), outline=(15, 15, 18), width=9)
        d.rounded_rectangle([6, 22, w + 6, 140], radius=34, fill=(226, 72, 72), outline=(15, 15, 18), width=9)
        d.rectangle([15, 100, w - 3, 140], fill=(226, 72, 72)); d.line([(6, 140), (w + 6, 140)], fill=(15, 15, 18), width=9)
        d.text((w // 2 + 6, 84), s.get("label", "DAYS LEFT"), font=F("Black", 54), fill=(255, 255, 255), anchor="mm")
        d.text((w // 2 + 6, 320), str(s["text"]), font=F("Black", 250), fill=(12, 12, 14), anchor="mm")
        for x in (110, w - 98): d.ellipse([x - 20, 4, x + 20, 44], fill=(160, 160, 168), outline=(15, 15, 18), width=6)
        return im.rotate(s.get("angle", 5), resample=Image.BICUBIC, expand=True)

    def comment_img(self, s):
        w = 940; fu, ft, fl = F("Bold", 40), F("Medium", 46), F("Bold", 34)
        d = ImageDraw.Draw(Image.new("RGBA", (1, 1))); lines = wrap(d, s["text"], ft, w - 300)[:3]
        h = 120 + 56 * len(lines)
        im = Image.new("RGBA", (w + 16, h + 18), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([10, 14, w + 10, h + 14], radius=40, fill=(0, 0, 0, 120))
        d.rounded_rectangle([0, 0, w, h], radius=40, fill=(255, 255, 255, 250), outline=(20, 20, 24), width=6)
        cx, cy, r = 92, 92, 52
        hue = sum(map(ord, s["user"])) % 4
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=[(225, 95, 140), (240, 200, 60), (90, 170, 240), (110, 200, 120)][hue])
        d.text((cx, cy), s["user"][:1].upper(), font=F("Black", 54), fill=(255, 255, 255), anchor="mm")
        d.text((175, 62), s["user"], font=fu, fill=(20, 20, 24), anchor="lm")
        for i, ln in enumerate(lines): d.text((175, 120 + i * 56), ln, font=ft, fill=(30, 30, 34), anchor="lm")
        hx, hy = w - 95, 66
        d.polygon([(hx - 24, hy - 6), (hx, hy + 24), (hx + 24, hy - 6)], fill=(232, 40, 80))
        d.ellipse([hx - 25, hy - 22, hx + 1, hy + 4], fill=(232, 40, 80)); d.ellipse([hx - 1, hy - 22, hx + 25, hy + 4], fill=(232, 40, 80))
        d.text((hx, 122), f"{s.get('likes', 0):,}", font=fl, fill=(120, 120, 128), anchor="mm")
        return im.rotate(s.get("angle", 1.5), resample=Image.BICUBIC, expand=True)

    def build_captions(self):
        self.CAP = {}; cc = self.c.get("captions")
        if not cc: return
        kw = {k.lower() for k in cc.get("keywords", [])}; hi = col(cc.get("color"), (255, 214, 102))
        self.CAP_Y = cc.get("y", 1500); self._capcache = {}
        for sc in cc.get("scenes", ["s1", "sb", "s3", "s4"]):
            if sc not in self.order or sc not in self.c["script"]: continue
            out = []
            for (gap, txt), a, b in zip(self.c["script"][sc], self.TM[sc], self.TE[sc]):
                words = txt.replace("...", "… ").split(); chunks, cur = [], []
                for w in words:
                    cur.append(w)
                    if len(cur) == 3 or re.search(r"[.,!?…:;]$", w) or (len(cur) == 2 and len("".join(cur)) > 11): chunks.append(cur); cur = []
                if cur: chunks.append(cur)
                tot = sum(len("".join(ch)) + 2 * len(ch) for ch in chunks); t = a
                for ch in chunks:
                    dt = (b - a) * (len("".join(ch)) + 2 * len(ch)) / max(1, tot)
                    styled = []
                    for w in ch:
                        k = re.sub(r"[^\w']", "", w).lower()
                        styled.append((w.upper(), hi if (k in kw or any(x.isdigit() for x in k)) else (255, 255, 255)))
                    out.append((t, t + dt, styled)); t += dt
            self.CAP[sc] = out

    def cap_img(self, styled):
        key = tuple(styled)
        if key in self._capcache: return self._capcache[key]
        size = 96
        while True:
            f = F("Black", size); d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
            sp = d.textlength(" ", font=f); tw = sum(d.textlength(w, font=f) for w, _ in styled) + sp * (len(styled) - 1)
            if tw <= 980 or size < 56: break
            size -= 6
        im = Image.new("RGBA", (int(tw) + 40, size + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = 20
        for w, c in styled:
            d.text((x + 3, 30 + size // 2 + 6), w, font=f, fill=(0, 0, 0, 160), anchor="lm", stroke_width=9, stroke_fill=(0, 0, 0, 160))
            d.text((x, 30 + size // 2), w, font=f, fill=c, anchor="lm", stroke_width=9, stroke_fill=(10, 10, 12))
            x += d.textlength(w, font=f) + sp
        self._capcache[key] = im; return im

    # ---------- per-frame ----------
    def overlay(self, n, t, im):
        for s, img in self.CARDS:
            if s["scene"] != n: continue
            t0 = self.line_t(n, s.get("line", 0)) + s.get("delay", 0); t1 = t0 + s.get("hold", 3.0)
            if t0 <= t < t1:
                p = back((t - t0) / .35); a = min(1, (t - t0) / .15, (t1 - t) / .25)
                center_paste(im, fade(scaled(img, 0.75 + 0.25 * p), a), s.get("y", 470) - 40 * (1 - ease((t - t0) / .35)))
        for s, img in self.STICK:
            if s["scene"] != n: continue
            t0 = self.line_t(n, s.get("line", 0)) + s.get("delay", 0); t1 = min(t0 + s.get("hold", 1.8), self.DUR[n] - 0.1)
            if t0 <= t < t1:
                p = (t - t0) / .28; k = (0.3 + 0.7 * back(p)) * (1 + 0.02 * math.sin((t - t0) * 9))
                lay = fade(scaled(img, k), min(1, (t1 - t) / .2))
                if "x" in s: im.alpha_composite(lay, (int(s["x"] - lay.width / 2), int(s.get("y", 560) - lay.height / 2)))
                else: center_paste(im, lay, s.get("y", 560))
        for a, b, styled in self.CAP.get(n, []):
            if a <= t < b + 0.05:
                p = ease((t - a) / .12); center_paste(im, scaled(self.cap_img(styled), 0.85 + 0.15 * p), self.CAP_Y); break
        if self.HUD:
            x = 24; idx = self.order.index(n)
            for tile, old, new in self.HUD:
                img, flash = old, 0
                if "at" in tile:
                    sc, ln = tile["at"]; si = self.order.index(sc) if sc in self.order else 99
                    ta = self.line_t(sc, ln) if sc in self.TM else 0
                    if idx > si or (idx == si and t >= ta): img = new; flash = max(0, 1 - (t - ta) / .5) if idx == si else 0
                else: img = new
                if flash > 0:
                    g = Image.new("RGBA", (img.width + 16, img.height + 16), (0, 0, 0, 0))
                    ImageDraw.Draw(g).rounded_rectangle([0, 0, g.width - 1, g.height - 1], radius=24, fill=(110, 230, 120, int(200 * flash)))
                    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(4)), (x - 8, 200 - 8))
                    s2 = scaled(img, 1 + 0.12 * flash); im.alpha_composite(s2, (x - (s2.width - img.width) // 2, 200 - (s2.height - img.height) // 2))
                else: im.alpha_composite(img, (x, 200))
                x += img.width + 12
        return im

    # ---------- the LAST EPISODE scoreboard scene ----------
    def sb(self, t):
        d = self.DUR["sb"]; sbc = self.c["scoreboard"]; st = self.TM["sb"]
        im = self.bg(t, d, 1.05, 1.12, self.BLUR)
        ov = Image.new("RGBA", (W, H), (8, 10, 30, 120)); im.alpha_composite(ov)
        title = sbc.get("title", "LAST EPISODE"); ft = F("Black", 64)
        a = ease((t - st[0]) / .35)
        if a > 0:
            L = Image.new("RGBA", (W, 110), (0, 0, 0, 0)); dd = ImageDraw.Draw(L)
            dd.text((W // 2, 55), "  ".join(title), font=F("Black", 54), fill=(235, 235, 245), anchor="mm")
            center_paste(im, fade(L, a), 450)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(ov)
        for i, (lab, rate, val, pts) in enumerate(sbc["rows"]):
            ti = st[min(i + 1, len(st) - 1)] + (0 if i + 1 < len(st) else 0.35 * (i + 2 - len(st)))
            p = ease((t - ti) / .35)
            if p <= 0: continue
            y = 560 + i * 165; xo = int((1 - p) * 140); A = int(255 * p)
            dr.rounded_rectangle([50 + xo, y, 1030 + xo, y + 140], radius=30, fill=(18, 20, 44, int(235 * p)), outline=(70, 74, 120, A), width=4)
            dr.text((90 + xo, y + 52), lab, font=F("Black", 50), fill=(255, 255, 255, A), anchor="lm")
            dr.text((92 + xo, y + 106), rate.upper(), font=F("Bold", 28), fill=(185, 185, 200, A), anchor="lm")
            dr.text((700 + xo, y + 70), str(val), font=F("Black", 62), fill=(245, 222, 90, A), anchor="rm")
            dr.text((990 + xo, y + 70), f"+{pts}", font=F("Black", 62), fill=((110, 230, 110) if pts else (150, 150, 160)) + (A,), anchor="rm")
        im.alpha_composite(ov)
        tt = st[-1]
        if t > tt:
            p = back((t - tt) / .4); cnt = ease((t - tt - 0.3) / 1.0)
            v = int(round(sbc["from"] + (sbc["to"] - sbc["from"]) * cnt))
            bw, bh = 760, 190; box = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); dd = ImageDraw.Draw(box)
            dd.rounded_rectangle([0, 0, bw - 1, bh - 1], radius=40, fill=(14, 16, 40, 250), outline=(236, 110, 180), width=8)
            dd.text((70, bh // 2), sbc.get("label", "AURA"), font=F("Black", 66), fill=(236, 110, 180), anchor="lm")
            dd.text((bw - 200, bh // 2 + 4), str(v), font=F("Black", 120), fill=(255, 255, 255), anchor="rm")
            dd.text((bw - 190, bh // 2 + 30), f"/{sbc.get('max', 100)}", font=F("Black", 54), fill=(200, 200, 215), anchor="lm")
            center_paste(im, scaled(box, 0.6 + 0.4 * p), 560 + len(sbc["rows"]) * 165 + 110)
        return im

    def make_cover(self):
        ct = self.c.get("cover_title")
        if not ct: return
        if self.c.get("cover_image"):  # Nov 26: cover = the fail image (RUNBOOK 5l.7), not the last beat
            import os as _os
            self.BIG = self.cover(Image.open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "assets", self.c["cover_image"])).convert("RGB"))
        im = self.bg(0, 1, 1.0, 1.0); self.shade(im, 0.3, 0.9, 0.55)
        if self.HUD:
            x = 24
            for _, _, new in self.HUD: im.alpha_composite(new, (x, 200)); x += new.width + 12
        big = Image.new("RGBA", (W, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(big)
        d.text((W // 2 + 8, 158), ct[0], font=F("Black", 230), fill=(0, 0, 0, 170), anchor="mm", stroke_width=14, stroke_fill=(0, 0, 0, 170))
        d.text((W // 2, 150), ct[0], font=F("Black", 230), fill=(255, 214, 102), anchor="mm", stroke_width=14, stroke_fill=(12, 12, 14))
        center_paste(im, big.rotate(-3, resample=Image.BICUBIC), 1180)
        if len(ct) > 1: center_paste(im, self.sticker_img({"text": ct[1], "bg": [236, 110, 160], "size": 78, "angle": -3}), 1420)
        im.convert("RGB").save(f"{self.out}/cover.jpg", quality=92)
