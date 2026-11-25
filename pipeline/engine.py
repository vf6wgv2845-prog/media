"""Generic episode renderer: hero image + 5 scenes (hook, stats, conflict, premise, vote), free Kokoro voice."""
import sys, os, math, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from common import *
from extras import Extras, SFX
from scenes2 import Scenes2
from PIL import ImageEnhance
import soundfile as sf

SR = 24000

class Episode(Scenes2, Extras):
    def __init__(self, cfg, outdir):
        self.c = cfg; self.out = outdir; os.makedirs(outdir, exist_ok=True)
        src = Image.open(cfg["image"]).convert("RGB")
        self.CW, self.CH = int(1280 * 1.12), int(1920 * 1.12)
        self.BIG = self.cover(src)
        self.BLUR = ImageEnhance.Brightness(self.BIG.filter(ImageFilter.GaussianBlur(28))).enhance(0.45)
        self.DIM = ImageEnhance.Brightness(self.BIG.filter(ImageFilter.GaussianBlur(3))).enhance(0.55)
        self.pill = pill(cfg["pill"], 40, (255, 255, 255), cfg["accent"])
        self.BEFORE = None
        self.order = cfg.get("order") or (["s1", "s2", "sb", "s3", "s4", "s5"] if cfg.get("scoreboard") else ["s1", "s2", "s3", "s4", "s5"])
        if cfg.get("hud"): self.pill = Image.new("RGBA", (1, 1), (0, 0, 0, 0))  # the HUD replaces the day pill
        self._prep_beats()
        if cfg.get("before_image"):
            b = Image.open(cfg["before_image"]).convert("RGB")
            self.BEFORE = self.cover(b)
            self.BEFORE_DIM = ImageEnhance.Brightness(self.BEFORE.filter(ImageFilter.GaussianBlur(3))).enhance(0.55)

    def _prep_beats(self):
        """cfg "beats": [{"scene": "s3", "line": 1, "image": "jess_dress.jpg"}, ...] = swap the background picture at that line
        (paths relative to pipeline/assets). Nov 21 evening fix: one static picture for 30 s is where viewers left (~9-11 s)."""
        base = (self.BIG, self.BLUR, self.DIM); self._BEATS = []
        for b in self.c.get("beats", []):
            path = b["image"] if os.path.isabs(b["image"]) else os.path.join(os.path.dirname(self.c["image"]), b["image"])
            big = self.cover(Image.open(path).convert("RGB"))
            self._BEATS.append((b["scene"], b.get("line", 0), b.get("delay", 0.0), (big, ImageEnhance.Brightness(big.filter(ImageFilter.GaussianBlur(28))).enhance(0.45),
                                                                    ImageEnhance.Brightness(big.filter(ImageFilter.GaussianBlur(3))).enhance(0.55))))
        self._BASE = base

    def _set_beat(self, n, t):
        self._since_beat = t  # time since the scene (or the latest beat in it) started; used by cfg "motion"
        if not self._BEATS: return
        cur = self._BASE; i = self.order.index(n)
        for sc, ln, dl, imgs in self._BEATS:
            if sc not in self.order: continue
            j = self.order.index(sc)
            if j < i or (j == i and t >= self.line_t(sc, ln) + dl):
                cur = imgs
                if j == i: self._since_beat = t - (self.line_t(sc, ln) + dl)
        self.BIG, self.BLUR, self.DIM = cur

    def cover(self, src):
        """Scale to fill CWxCH keeping aspect ratio (crop the overflow, biased to keep the top)."""
        k = max(self.CW / src.width, self.CH / src.height)
        r = src.resize((int(src.width * k) + 1, int(src.height * k) + 1), Image.LANCZOS)
        x = (r.width - self.CW) // 2; y = int((r.height - self.CH) * 0.3)
        return r.crop((x, y, x + self.CW, y + self.CH)).filter(ImageFilter.UnsharpMask(2, 60, 2))

    # ---------- audio ----------
    def voice(self):
        from kokoro_onnx import Kokoro
        k = Kokoro(os.environ.get('KOKORO_MODEL', '/tmp/tts/kokoro.onnx'), os.environ.get('KOKORO_VOICES', '/tmp/tts/voices.bin'))
        self.TM, self.DUR, self.TE = {}, {}, {}
        for sc, segs in self.c["script"].items():
            parts, starts, ends, t = [], [], [], 0.0
            for gap, txt in segs:
                a, sr = k.create(txt, voice=self.c["voice"], speed=self.c.get("speed", 1.08), lang='en-us')
                nz = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, nz[0] - 300): nz[-1] + 1200]
                parts.append(np.zeros(int(gap * SR))); t += gap; starts.append(round(t, 3)); parts.append(a); t += len(a) / SR; ends.append(round(t, 3))
            tail = 2.0 if sc == "s5" else 0.45
            parts.append(np.zeros(int(tail * SR))); t += tail
            sf.write(f"{self.out}/vo_{sc}.wav", np.concatenate(parts).astype(np.float32), SR)
            self.TM[sc] = starts; self.TE[sc] = ends; self.DUR[sc] = round(t * FPS) / FPS
        json.dump({"TM": self.TM, "DUR": self.DUR, "TE": self.TE}, open(f"{self.out}/timing.json", "w"))

    def load_timing(self):
        j = json.load(open(f"{self.out}/timing.json")); self.TM, self.DUR = j["TM"], j["DUR"]
        self.TE = j.get("TE") or {k: [b - 0.2 for b in v[1:]] + [self.DUR[k] - 0.5] for k, v in self.TM.items()}

    def mix(self):
        names = self.order; total = sum(self.DUR[n] for n in names)
        out = np.zeros(int(total * SR) + SR); off = 0.0; rng = np.random.default_rng(1)
        for n in names:
            vo, _ = sf.read(f"{self.out}/vo_{n}.wav"); s = int(off * SR); out[s:s + len(vo)] += vo
            if off > 0:
                L = int(0.35 * SR); tt = np.arange(L) / SR; nz = np.convolve(rng.standard_normal(L), np.ones(6) / 6, 'same')
                a = max(0, s - int(0.15 * SR)); out[a:a + L] += 0.05 * nz * np.sin(np.pi * tt / 0.35) ** 2
            if n == "s3":
                t0 = self.TM["s3"][self.c["notif_line"]]
                tt = np.arange(int(0.8 * SR)) / SR
                for f, dl in [(1318.5, 0), (1760, 0.09)]:
                    ss = s + int((t0 + dl) * SR); seg = 0.16 * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 6); out[ss:ss + len(seg)] += seg
            for kind, t0 in self.sfx_times(n):
                ss = s + int(t0 * SR); seg = SFX[kind]; out[ss:ss + len(seg)] += seg[:max(0, len(out) - ss)]
            off += self.DUR[n]
        out = out[:int(total * SR)]; out /= np.abs(out).max() * 1.05
        sf.write(f"{self.out}/mix.wav", out.astype(np.float32), SR)

    # ---------- visuals ----------
    def bg(self, t, dur, z0, z1, src=None):
        src = src or self.BIG; cx_off = self.c.get("cx", 0.0)
        z = (z0 + (z1 - z0) * (t / dur)) * (1 + 0.006 * math.sin(t * 2.0))
        sx = 0.0
        if self.c.get("motion"):  # Nov 25 (RUNBOOK 5j): punch-in + tiny shake on every picture change, stronger slow push
            k = getattr(self, "_since_beat", 9.0)
            z *= 1 + 0.04 * (t / max(dur, 0.1))
            if 0 <= k < 0.35:
                e = 1 - k / 0.35; z *= 1 + 0.09 * e * e; sx = math.sin(k * 90) * 14 * e
        vw = self.CW / (1.12 * z) * (1080 / 1280); vh = vw * 1920 / 1080
        x0 = max(0, min(self.CW - vw, self.CW / 2 - vw / 2 + cx_off * self.CW + sx))
        y0 = max(0, min(self.CH - vh, self.CH * 0.5 - vh / 2 - (self.CH - vh) * 0.05))
        return src.crop((int(x0), int(y0), int(x0 + vw), int(y0 + vh))).resize((W, H), Image.BILINEAR).convert("RGBA")

    def shade(self, im, top, bottom, start):
        y = np.linspace(0, 1, H)[:, None]
        a = np.where(y > start, (y - start) / (1 - start) * bottom, 0) + np.where(y < 0.18, (0.18 - y) / 0.18 * top, 0)
        ov = np.zeros((H, W, 4), np.uint8); ov[..., 3] = (np.clip(a, 0, 1) * 255).astype(np.uint8).repeat(W, 1)
        im.alpha_composite(Image.fromarray(ov))

    def panel(self, im, box, p):
        if p <= 0: return
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(ov).rounded_rectangle(box, radius=48, fill=(10, 10, 16, int(165 * p)))
        im.alpha_composite(ov.filter(ImageFilter.GaussianBlur(2)))

    def build_layers(self):
        c = self.c; gold = (255, 214, 102)
        self.L1 = [text_layer([c["hook"][0]], 100), text_layer([c["hook"][1]], 82, "ExtraBold"), text_layer([(c["hook"][2], gold)], 82, "ExtraBold")]
        self.NAME = text_layer([c["name_line"]], 100); self.SUB = text_layer([c["sub_line"]], 50, "Bold", color=(225, 225, 235))
        if c.get("conflict") and any(c["conflict"]): self.L3a = text_layer([c["conflict"][0]], 84); self.L3b = text_layer(c["conflict"][1], 64, "ExtraBold", color=(255, 120, 120))
        self.L4a = text_layer(c["premise"][0], 104); self.L4b = text_layer([(c["premise"][1], gold)], 56, "ExtraBold")
        self.L4c = text_layer(c["premise"][2], 56, "Bold", color=(225, 225, 240))
        self.L5a = text_layer(c["vote_q"], 92); self.L5b = text_layer([c.get("cta", "Comment the number below")], 58, "ExtraBold", color=gold)
        self.POINT = emoji("👇", 90)
        def row(e, label):
            w, h = 820, 128; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            d.rounded_rectangle([0, 0, w - 1, h - 1], radius=36, fill=(20, 20, 30, 150), outline=(255, 255, 255, 110), width=3)
            em = emoji(e, 72); im.alpha_composite(em, (50, (h - em.height) // 2))
            d.text((160, h // 2), label, font=F("ExtraBold", 48), fill=(255, 255, 255), anchor="lm"); return im
        self.ROWS = [row(e, f"{i + 1}  {l}" if c.get("numbered", True) else l) for i, (e, l) in enumerate(c["options"])]
        n = c["notif"]; w, h = 900, 200; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=44, fill=(242, 242, 247, 245))
        d.rounded_rectangle([30, 45, 140, 155], radius=26, fill=n.get("color", (52, 199, 89)))
        b = emoji(n.get("icon", "💬"), 64); im.alpha_composite(b, (85 - b.width // 2, 100 - b.height // 2))
        d.text((170, 62), n["from"], font=F("Bold", 42), fill=(20, 20, 24), anchor="lm")
        d.text((860, 62), "now", font=F("Medium", 32), fill=(130, 130, 138), anchor="rm")
        d.text((170, 128), n["msg"], font=F("Medium", 35), fill=(40, 40, 46), anchor="lm")
        if n.get("emoji"):
            sm = emoji(n["emoji"], 38); im.alpha_composite(sm, (170 + int(d.textlength(n["msg"], font=F("Medium", 35))) + 10, 110))
        self.NOTIF = im

    def s1(self, t):
        d = self.DUR["s1"]; im = self.bg(t, d, 0.93, 1.0, self.BEFORE_DIM if self.BEFORE is not None else self.DIM); st = self.TM["s1"]
        if self.c.get("snow"): snow(im, t, 150)
        center_paste(im, self.pill, 330)
        # Nov 21 evening fix: the 3 hook text lines used to wait for voice lines 2 and 3, so the hook's punchline was not on screen until ~3-4 s.
        # Now all 3 pop in during the first voice line (0.1 / 0.45 / 0.8 s). "hook_slow": true restores the old behaviour.
        slow = self.c.get("hook_slow")
        for i, (L, y) in enumerate(zip(self.L1, (700, 860, 970))):
            t0 = (st[i] if i < len(st) else st[-1] + 0.8 * (i - len(st) + 1)) if slow else st[0] + 0.35 * i
            paste_anim(im, L, y, t0, t, pop=(i == 0))
        tp = (st[-1] + 0.8 * max(0, 3 - len(st)) + 0.5) if slow else st[0] + 1.3
        if t > tp:
            e = emoji(self.c["hook_emoji"], 190); center_paste(im, e, 1260 - 30 * ease((t - tp) / .4), ease((t - tp) / .4))
        return im

    def s2(self, t):
        d = self.DUR["s2"]; st = self.TM["s2"]; im = self.bg(t, d, 0.9, 0.97)
        if self.BEFORE is not None:
            wp = ease((t - 0.5) / 1.3)
            if wp < 1:
                bim = self.bg(t, d, 0.9, 0.97, self.BEFORE)
                x = int(W * wp); 
                if x < W: im.paste(bim.crop((x, 0, W, H)), (x, 0))
                if 0 < wp < 1: ImageDraw.Draw(im).rectangle([x - 4, 0, x + 4, H], fill=(255, 255, 255, 255))
            lab = pill("AFTER" if wp >= 0.5 else "BEFORE", 34, (255, 255, 255), (30, 30, 36) if wp < 0.5 else self.c["accent"])
            if t < 3.2: center_paste(im, lab, 340, min(1, (3.2 - t) / 0.4))
        self.shade(im, 0.5, 1.0, 0.42)
        center_paste(im, self.pill, 250)
        self.panel(im, (90, 950, 990, 1600), ease((t - st[0]) / .4))
        paste_anim(im, self.NAME, 1010, st[0], t, pop=True); paste_anim(im, self.SUB, 1120, st[0] + 0.4, t)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(ov); f = F("Bold", 40); fs = F("ExtraBold", 40)
        for i, (lab, v) in enumerate(self.c["stats"]):
            p = ease((t - st[min(i + 1, len(st) - 1)] - (0 if i + 1 < len(st) else 0.4 * (i + 2 - len(st)))) / .45)
            if p <= 0: continue
            y = 1240 + i * 70; a = int(255 * p)
            dr.text((150, y), lab, font=f, fill=(255, 255, 255, a), anchor="lm")
            x0, x1 = 470, 820
            dr.rounded_rectangle([x0, y - 13, x1, y + 13], radius=13, fill=(255, 255, 255, int(55 * p)))
            dr.rounded_rectangle([x0, y - 13, max(x0 + 26, x0 + (x1 - x0) * v / 10 * p), y + 13], radius=13, fill=self.c["accent"] + (a,))
            dr.text((930, y), f"{v}/10", font=fs, fill=(255, 255, 255, a), anchor="rm")
        im.alpha_composite(ov); return im

    def s3(self, t):
        d = self.DUR["s3"]; im = self.bg(t, d, 0.97, 1.08); self.shade(im, 0.6, 1.0, 0.42); st = self.TM["s3"]
        tn = st[self.c["notif_line"]]
        if t > tn:
            p = back((t - tn) / .45); ny = self.c.get('notif_y'); im.alpha_composite(self.NOTIF, ((W - 900) // 2, int(-220 + p * (690 if self.c.get('hud') else 500)) if ny is None else int(ny - (1 - min(1, p)) * 160)))  # notif_y: keep the face clear (Nov 24)
        if self.c.get("conflict") and any(self.c["conflict"]):  # "conflict": null -> no text panel (it fought the word captions, Nov 21)
            self.panel(im, (80, 1085, 1000, 1430), ease((t - st[self.c["conflict_lines"][0]]) / .4))
            paste_anim(im, self.L3a, 1150, st[self.c["conflict_lines"][0]], t, pop=True)
            paste_anim(im, self.L3b, 1270, st[self.c["conflict_lines"][1]], t)
        return im

    def s4(self, t):
        d = self.DUR["s4"]; im = self.bg(t, d, 1.10, 1.18, self.BLUR); st = self.TM["s4"]
        if self.c.get("snow"): snow(im, t + 9, 110)
        paste_anim(im, self.L4a, 520, st[0], t, pop=True)
        paste_anim(im, self.L4b, 900, st[1], t); paste_anim(im, self.L4c, 1030, st[2], t)
        return im

    def s5(self, t):
        d = self.DUR["s5"]; im = self.bg(t, d, 1.18, 1.24, self.BLUR); st = self.TM["s5"]
        if self.c.get("snow"): snow(im, t + 14, 100)
        center_paste(im, self.pill, 250); paste_anim(im, self.L5a, 330, st[0], t, pop=True)
        opt_t = st[1]; span = (st[2] - st[1]) * 0.85
        for i, r in enumerate(self.ROWS):
            p = ease((t - opt_t - i * span / len(self.ROWS)) / .35)
            if p <= 0: continue
            a = np.array(r); a[..., 3] = (a[..., 3] * p).astype(np.uint8)
            im.alpha_composite(Image.fromarray(a), (int((W - 820) // 2 - (1 - p) * 120), 590 + i * 152))
        paste_anim(im, self.L5b, 1365, st[2], t); tp = st[2] + 0.3
        if t > tp: center_paste(im, self.POINT, 1520 + math.sin((t - tp) * 6) * 14, ease((t - tp) / .3))
        return im

    def render(self, stills=False):
        self.build_layers(); self.build_extras()
        scenes = [(n, (lambda f, n: (lambda t: (self._set_beat(n, t), self.overlay(n, t, f(t)))[1]))(getattr(self, n), n)) for n in self.order]
        if stills:
            pts = [(n, self.DUR[n] - 0.6) for n in self.order]
            for n in self.order:
                pts += [(n, t0 + 0.5) for _, t0 in self.sfx_times(n)]
                pts += [(n, (a + b) / 2) for a, b, _ in self.CAP.get(n, [])[:1]]
                pts += [(n, self.line_t(sc, ln) + dl + 0.4) for sc, ln, dl, _ in getattr(self, "_BEATS", []) if sc == n]
            pts.sort(key=lambda x: (self.order.index(x[0]), x[1]))
            fs = [dict(scenes)[n](min(t, self.DUR[n] - 0.05)).convert("RGB").resize((360, 640)) for n, t in pts]
            cols = 6; rows = (len(fs) + cols - 1) // cols
            c = Image.new("RGB", (360 * cols, 640 * rows)); [c.paste(x, ((i % cols) * 360, (i // cols) * 640)) for i, x in enumerate(fs)]
            c.save(f"{self.out}/contact.jpg", quality=85); return
        for n, fn in scenes:
            dur = self.DUR[n]; tmp = f"{self.out}/{n}.tmp.mp4"; N = int(round(dur * FPS))
            p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                                  "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
            for i in range(N):
                t = i / FPS; fr = fn(t).convert("RGB")
                fo = min(1, (t + 1 / FPS) / 0.1, (dur - t) / 0.1)
                if fo < 1 and n != "s1": fr = Image.blend(Image.new("RGB", (W, H)), fr, max(0, fo))
                p.stdin.write(fr.tobytes())
            p.stdin.close()
            if p.wait() != 0: sys.exit("render failed " + n)
            os.replace(tmp, f"{self.out}/{n}.mp4")
        open(f"{self.out}/list.txt", "w").write("".join(f"file '{n}.mp4'\n" for n, _ in scenes))
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-i", f"{self.out}/list.txt", "-c", "copy", f"{self.out}/v.mp4"])
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{self.out}/v.mp4", "-i", f"{self.out}/mix.wav", "-map", "0:v", "-map", "1:a",
                               "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-shortest", "-movflags", "+faststart", f"{self.out}/final.mp4"])
        cov_t = self.DUR[self.order[0]] + self.DUR[self.order[1]] - 0.5
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(cov_t), "-i", f"{self.out}/final.mp4", "-frames:v", "1", "-q:v", "2", f"{self.out}/cover.jpg"])
        self.make_cover()
