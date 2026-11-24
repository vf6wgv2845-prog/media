"""Original flat-vector cartoon characters + rooms, drawn as SVG and rendered with the pre-installed Chromium.
Made Nov 21 so Jess and Danny exist without Leonardo, and so characters can VISIBLY change every day
(hair, outfit, skin, expression, props are parameters) - the #1 thing @30daystofix has that we didn't.

Usage:  python3 -I pipeline/toon.py spec.json      -> writes spec["out"] (PNG, 1080x1920)
spec = {"out": "pipeline/assets/jess.png", "who": "jess" | "danny", "scene": "jess_bedroom" | "danny_bedroom" | "plain",
        "look": {...overrides of the character's defaults below...},
        "extra": "<optional raw SVG drawn over the character, e.g. a prop>"}
Style: thick dark outlines, flat colours, big heads. Our own design: do not copy any other account's character."""
import sys, os, json, math

INK = "#1f1b2d"

def _eye(cx, cy, look, flip=1):
    tired = look.get("tired", 0)
    s = f'<ellipse cx="{cx}" cy="{cy}" rx="34" ry="{38 - 10 * tired}" fill="#fff" stroke="{INK}" stroke-width="6"/>'
    px = cx + look.get("gaze", 0) * 8
    s += f'<circle cx="{px}" cy="{cy + 4}" r="15" fill="{look.get("eye", "#4a3426")}"/><circle cx="{px - 5}" cy="{cy - 2}" r="5" fill="#fff"/>'
    if tired:  # heavy lids + bags
        s += f'<path d="M{cx - 36} {cy - 6 - 14 * (1 - tired)} Q{cx} {cy - 26 - 10 * (1 - tired)} {cx + 36} {cy - 6 - 14 * (1 - tired)} L{cx + 36} {cy - 44} L{cx - 36} {cy - 44} Z" fill="{look["skin"]}" stroke="none"/>'
        s += f'<path d="M{cx - 36} {cy - 6 - 14 * (1 - tired)} Q{cx} {cy - 26 - 10 * (1 - tired)} {cx + 36} {cy - 6 - 14 * (1 - tired)}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
        s += f'<path d="M{cx - 26} {cy + 46} Q{cx} {cy + 58} {cx + 26} {cy + 46}" fill="none" stroke="#9b6fa0" stroke-width="7" stroke-linecap="round" opacity=".8"/>'
    if look.get("bags") and not tired:
        s += f'<path d="M{cx - 26} {cy + 46} Q{cx} {cy + 58} {cx + 26} {cy + 46}" fill="none" stroke="#9b6fa0" stroke-width="7" stroke-linecap="round" opacity=".8"/>'
    return s

def _brow(cx, cy, tilt, color):
    return f'<path d="M{cx - 38} {cy + tilt} Q{cx} {cy - 14} {cx + 38} {cy - tilt}" fill="none" stroke="{color}" stroke-width="14" stroke-linecap="round"/>'

MOUTHS = {
    "flat": lambda x, y: f'<path d="M{x - 40} {y} Q{x} {y + 8} {x + 40} {y}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>',
    "sad": lambda x, y: f'<path d="M{x - 42} {y + 10} Q{x} {y - 16} {x + 42} {y + 10}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>',
    "smirk": lambda x, y: f'<path d="M{x - 40} {y + 4} Q{x + 6} {y + 16} {x + 44} {y - 10}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>',
    "smile": lambda x, y: f'<path d="M{x - 52} {y - 6} Q{x} {y + 50} {x + 52} {y - 6} Z" fill="#7a2230" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/><path d="M{x - 40} {y} Q{x} {y + 12} {x + 40} {y}" fill="#fff"/>',
    "grin": lambda x, y: f'<path d="M{x - 70} {y - 10} Q{x} {y + 56} {x + 70} {y - 10} Z" fill="#fff" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
                         + "".join(f'<line x1="{x + k}" y1="{y - 8}" x2="{x + k}" y2="{y + 26 - abs(k) // 4}" stroke="{INK}" stroke-width="4"/>' for k in (-42, -14, 14, 42)),
    "shock": lambda x, y: f'<ellipse cx="{x}" cy="{y + 12}" rx="30" ry="38" fill="#7a2230" stroke="{INK}" stroke-width="6"/>',
}

# ------------------------------------------------------------------ characters
JESS = dict(skin="#f2c3a0", blush="#ec8f8f", hair="#5a3324", hair_style="bun_bangs", eye="#3d6b4f", tired=0, bags=True, brow_tilt=14, brow_y=-58,
            mouth="sad", top="hoodie", top_color="#9a9ca6", top_dark="#7d7f8a", pants="#3a4a6b", spots=0, phone=True, sweat=False,
            lashes=True, earrings=False, makeup=0)
