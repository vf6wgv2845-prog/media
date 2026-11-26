"""Overlay the REAL IntelliStudy capture (cap.json from cap_dNN.py) as Kai's phone screen onto a rendered episode.
Usage: python3 phone_overlay.py CAPDIR EPISODE_DIR OUT.mp4 SCENE LINE  (phone shows from that script line to the end of that scene)
Real generation time is shown with a live timer (measured, not sped up)."""
import json, sys, os, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont
cap, epd, out, scene, line = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
FD = '/usr/share/fonts/opentype/inter/'
def F(w, s): return ImageFont.truetype(FD + f'Inter-{w}.otf', s)
W, H, FPS = 1080, 1920, 30
tm = json.load(open(f'{epd}/timing.json')); order = ["s1", "sc", "s3", "sv"]
off = 0
for n in order:
    if n == scene: break
    off += tm['DUR'][n]
t0 = off + tm['TM'][scene][line]; t1 = off + tm['DUR'][scene] - 0.1
j = json.load(open(f'{cap}/cap.json')); fr = j['frames']; gen = j['gen_seconds']
typed = [f for f in fr if f[2] == 'typed'][0][0]; btn = [f for f in fr if f[2] == 'btn'][0][0]
waits = [f[0] for f in fr if f[2] == 'wait']; scrolls = [f[0] for f in fr if f[2] == 'scroll']; last = fr[-1][0]
seq = [(typed, 0.35), (btn, 0.25)] + [(w, gen / len(waits)) for w in waits]
t_cards = sum(d for _, d in seq)
scr = scrolls[len(scrolls) // 2 - 6:]  # from where the cards come into view
seq += [(s, 0.055) for s in scr]
D = t1 - t0; seq.append((last, max(0.5, D - sum(d for _, d in seq))))
PW, PH = 600, 1067; PX, PY = (W - PW) // 2, 385; B = 18
mask = Image.new('L', (PW, PH), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, PW - 1, PH - 1], 44, fill=255)
body = Image.new('RGBA', (W, H), (14, 10, 30, 205)); d = ImageDraw.Draw(body)
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([PX - B, PY - B + 20, PX + PW + B, PY + PH + B + 20], 64, fill=(0, 0, 0, 150)); sh = sh.filter(ImageFilter.GaussianBlur(22))
body.alpha_composite(sh); d.rounded_rectangle([PX - B, PY - B, PX + PW + B, PY + PH + B], 62, fill=(31, 27, 45, 255))
def label(im, txt, y, bg, fg=(15, 15, 15), size=66, ang=-3):
    f = F('ExtraBold', size); tw = int(ImageDraw.Draw(im).textlength(txt, font=f))
    s = Image.new('RGBA', (tw + 60, size + 44), (0, 0, 0, 0)); dd = ImageDraw.Draw(s); dd.rounded_rectangle([0, 0, tw + 59, size + 43], 18, fill=bg + (255,)); dd.text((30, 14), txt, font=f, fill=fg)
    s = s.rotate(ang, expand=True, resample=Image.BICUBIC); im.alpha_composite(s, ((W - s.width) // 2, y))
os.makedirs('/tmp/ph', exist_ok=True); [os.remove('/tmp/ph/' + x) for x in os.listdir('/tmp/ph')]
cache = {}
N = int(D * FPS)
for i in range(N):
    t = i / FPS; acc = 0; path = seq[-1][0]
    for p, dur in seq:
        if t < acc + dur: path = p; break
        acc += dur
    if path not in cache: cache[path] = Image.open(f'{cap}/{os.path.basename(path)}' if not os.path.exists(path) else path).convert('RGB').resize((PW, PH), Image.LANCZOS)
    im = body.copy(); im.paste(cache[path], (PX, PY), mask)
    pop = min(1, t / 0.2); 
    if t < 0.6: label(im, "REAL APP · KAI'S NOTES", 1500, (120, 225, 120), size=58)
    elif t < t_cards: label(im, f"{min(t - 0.6, gen):.1f} s", 1500, (235, 80, 95), (255, 255, 255), size=90, ang=3)
    else: label(im, f"3 CARDS · {gen:.1f} s", 1500, (255, 214, 102), size=80)
    if False: im = im.resize((int(W * (0.8 + 0.2 * pop)), int(H * (0.8 + 0.2 * pop)))); bg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bg.alpha_composite(im, ((W - im.width) // 2, (H - im.height) // 2)); im = bg
    im.save(f'/tmp/ph/{i:04d}.png')
subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{epd}/final.mp4', '-framerate', str(FPS), '-itsoffset', f'{t0:.3f}', '-i', '/tmp/ph/%04d.png',
    '-filter_complex', '[0:v][1:v]overlay=0:0:eof_action=pass[v]', '-map', '[v]', '-map', '0:a', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', out])
print('phone', round(t0, 2), '->', round(t1, 2), 'gen', round(gen, 2))
