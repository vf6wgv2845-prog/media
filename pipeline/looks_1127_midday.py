"""Nov 27 midday extras: toon looks for Malik (sneaker store), Rosie (ketchup trap), Wes (rehearsing to a trash can)
and Gus History #7 (Black Friday origin). Run: python3 -I pipeline/looks_1127_midday.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import props
from props import phone, sign, burst, chip, INK
from PIL import Image, ImageDraw, ImageFont, ImageFilter
A = os.path.join(HERE, "assets")

def sneaker(x, y, s=1.0, angle=0, color="#e5484d", lace=True, stretch=1.0):
    sx = s * stretch
    g = f'<g transform="translate({x} {y}) rotate({angle}) scale({sx} {s})">'
    g += f'<path d="M-130 30 Q-135 -40 -70 -50 L-10 -60 Q30 -20 90 -10 Q140 0 140 40 L140 55 L-130 55 Z" fill="{color}" stroke="{INK}" stroke-width="7"/>'
    g += f'<rect x="-135" y="40" width="280" height="26" rx="10" fill="#fff" stroke="{INK}" stroke-width="6"/>'
    g += f'<path d="M-40 -10 Q20 20 80 10" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round"/>'
    if lace:
        for k in range(3):
            g += f'<line x1="{-60 + k * 22}" y1="{-48 + k * 4}" x2="{-40 + k * 22}" y2="{-30 + k * 4}" stroke="#fff" stroke-width="6"/>'
    return g + '</g>'

def ketchup(x, y, s=1.0, angle=-8):
    return (f'<g transform="translate({x} {y}) rotate({angle}) scale({s})"><rect x="-55" y="-150" width="110" height="260" rx="40" fill="#d62828" stroke="{INK}" stroke-width="7"/>'
            f'<rect x="-30" y="-200" width="60" height="60" rx="10" fill="#fff" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="-48" y="-60" width="96" height="70" rx="8" fill="#fff8e7" stroke="{INK}" stroke-width="4"/>'
            f'<text x="0" y="-15" font-family="Inter" font-weight="900" font-size="22" text-anchor="middle" fill="#d62828">KETCHUP</text></g>')

def trashcan(x, y, s=1.0, talk=False):
    g = f'<g transform="translate({x} {y}) scale({s})">'
    g += f'<path d="M-110 -120 L110 -120 L90 160 L-90 160 Z" fill="#5f6b75" stroke="{INK}" stroke-width="7"/>'
    g += f'<rect x="-125" y="-150" width="250" height="40" rx="10" fill="#4b5560" stroke="{INK}" stroke-width="7"/>'
    for k in (-50, 0, 50):
        g += f'<line x1="{k}" y1="-90" x2="{k * 0.85}" y2="140" stroke="{INK}" stroke-width="4" opacity=".5"/>'
    g += '<g fill="#8fe36b" stroke="#1f1b2d" stroke-width="4"><circle cx="-40" cy="-30" r="24"/><circle cx="40" cy="-30" r="24"/></g>'
    g += '<g fill="#1f1b2d"><circle cx="-36" cy="-28" r="9"/><circle cx="44" cy="-28" r="9"/></g>'
    if talk:
        g += f'<ellipse cx="0" cy="50" rx="44" ry="30" fill="#7a2230" stroke="{INK}" stroke-width="5"/>'
    else:
        g += f'<path d="M-40 50 Q0 70 40 50" fill="none" stroke="{INK}" stroke-width="6"/>'
    # wrappers peeking out
    g += f'<path d="M-90 -150 L-60 -200 L-30 -150 Z" fill="#ffd166" stroke="{INK}" stroke-width="5"/><path d="M30 -150 L70 -195 L90 -150 Z" fill="#ef8354" stroke="{INK}" stroke-width="5"/>'
    return g + '</g>'

def bubble(x, y, text, size=46, w=None):
    return sign(x, y, [text], w=w, bg="#ffffff", fg=INK, size=size, angle=0, pad=18)

specs = []
# ---------------- Malik (shoestore)
specs += [
    {"out": f"{A}/malik_b1127_hook.jpg", "who": "malik", "scene": "shoestore", "look": {"mouth": "shock", "brow_tilt": 10, "sweat": True},
     "extra": sneaker(700, 1250, 1.1, -12)
              + sign(300, 1290, ["DEZ HAS", "THE LEFT"], bg="#e5484d", fg="#fff", size=40, angle=5)},
    {"out": f"{A}/malik_b1127_phone.jpg", "who": "malik", "scene": "shoestore", "look": {"mouth": "flat", "gaze": 1, "brow_tilt": -4},
     "extra": sneaker(330, 1300, 0.9, 8) + phone(700, 1180, ["are u and dez", "fighting over", "ONE shoe", "", "i'm behind u"], title="JADA", w=330, h=470, size=32, angle=-5)},
    {"out": f"{A}/malik_b1127_tug.jpg", "who": "malik", "scene": "shoestore", "look": {"mouth": "grin", "brow_tilt": -14, "sweat": True},
     "extra": sneaker(540, 1260, 1.1, 0, stretch=1.9) + burst(840, 1000, "RIIIP", r=120, size=50)},
    {"out": f"{A}/malik_b1127_lace.jpg", "who": "malik", "scene": "shoestore", "look": {"mouth": "sad", "brow_tilt": 12},
     "extra": sneaker(560, 1270, 1.0, -6, lace=False)
              + '<path d="M640 1210 Q700 1150 690 1080 Q680 1030 720 1000" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round"/><path d="M640 1210 Q700 1150 690 1080 Q680 1030 720 1000" fill="none" stroke="#1f1b2d" stroke-width="3" stroke-linecap="round"/>'
              + sign(300, 1330, ["ONE EACH.", "FULL PRICE."], bg="#fff8e7", fg="#c0504d", size=40, angle=3)},
    {"out": f"{A}/malik_b1127_two.jpg", "who": "malik", "scene": "shoestore", "look": {"mouth": "flat", "brow_tilt": 4, "gaze": -1},
     "extra": phone(360, 1200, ["sunday?"], title="JADA", w=270, h=300, size=38, angle=-8)
              + phone(720, 1200, ["film's up", "if u scared"], title="DEZ", w=270, h=300, size=34, angle=7, title_bg="#e5484d")},
]
# ---------------- Rosie (kitchen)
specs += [
    {"out": f"{A}/rosie_b1127_hook.jpg", "who": "rosie", "scene": "kitchen", "look": {"mouth": "smirk", "brow_tilt": -10, "gaze": 1},
     "extra": ketchup(720, 1230, 1.0) + bubble(540, 520, "MY SECRET? KETCHUP.", size=50)
              + sign(290, 1300, ["DISH PIT", "→"], bg="#2a9d8f", fg="#fff", size=40, angle=-5)},
    {"out": f"{A}/rosie_b1127_phone.jpg", "who": "rosie", "scene": "kitchen", "look": {"mouth": "shock", "brow_tilt": 12},
     "extra": phone(700, 1180, ["ketchup??", "in a cook-off??", "", "rosie. no."], title="JULIAN", w=330, h=440, size=34, angle=-5)
              + sign(300, 1300, ["4 MIN", "LATER"], bg="#1f1b2d", fg="#ffd166", size=42, angle=4)},
    {"out": f"{A}/rosie_b1127_turkey.jpg", "who": "rosie", "scene": "kitchen", "look": {"mouth": "flat", "brow_tilt": 6, "gaze": -1},
     "extra": props.turkey(380, 1300, 0.8) + phone(760, 1160, ["2 hours max.", "then the fridge.", "eat in 3-4 days."], title="JULIAN", w=320, h=400, size=30, angle=6)},
    {"out": f"{A}/rosie_b1127_marco.jpg", "who": "rosie", "scene": "kitchen", "look": {"mouth": "sad", "brow_tilt": 14, "sweat": True},
     "extra": sign(830, 1290, ["- MARCO"], bg="#fff8e7", fg=INK, size=38, angle=4)},
    {"out": f"{A}/rosie_b1127_apron.jpg", "who": "rosie", "scene": "kitchen", "look": {"mouth": "flat", "brow_tilt": -16, "gaze": 1},
     "extra": sign(390, 1330, ["APRON: OFF"], bg="#e5484d", fg="#fff", size=44, angle=-3)
              + phone(740, 1380, ["JULIAN (big bro):", "lol ketchup"], title="DISH PIT PHONE", w=330, h=300, size=28, angle=5, title_bg="#1f1b2d")},
]
# ---------------- Wes (street)
specs += [
    {"out": f"{A}/wes_b1127m_rehearse.jpg", "who": "wes", "scene": "street", "look": {"mouth": "flat", "brow_tilt": -12, "gaze": 1},
     "extra": trashcan(760, 1240, 1.1) + bubble(540, 470, "\"BROOKE... NO.\"", size=56)},
    {"out": f"{A}/wes_b1127m_can.jpg", "who": "wes", "scene": "street", "look": {"mouth": "shock", "brow_tilt": 14, "sweat": True},
     "extra": trashcan(760, 1240, 1.1, talk=True) + bubble(560, 470, "\"LET HER COME.\"", size=56)},
    {"out": f"{A}/wes_b1127m_phone.jpg", "who": "wes", "scene": "street", "look": {"mouth": "sad", "brow_tilt": 10},
     "extra": trashcan(300, 1300, 0.6) + phone(720, 1180, ["WHO ARE YOU", "TALKING TO.", "", "IS THAT THE", "TRASH CAN."], title="RANGER COLE", w=330, h=470, size=30, angle=-5, title_bg="#2a9d8f")},
    {"out": f"{A}/wes_b1127m_brooke.jpg", "who": "wes", "scene": "street", "look": {"mouth": "smile", "brow_tilt": 6, "gaze": 1},
     "extra": trashcan(300, 1300, 0.6) + phone(720, 1200, ["bringing snacks", "for the crew :)"], title="BROOKE", w=330, h=330, size=32, angle=5, title_bg="#e76fa0")},
]
props.render_many(specs)

# ---------------- Gus (History #7): paste the exhibit into his wall frame + full-screen exhibit beats
H = os.path.join(A, "history")
EX = {"police": ("whistler_policeman_1855.jpg", "James McNeill Whistler, Policeman and Citizen, 1854/55 (AIC)"),
      "street": ("caillebotte_paris_street_1877.jpg", "Gustave Caillebotte, Paris Street; Rainy Day, 1877 (AIC)"),
      "football": ("callot_football_1622.jpg", "Jacques Callot, Football Game in Florence, c. 1622 (AIC)")}

def font(sz, bold=True):
    for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
        if os.path.exists(f): return ImageFont.truetype(f, sz)
    return ImageFont.load_default()

def cover_fit(img, w, h):
    r = max(w / img.width, h / img.height); im = img.resize((int(img.width * r) + 1, int(img.height * r) + 1))
    l = (im.width - w) // 2; t = (im.height - h) // 2; return im.crop((l, t, l + w, t + h))

def in_frame(base, key, out):
    b = Image.open(os.path.join(A, base)).convert("RGB").resize((1080, 1920))
    art = Image.open(os.path.join(H, EX[key][0])).convert("RGB")
    b.paste(cover_fit(art, 290, 350), (735, 255)); b.save(out, quality=92); print(out)

def exhibit(key, out):
    art = Image.open(os.path.join(H, EX[key][0])).convert("RGB")
    bg = Image.new("RGB", (1080, 1920), (110, 110, 112))
    maxw, maxh = 880, 1000
    r = min(maxw / art.width, maxh / art.height); art = art.resize((int(art.width * r), int(art.height * r)))
    x = (1080 - art.width) // 2; y = 760 - art.height // 2 + 60
    sh = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    d.rectangle((x - 40, y - 40 + 30, x + art.width + 40, y + art.height + 40 + 30), fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(30)); bg = bg.convert("RGBA"); bg.alpha_composite(sh); bg = bg.convert("RGB")
    d = ImageDraw.Draw(bg)
    d.rectangle((x - 34, y - 34, x + art.width + 34, y + art.height + 34), fill=(31, 27, 45))
    d.rectangle((x - 28, y - 28, x + art.width + 28, y + art.height + 28), fill=(184, 137, 63))
    d.rectangle((x - 8, y - 8, x + art.width + 8, y + art.height + 8), fill=(244, 241, 222))
    bg.paste(art, (x, y))
    f = font(24); label = EX[key][1]; tw = d.textlength(label, font=f)
    ly = y + art.height + 70
    d.rounded_rectangle(((1080 - tw) / 2 - 18, ly - 10, (1080 + tw) / 2 + 18, ly + 40), 8, fill=(244, 241, 222), outline=(31, 27, 45), width=3)
    d.text(((1080 - tw) / 2, ly), label, font=f, fill=(31, 27, 45))
    bg.save(out, quality=92); print(out)

in_frame("gus_toon_point.jpg", "police", f"{A}/gus_e07_point_police.jpg")
in_frame("gus_toon_shock.jpg", "police", f"{A}/gus_e07_shock_police.jpg")
in_frame("gus_toon_phone.jpg", "street", f"{A}/gus_e07_phone.jpg")
in_frame("gus_toon_base.jpg", "football", f"{A}/gus_e07_base_football.jpg")
for k in EX: exhibit(k, f"{A}/gus_e07_ex_{k}.jpg")
# Gus holding the failed rebrand: a "BIG FRIDAY" sign, crossed out
props.overlay_many([{"base": f"{A}/gus_e07_base_football.jpg", "out": f"{A}/gus_e07_bigfriday.jpg",
                     "svg": sign(540, 1250, ["BIG FRIDAY"], bg="#fff8e7", fg="#2f6fb3", size=78, angle=-4)
                            + '<line x1="290" y1="1300" x2="790" y2="1190" stroke="#d62828" stroke-width="22" stroke-linecap="round"/>'
                            + chip(540, 1420, "1961: NOPE.", bg="#d62828", fg="#fff", size=48, angle=3)}])
props.strip([s["out"] for s in specs] + [f"{A}/gus_e07_{n}.jpg" for n in ("point_police", "ex_police", "ex_street", "ex_football", "phone", "bigfriday", "shock_police")],
            "/tmp/claude-0/looks_1127m.jpg", w=150)