DANNY = dict(skin="#e9b48c", blush="#e08a7a", hair="#3b2a20", hair_style="messy_short", eye="#4a3426", tired=0, brow_tilt=-10,
             mouth="grin", top="polo", top_color="#2f9e8f", top_dark="#23786d", pants="#4b4f5c", spots=0, phone=True, sweat=True,
             beard="patchy", belly=1, nametag="DANNY", lashes=False, earrings=False, makeup=0)

def character(who, look_over=None):
    look = dict(JESS if who == "jess" else DANNY); look.update(look_over or {})
    hx, hy = 540, 900; wide = 1.08 if who == "danny" else 1.0
    rx, ry = int(215 * wide), 235
    g = []
    # ---- body
    belly = look.get("belly", 0)
    if look["top"] == "hoodie":
        g.append(f'<path d="M300 1920 L318 1300 Q330 1150 540 1130 Q750 1150 762 1300 L780 1920 Z" fill="{look["top_color"]}" stroke="{INK}" stroke-width="8"/>')
        g.append(f'<path d="M380 1150 Q540 1250 700 1150 Q690 1080 540 1070 Q390 1080 380 1150 Z" fill="{look["top_dark"]}" stroke="{INK}" stroke-width="7"/>')
        g.append(f'<line x1="500" y1="1200" x2="490" y2="1330" stroke="#e8e8ee" stroke-width="7" stroke-linecap="round"/><line x1="580" y1="1200" x2="590" y2="1330" stroke="#e8e8ee" stroke-width="7" stroke-linecap="round"/>')
        g.append(f'<path d="M410 1560 L670 1560 L640 1700 L440 1700 Z" fill="{look["top_dark"]}" stroke="{INK}" stroke-width="6"/>')
    elif look["top"] == "polo":
        bw = 40 * belly
        g.append(f'<path d="M{290 - bw} 1920 Q{270 - bw} 1550 {320} 1290 Q340 1160 540 1140 Q740 1160 760 1290 Q{810 + bw} 1550 {790 + bw} 1920 Z" fill="{look["top_color"]}" stroke="{INK}" stroke-width="8"/>')
        g.append(f'<path d="M440 1150 L540 1260 L640 1150 L600 1140 L540 1200 L480 1140 Z" fill="#fff" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
        g.append(f'<circle cx="540" cy="1290" r="9" fill="#fff" stroke="{INK}" stroke-width="4"/><circle cx="540" cy="1340" r="9" fill="#fff" stroke="{INK}" stroke-width="4"/>')
        if look.get("nametag"):
            g.append(f'<rect x="600" y="1310" width="150" height="70" rx="10" fill="#fff" stroke="{INK}" stroke-width="5"/><rect x="600" y="1310" width="150" height="22" rx="8" fill="#e5484d"/>'
                     f'<text x="675" y="1366" font-family="Inter" font-weight="900" font-size="28" text-anchor="middle" fill="{INK}">{look["nametag"]}</text>')
        if belly: g.append(f'<path d="M420 1700 Q540 1760 660 1700" fill="none" stroke="{look["top_dark"]}" stroke-width="10" stroke-linecap="round"/>')
    elif look["top"] == "dress":
        g.append(f'<path d="M360 1920 L400 1300 Q420 1170 540 1160 Q660 1170 680 1300 L720 1920 Z" fill="{look["top_color"]}" stroke="{INK}" stroke-width="8"/>')
        g.append(f'<path d="M430 1200 Q540 1260 650 1200" fill="none" stroke="{look["top_dark"]}" stroke-width="10"/>')
    else:  # tee / jacket generic
        g.append(f'<path d="M300 1920 L320 1290 Q340 1160 540 1140 Q740 1160 760 1290 L780 1920 Z" fill="{look["top_color"]}" stroke="{INK}" stroke-width="8"/>')
        g.append(f'<path d="M470 1150 Q540 1210 610 1150" fill="none" stroke="{INK}" stroke-width="7"/>')
    # neck
    g.append(f'<path d="M490 1080 L490 1150 Q540 1180 590 1150 L590 1080 Z" fill="{look["skin"]}" stroke="{INK}" stroke-width="7"/>')
    # arms + phone
    if look.get("phone"):
        g.append(f'<path d="M330 1330 Q300 1520 430 1560 L470 1520 Q390 1470 400 1340 Z" fill="{look["top_color"]}" stroke="{INK}" stroke-width="7"/>')
        g.append(f'<rect x="450" y="1430" width="110" height="180" rx="16" fill="#26232f" stroke="{INK}" stroke-width="6" transform="rotate(-12 505 1520)"/>'
                 f'<rect x="460" y="1444" width="90" height="150" rx="10" fill="#7fd0ff" transform="rotate(-12 505 1520)"/>')
        g.append(f'<ellipse cx="455" cy="1555" rx="42" ry="36" fill="{look["skin"]}" stroke="{INK}" stroke-width="6"/>')
    # ---- back hair
    hs = look["hair_style"]
    if hs == "bun_bangs":
        g.append(f'<path d="M{hx - rx - 10} {hy - 40} Q{hx - rx - 30} {hy + 80} {hx - rx + 10} {hy + 170} L{hx - rx + 40} {hy + 60} Z" fill="{look["hair"]}" stroke="{INK}" stroke-width="7"/><path d="M{hx + rx + 10} {hy - 40} Q{hx + rx + 30} {hy + 80} {hx + rx - 10} {hy + 170} L{hx + rx - 40} {hy + 60} Z" fill="{look["hair"]}" stroke="{INK}" stroke-width="7"/>')
    elif hs == "long_waves":
        g.append(f'<path d="M{hx - rx - 40} {hy + 300} Q{hx - rx - 80} {hy - ry} {hx} {hy - ry - 40} Q{hx + rx + 80} {hy - ry} {hx + rx + 40} {hy + 300} Q{hx} {hy + 340} {hx - rx - 40} {hy + 300} Z" fill="{look["hair"]}" stroke="{INK}" stroke-width="8"/>')
    # ears + head
    g.append(f'<ellipse cx="{hx - rx + 4}" cy="{hy + 20}" rx="34" ry="44" fill="{look["skin"]}" stroke="{INK}" stroke-width="7"/><ellipse cx="{hx + rx - 4}" cy="{hy + 20}" rx="34" ry="44" fill="{look["skin"]}" stroke="{INK}" stroke-width="7"/>')
    if look.get("earrings"):
        g.append(f'<circle cx="{hx - rx}" cy="{hy + 72}" r="12" fill="#f6c945" stroke="{INK}" stroke-width="4"/><circle cx="{hx + rx}" cy="{hy + 72}" r="12" fill="#f6c945" stroke="{INK}" stroke-width="4"/>')
    jaw = 30 if who == "danny" else 0
    g.append(f'<path d="M{hx - rx} {hy - 30} Q{hx - rx} {hy - ry} {hx} {hy - ry} Q{hx + rx} {hy - ry} {hx + rx} {hy - 30} Q{hx + rx + jaw // 2} {hy + ry - 40} {hx} {hy + ry + jaw // 2} Q{hx - rx - jaw // 2} {hy + ry - 40} {hx - rx} {hy - 30} Z" fill="{look["skin"]}" stroke="{INK}" stroke-width="8"/>')
    # beard
    if look.get("beard") == "patchy":
        import random; r = random.Random(7)
        for _ in range(70):
            a = r.uniform(0.15, 0.85) * math.pi; d = r.uniform(0.62, 0.95)
            x = hx + math.cos(a) * rx * d * 0.95; y = hy + 40 + math.sin(a) * (ry - 20) * d
            if r.random() < 0.25: continue
            g.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(3, 7):.1f}" fill="#4a3628" opacity=".75"/>')
    elif look.get("beard") == "trimmed":
        g.append(f'<path d="M{hx - rx + 20} {hy + 40} Q{hx - rx + 30} {hy + ry + 10} {hx} {hy + ry + 26} Q{hx + rx - 30} {hy + ry + 10} {hx + rx - 20} {hy + 40} Q{hx + 60} {hy + 150} {hx} {hy + 150} Q{hx - 60} {hy + 150} {hx - rx + 20} {hy + 40} Z" fill="#3b2a20" opacity=".9"/>')
    # spots
    import random; r2 = random.Random(3)
    for _ in range(int(look.get("spots", 0))):
        x = hx + r2.uniform(-rx * 0.7, rx * 0.7); y = hy + r2.uniform(-ry * 0.5, ry * 0.6)
        g.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r2.uniform(6, 11):.0f}" fill="#e2706a" stroke="#b9504c" stroke-width="2"/>')
    # blush
    g.append(f'<ellipse cx="{hx - 110}" cy="{hy + 70}" rx="38" ry="22" fill="{look["blush"]}" opacity=".45"/><ellipse cx="{hx + 110}" cy="{hy + 70}" rx="38" ry="22" fill="{look["blush"]}" opacity=".45"/>')
    # eyes, brows, lashes, makeup
    g.append(_eye(hx - 82, hy - 10, look) + _eye(hx + 82, hy - 10, look))
    if look.get("makeup"):
        g.append(f'<path d="M{hx - 112} {hy - 34} Q{hx - 75} {hy - 64} {hx - 38} {hy - 34}" fill="none" stroke="#c46a9a" stroke-width="8" opacity=".6"/><path d="M{hx + 38} {hy - 34} Q{hx + 75} {hy - 64} {hx + 112} {hy - 34}" fill="none" stroke="#c46a9a" stroke-width="8" opacity=".6"/>')
    if look.get("lashes"):
        for cx in (hx - 75, hx + 75):
            sgn = -1 if cx < hx else 1
            g.append(f'<path d="M{cx + sgn * 30} {hy - 34} l{sgn * 16} -12" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    bt = look.get("brow_tilt", 0)
    by = hy + look.get("brow_y", -80)
    g.append(_brow(hx - 82, by, -bt, look.get("brow", look["hair"])) + _brow(hx + 82, by, bt, look.get("brow", look["hair"])))
    # nose + mouth
    g.append(f'<path d="M{hx - 6} {hy + 30} Q{hx - 22} {hy + 70} {hx + 4} {hy + 76}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    g.append(MOUTHS[look.get("mouth", "flat")](hx, hy + 128))
    # front hair
    if hs == "bun_bangs":
        g.append(f'<circle cx="{hx + 20}" cy="{hy - ry - 60}" r="78" fill="{look["hair"]}" stroke="{INK}" stroke-width="8"/>')
        g.append(f'<path d="M{hx + 60} {hy - ry - 120} q30 -40 50 -10 M{hx - 40} {hy - ry - 110} q-30 -30 -50 5" fill="none" stroke="{look["hair"]}" stroke-width="10" stroke-linecap="round"/>')
        pts = []
        for i in range(9):
            x = hx - rx + 10 + i * (2 * rx - 20) / 8; pts.append(f'{x:.0f},{hy - 70 + look.get("bangs", 0) + (28 if i % 2 else 0) + (12 if i in (3, 6) else 0) + (look.get("bangs_jag", 0) * ((i * 7) % 3 - 1))}')
        g.append(f'<path d="M{hx - rx - 5} {hy - 40} Q{hx - rx} {hy - ry - 20} {hx} {hy - ry - 18} Q{hx + rx} {hy - ry - 20} {hx + rx + 5} {hy - 40} L{" L".join(reversed(pts))} Z" fill="{look["hair"]}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
    elif hs == "long_waves":
        g.append(f'<path d="M{hx - rx - 10} {hy - 10} Q{hx - rx} {hy - ry - 30} {hx + 20} {hy - ry - 25} Q{hx + rx + 10} {hy - ry - 10} {hx + rx + 10} {hy - 10} Q{hx + 60} {hy - 120} {hx - 40} {hy - 150} Q{hx - 120} {hy - 120} {hx - rx - 10} {hy - 10} Z" fill="{look["hair"]}" stroke="{INK}" stroke-width="8"/>')
    elif hs == "messy_short":
        spikes = " ".join(f'L{hx - rx + i * (2 * rx) / 10:.0f},{hy - ry - (40 if i % 2 else 5)}' for i in range(11))
        g.append(f'<path d="M{hx - rx - 8} {hy - 50} {spikes} L{hx + rx + 8} {hy - 50} Q{hx + 40} {hy - ry + 30} {hx - rx - 8} {hy - 50} Z" fill="{look["hair"]}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
    elif hs == "fade":
        g.append(f'<path d="M{hx - rx + 5} {hy - 60} Q{hx - rx + 10} {hy - ry - 30} {hx} {hy - ry - 32} Q{hx + rx - 10} {hy - ry - 30} {hx + rx - 5} {hy - 60} Q{hx + 60} {hy - ry + 30} {hx - 20} {hy - ry + 36} Q{hx - 100} {hy - ry + 40} {hx - rx + 5} {hy - 60} Z" fill="{look["hair"]}" stroke="{INK}" stroke-width="8"/>')
    if look.get("sweat"):
        g.append(f'<path d="M{hx + rx - 30} {hy - 120} q-22 40 0 52 q22 -12 0 -52 Z" fill="#8fd3ff" stroke="{INK}" stroke-width="5"/>')
    return "\n".join(g)

# ------------------------------------------------------------------ rooms
def scene(name):
    if name == "jess_bedroom":
        return f'''<rect width="1080" height="1920" fill="#f3d9e3"/><rect y="1380" width="1080" height="540" fill="#c9a28a"/>
<rect x="0" y="1360" width="1080" height="30" fill="#b48a72"/>
<rect x="640" y="250" width="340" height="300" rx="10" fill="#bfe3f5" stroke="{INK}" stroke-width="8"/><line x1="810" y1="250" x2="810" y2="550" stroke="{INK}" stroke-width="8"/><line x1="640" y1="400" x2="980" y2="400" stroke="{INK}" stroke-width="8"/>
<path d="M120 300 L120 1250" stroke="#8a6d5b" stroke-width="10"/><path d="M60 300 L180 300" stroke="{INK}" stroke-width="8"/>
<path d="M120 300 L70 360 L60 1180 Q120 1230 180 1180 L170 360 Z" fill="#d9e8f5" stroke="{INK}" stroke-width="7" opacity=".95"/>
<path d="M85 420 Q120 460 155 420 L165 1150 Q120 1190 75 1150 Z" fill="#f2a7c3" stroke="{INK}" stroke-width="5"/>
<text x="120" y="1250" font-family="Inter" font-weight="900" font-size="30" text-anchor="middle" fill="{INK}">BRIDESMAID</text>
<rect x="700" y="1250" width="380" height="300" rx="30" fill="#ffffff" stroke="{INK}" stroke-width="8"/><rect x="700" y="1210" width="380" height="90" rx="30" fill="#f7b6cd" stroke="{INK}" stroke-width="8"/>
<rect x="130" y="1560" width="170" height="34" rx="8" fill="#6c63ff" stroke="{INK}" stroke-width="5"/><rect x="140" y="1528" width="150" height="34" rx="8" fill="#ffb703" stroke="{INK}" stroke-width="5"/><text x="215" y="1556" font-family="Inter" font-weight="900" font-size="20" text-anchor="middle" fill="{INK}">ICE CREAM</text>'''
    if name == "danny_bedroom":
        return f'''<rect width="1080" height="1920" fill="#c9d6e8"/><rect y="1380" width="1080" height="540" fill="#8d7a6a"/>
<rect x="0" y="1360" width="1080" height="30" fill="#76655a"/>
<rect x="80" y="260" width="220" height="300" fill="#e5484d" stroke="{INK}" stroke-width="7" transform="rotate(-4 190 410)"/><text x="190" y="420" font-family="Inter" font-weight="900" font-size="44" text-anchor="middle" fill="#fff" transform="rotate(-4 190 410)">CLASS</text><text x="190" y="470" font-family="Inter" font-weight="900" font-size="44" text-anchor="middle" fill="#fff" transform="rotate(-4 190 410)">OF 2016</text>
<rect x="780" y="240" width="230" height="320" fill="#ffd166" stroke="{INK}" stroke-width="7" transform="rotate(5 895 400)"/><circle cx="895" cy="360" r="70" fill="#f4a261" stroke="{INK}" stroke-width="6" transform="rotate(5 895 400)"/><text x="895" y="510" font-family="Inter" font-weight="900" font-size="36" text-anchor="middle" fill="{INK}" transform="rotate(5 895 400)">DREAM BIG</text>
<rect x="700" y="1230" width="380" height="330" rx="20" fill="#3d5a80" stroke="{INK}" stroke-width="8"/><rect x="700" y="1200" width="380" height="70" rx="20" fill="#98c1d9" stroke="{INK}" stroke-width="8"/>
<rect x="40" y="1320" width="220" height="240" rx="10" fill="#a7825f" stroke="{INK}" stroke-width="7"/><rect x="70" y="1250" width="160" height="80" rx="8" fill="#2b2d42" stroke="{INK}" stroke-width="6"/><rect x="82" y="1262" width="136" height="56" fill="#8ecae6"/>'''
    return '<rect width="1080" height="1920" fill="#e9e3f5"/>'

def svg(spec):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
<defs><radialGradient id="vg" cx="50%" cy="45%" r="75%"><stop offset="60%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#000" stop-opacity=".28"/></radialGradient></defs>
{scene(spec.get("scene", "plain"))}
<ellipse cx="540" cy="1900" rx="330" ry="40" fill="#000" opacity=".12"/>
{character(spec["who"], spec.get("look"))}
{spec.get("extra", "")}
<rect width="1080" height="1920" fill="url(#vg)"/></svg>'''

def render(spec):
    from playwright.sync_api import sync_playwright
    html = f'<html><body style="margin:0;background:#000">{svg(spec)}</body></html>'
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        pg.set_content(html); pg.screenshot(path=spec["out"], clip={"x": 0, "y": 0, "width": 1080, "height": 1920}); b.close()
    print(spec["out"])

if __name__ == "__main__":
    render(json.load(open(sys.argv[1])))
