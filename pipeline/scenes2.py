"""Extra scene types learned from @30daystofix (Nov 21 analysis). Use by adding the key to "order" and a script entry.
"sm" = PREVIOUSLY montage (hook): flashes of earlier days, 0.4-0.6 s each, with a DAY label and a status tag.
   cfg "montage": [{"image": "theo_scruffy.jpg", "label": "DAY 1", "tag": "STINKY"}, {"image": "...", "label": "DAY 2", "tag": "SKIN: FIXED"}, ...,
                   {"image": "...", "label": "NOW", "tag": ""}]   (images from pipeline/assets; the last one should be the current look)
   script "sm": 1-2 short lines spoken over it (e.g. "Twenty-five days until he sees his ex.")
"sc" = text-message chat scene: phone mockup, bubbles appear one by one, Theo's reply is typed live then sent.
   cfg "chat": {"name": "Maya", "sub": "his ex", "msgs": [["them", "was that you at the gym?"], ["me", "maybe"], ...]}
   Messages are spread over the script "sc" lines: message i appears at line min(i, n_lines-1) start (+0.35 s steps if several share a line).
   A "me" message is typed into the input box for ~0.9 s before it pops into the thread."""
import os, math
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from common import W, H, F, ease, back, center_paste

HERE = os.path.dirname(os.path.abspath(__file__))

class Scenes2:
    # ---------- montage ----------
    def _montage_frames(self):
        if getattr(self, "_MON", None) is not None: return self._MON
        self._MON = []
        for m in self.c.get("montage", []):
            src = Image.open(os.path.join(HERE, "assets", m["image"])).convert("RGB")
            big = self.cover(src)
            lab = self.sticker_img({"text": m.get("label", ""), "bg": [235, 80, 95] if m.get("label") != "NOW" else [102, 200, 92], "size": 90, "angle": -3}) if m.get("label") else None
            tag = self.sticker_img({"text": m["tag"], "bg": [102, 200, 92], "fg": [15, 15, 15], "size": 70, "angle": 3}) if m.get("tag") else None
            self._MON.append((big, lab, tag))
        return self._MON

    def sm(self, t):
        fr = self._montage_frames(); d = self.DUR["sm"]
        if not fr: return self.bg(t, d, 1.0, 1.05)
        n = len(fr); seg = max(0.35, (d - 0.3) / n); i = min(n - 1, int(t / seg)); lt = t - i * seg
        big, lab, tag = fr[i]
        z = 1.0 + 0.06 * (lt / seg)
        im = self.bg(lt, seg, z, z + 0.01, big)
        if lt < 0.06: im = Image.blend(Image.new("RGBA", (W, H), (255, 255, 255, 255)), im, lt / 0.06)  # flash cut
        if lab: center_paste(im, lab, 470)
        if tag: center_paste(im, tag, 1250)
        return im

    # ---------- chat ----------
    def _bubble(self, text, me):
        f = F("Medium", 40); d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        words, lines, cur = text.split(), [], ""
        for w in words:
            tt = (cur + " " + w).strip()
            if d.textlength(tt, font=f) <= 440: cur = tt
            else: lines.append(cur); cur = w
        lines.append(cur)
        tw = max(d.textlength(l, font=f) for l in lines); bw, bh = int(tw + 52), 30 + 52 * len(lines)
        im = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
        dd.rounded_rectangle([0, 0, bw - 1, bh - 1], radius=30, fill=(10, 132, 255) if me else (229, 229, 234))
        for k, l in enumerate(lines): dd.text((26, 15 + k * 52), l, font=f, fill=(255, 255, 255) if me else (20, 20, 24))
        return im

    def sc(self, t):
        d = self.DUR["sc"]; ch = self.c.get("chat", {}); msgs = ch.get("msgs", [])
        im = self.bg(t, d, 1.15, 1.18, self.BLUR)
        ov = Image.new("RGBA", (W, H), (40, 10, 70, 120)); im.alpha_composite(ov)
        px0, py0, px1, py1 = 150, 400, 930, 1640
        ph = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dp = ImageDraw.Draw(ph)
        dp.rounded_rectangle([px0 - 18, py0 - 18, px1 + 18, py1 + 18], radius=80, fill=(12, 12, 16, 255))
        dp.rounded_rectangle([px0, py0, px1, py1], radius=64, fill=(250, 250, 252, 255))
        dp.rounded_rectangle([(px0 + px1) // 2 - 90, py0 + 16, (px0 + px1) // 2 + 90, py0 + 52], radius=18, fill=(12, 12, 16, 255))
        dp.rectangle([px0, py0 + 70, px1, py0 + 190], fill=(240, 240, 244, 255))
        dp.ellipse([px0 + 30, py0 + 95, px0 + 100, py0 + 165], fill=(236, 80, 130, 255))
        dp.text((px0 + 65, py0 + 130), ch.get("name", "?")[:1].upper(), font=F("Black", 40), fill=(255, 255, 255), anchor="mm")
        dp.text((px0 + 120, py0 + 112), ch.get("name", ""), font=F("Bold", 42), fill=(20, 20, 24), anchor="lm")
        dp.text((px0 + 120, py0 + 152), ch.get("sub", ""), font=F("Medium", 30), fill=(236, 80, 130), anchor="lm")
        dp.rounded_rectangle([px0 + 30, py1 - 110, px1 - 30, py1 - 40], radius=35, fill=(255, 255, 255, 255), outline=(200, 200, 206, 255), width=3)
        im.alpha_composite(ph)
        st = self.TM.get("sc", [0.0]); n = len(st); shown = []; typing = None
        times = []
        for i in range(len(msgs)):
            k = min(i, n - 1); extra = max(0, i - (n - 1)) * 0.9
            times.append(st[k] + extra)
        for i, (who, text) in enumerate(msgs):
            t0 = times[i]; me = who == "me"
            if me:
                if t0 - 0.9 <= t < t0: typing = text[:max(1, int(len(text) * (t - (t0 - 0.9)) / 0.9))]
            if t >= t0: shown.append((i, me, text, t0))
        y = py1 - 140; dd = ImageDraw.Draw(im)
        for i, me, text, t0 in reversed(shown):
            b = self._bubble(text, me); p = back(min(1, (t - t0) / 0.3))
            y -= b.height + 18
            if y < py0 + 210: break
            bb = b.resize((max(1, int(b.width * (0.7 + 0.3 * p))), max(1, int(b.height * (0.7 + 0.3 * p)))))
            x = px1 - 40 - bb.width if me else px0 + 40
            im.alpha_composite(bb, (int(x), int(y)))
        dd.text((px0 + 60, py1 - 75), typing + "|" if typing else "iMessage", font=F("Medium", 34), fill=(30, 30, 34) if typing else (160, 160, 168), anchor="lm")
        return im
