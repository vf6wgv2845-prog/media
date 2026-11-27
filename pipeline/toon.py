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
# Nov 25: Malik + Rosie redrawn in the toon style (Boris: they switch from 3D; Theo stays 3D), Wes = Trash Horde story lead.
MALIK = dict(skin="#8a5636", blush="#b5664f", hair="#1c1410", hair_style="locs", eye="#3b2418", tired=0, brow_tilt=-6, brow_y=-70,
             mouth="flat", top="jersey", top_color="#1f4fa3", top_dark="#173c7d", number="23", pants="#2b2f3a", spots=0, phone=False, sweat=False,
             lashes=False, earrings=False, makeup=0)
ROSIE = dict(skin="#d9a07a", blush="#e07a6a", hair="#2a1812", hair_style="curly_bun", bandana="#d63a3a", eye="#4a2c1c", tired=0, brow_tilt=8, brow_y=-62,
             mouth="smile", top="chef", top_color="#f7f4ee", top_dark="#dcd6cc", chef_name="Rosie", pants="#3a3f4b", spots=0, phone=False, sweat=False,
             lashes=True, earrings=False, makeup=0)
WES = dict(skin="#efc19c", blush="#e68f80", hair="#8a5a2b", hair_style="messy_short", eye="#3c5a7a", tired=0, brow_tilt=-8, brow_y=-70,
           mouth="flat", top="vest", top_color="#7d8796", top_dark="#5f6774", pants="#3b4150", spots=0, phone=False, sweat=False,
           lashes=False, earrings=False, makeup=0, gloves=True)
# Nov 25 night (Boris live, RUNBOOK 5m): recurring History host + the IntelliStudy student series lead.
GUS = dict(skin="#e8b896", blush="#d98a78", hair="#c9c9cf", hair_style="fade", eye="#3c4a5a", tired=0, brow_tilt=-4, brow_y=-72, brow="#9a9aa2",
           mouth="smirk", top="tee", top_color="#27365a", top_dark="#1c2742", pants="#2b2f3a", spots=0, phone=False, sweat=False,
           beard="trimmed", beard_color="#a9a9b0", lashes=False, earrings=False, makeup=0)
KAI = dict(skin="#d7a27c", blush="#d9826f", hair="#1b1512", hair_style="messy_short", eye="#3b2a1e", tired=0, brow_tilt=-6, brow_y=-70,
           mouth="flat", top="hoodie", top_color="#3f8f6b", top_dark="#2f6f52", pants="#3a4a6b", spots=1, phone=True, sweat=False,
           lashes=False, earrings=False, makeup=0)
CHARS = {"jess": JESS, "danny": DANNY, "malik": MALIK, "rosie": ROSIE, "wes": WES, "gus": GUS, "kai": KAI}

def character(who, look_over=None):
    look = dict(CHARS.get(who, DANNY)); look.update(look_over or {})
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
    elif look["top"] == "jersey":
        g.append(f'<path d="M330 1920 L345 1260 Q350 1170 430 1150 L470 1150 Q540 1230 610 1150 L650 1150 Q730 1170 735 1260 L750 1920 Z" fill="{look["top_color"]}" stroke="{INK}" stroke-width="8"/>')
        g.append(f'<path d="M300 1250 Q270 1400 330 1560 L345 1260 Z M780 1250 Q810 1400 750 1560 L735 1260 Z" fill="{look["skin"]}" stroke="{INK}" stroke-width="7"/>')
        g.append(f'<path d="M470 1150 Q540 1230 610 1150" fill="none" stroke="#fff" stroke-width="12"/>')
        g.append(f'<text x="540" y="1470" font-family="Inter" font-weight="900" font-size="190" text-anchor="middle" fill="#fff" stroke="{INK}" stroke-width="6">{look.get("number", "23")}</text>')
    elif look["top"] == "chef":
        g.append(f'<path d="M300 1920 L320 1290 Q340 1160 540 1140 Q740 1160 760 1290 L780 1920 Z" fill="{look["top_color"]}" stroke="{INK}" stroke-width="8"/>')
        g.append(f'<path d="M470 1145 L540 1300 L560 1920" fill="none" stroke="{look["top_dark"]}" stroke-width="8"/><rect x="455" y="1130" width="170" height="50" rx="20" fill="{look["top_color"]}" stroke="{INK}" stroke-width="7"/>')
        for yy in (1340, 1440, 1540):
            g.append(f'<circle cx="610" cy="{yy}" r="11" fill="{look["top_dark"]}" stroke="{INK}" stroke-width="4"/><circle cx="680" cy="{yy}" r="11" fill="{look["top_dark"]}" stroke="{INK}" stroke-width="4"/>')
        if look.get("chef_name"):
            g.append(f'<text x="420" y="1330" font-family="Inter" font-weight="900" font-style="italic" font-size="44" text-anchor="middle" fill="#c0392b">{look["chef_name"]}</text>')
    elif look["top"] == "vest":
        g.append(f'<path d="M300 1920 L320 1290 Q340 1160 540 1140 Q740 1160 760 1290 L780 1920 Z" fill="{look["top_color"]}" stroke="{INK}" stroke-width="8"/>')
        g.append(f'<path d="M360 1230 L470 1160 L520 1920 L370 1920 Z M720 1230 L610 1160 L560 1920 L710 1920 Z" fill="#ff8a1f" stroke="{INK}" stroke-width="7"/>')
        g.append(f'<rect x="375" y="1450" width="135" height="30" fill="#e8f060" stroke="{INK}" stroke-width="4"/><rect x="570" y="1450" width="135" height="30" fill="#e8f060" stroke="{INK}" stroke-width="4"/>')
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
    jaw = {"danny": 30, "malik": 18, "wes": 14}.get(who, 0)
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
        g.append(f'<path d="M{hx - rx + 20} {hy + 40} Q{hx - rx + 30} {hy + ry + 10} {hx} {hy + ry + 26} Q{hx + rx - 30} {hy + ry + 10} {hx + rx - 20} {hy + 40} Q{hx + 60} {hy + 150} {hx} {hy + 150} Q{hx - 60} {hy + 150} {hx - rx + 20} {hy + 40} Z" fill="{look.get('beard_color', '#3b2a20')}" opacity=".9"/>')
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
    elif hs == "locs":
        g.append(f'<path d="M{hx - rx + 5} {hy - 60} Q{hx - rx + 10} {hy - ry - 30} {hx} {hy - ry - 32} Q{hx + rx - 10} {hy - ry - 30} {hx + rx - 5} {hy - 60} Q{hx + 60} {hy - ry + 20} {hx - 20} {hy - ry + 26} Q{hx - 100} {hy - ry + 30} {hx - rx + 5} {hy - 60} Z" fill="{look["hair"]}" stroke="{INK}" stroke-width="8"/>')
        for i in range(13):
            x = hx - rx + 20 + i * (2 * rx - 40) / 12; top = hy - ry - 70 - (20 if i % 2 else 0)
            g.append(f'<rect x="{x - 15:.0f}" y="{top:.0f}" width="30" height="{110 + (i % 3) * 14}" rx="15" fill="{look["hair"]}" stroke="{INK}" stroke-width="5" transform="rotate({(i - 6) * 4} {x:.0f} {top + 60:.0f})"/>')
    elif hs == "curly_bun":
        g.append(f'<circle cx="{hx}" cy="{hy - ry - 70}" r="95" fill="{look["hair"]}" stroke="{INK}" stroke-width="8"/>')
        for i in range(9):
            x = hx - 70 + i * 18; g.append(f'<circle cx="{x}" cy="{hy - ry - 120 + (i % 2) * 14}" r="26" fill="{look["hair"]}" stroke="{INK}" stroke-width="4"/>')
        g.append(f'<path d="M{hx - rx - 5} {hy - 40} Q{hx - rx} {hy - ry - 20} {hx} {hy - ry - 18} Q{hx + rx} {hy - ry - 20} {hx + rx + 5} {hy - 40} Q{hx + 120} {hy - 150} {hx} {hy - 140} Q{hx - 120} {hy - 150} {hx - rx - 5} {hy - 40} Z" fill="{look["hair"]}" stroke="{INK}" stroke-width="8"/>')
        for x in (hx - rx + 10, hx + rx - 10):
            g.append(f'<circle cx="{x}" cy="{hy - 20}" r="34" fill="{look["hair"]}" stroke="{INK}" stroke-width="5"/>')
        if look.get("bandana"):
            g.append(f'<path d="M{hx - rx + 10} {hy - ry + 40} Q{hx} {hy - ry - 10} {hx + rx - 10} {hy - ry + 40} L{hx + rx - 20} {hy - ry + 85} Q{hx} {hy - ry + 35} {hx - rx + 20} {hy - ry + 85} Z" fill="{look["bandana"]}" stroke="{INK}" stroke-width="6"/>')
            g.append(f'<path d="M{hx + 20} {hy - ry - 5} q60 -70 100 -20 q-40 40 -100 20 Z M{hx + 20} {hy - ry - 5} q-30 -80 -90 -50 q20 50 90 50 Z" fill="{look["bandana"]}" stroke="{INK}" stroke-width="6"/>')
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
    if name == "kitchen":
        return f'''<rect width="1080" height="1920" fill="#f5e6c8"/><rect y="0" width="1080" height="260" fill="#cfd8dc"/>
<rect x="0" y="1380" width="1080" height="540" fill="#9aa5ae"/><rect x="0" y="1360" width="1080" height="34" fill="#7b868f"/>
<line x1="80" y1="300" x2="1000" y2="300" stroke="{INK}" stroke-width="8"/>
<circle cx="170" cy="380" r="60" fill="#d98c4a" stroke="{INK}" stroke-width="7"/><line x1="170" y1="300" x2="170" y2="320" stroke="{INK}" stroke-width="6"/>
<circle cx="910" cy="390" r="70" fill="#c07a3a" stroke="{INK}" stroke-width="7"/><line x1="910" y1="300" x2="910" y2="320" stroke="{INK}" stroke-width="6"/>
<rect x="760" y="520" width="90" height="120" fill="#fff" stroke="{INK}" stroke-width="5" transform="rotate(4 805 580)"/><rect x="870" y="520" width="90" height="120" fill="#fff" stroke="{INK}" stroke-width="5" transform="rotate(-3 915 580)"/>
<text x="805" y="590" font-family="Inter" font-weight="900" font-size="22" text-anchor="middle" fill="{INK}" transform="rotate(4 805 580)">TABLE 4</text><text x="915" y="590" font-family="Inter" font-weight="900" font-size="22" text-anchor="middle" fill="{INK}" transform="rotate(-3 915 580)">86 FISH</text>
<rect x="40" y="1230" width="300" height="140" rx="12" fill="#5f6b75" stroke="{INK}" stroke-width="7"/><ellipse cx="120" cy="1230" rx="60" ry="14" fill="#2b2b2b"/><ellipse cx="260" cy="1230" rx="60" ry="14" fill="#2b2b2b"/>'''
    if name == "gym":
        return f'''<rect width="1080" height="1920" fill="#e8d2a8"/><rect y="1380" width="1080" height="540" fill="#c98f4f"/>
<line x1="0" y1="1500" x2="1080" y2="1500" stroke="#fff" stroke-width="8" opacity=".7"/><path d="M200 1920 Q540 1560 880 1920" fill="none" stroke="#fff" stroke-width="8" opacity=".7"/>
<rect x="60" y="200" width="420" height="160" rx="8" fill="#1f4fa3" stroke="{INK}" stroke-width="7"/><text x="270" y="300" font-family="Inter" font-weight="900" font-size="64" text-anchor="middle" fill="#ffd166">EAGLES</text>
<rect x="760" y="240" width="220" height="140" fill="#fff" stroke="{INK}" stroke-width="7"/><rect x="830" y="300" width="80" height="60" fill="none" stroke="#e5484d" stroke-width="6"/>
<circle cx="870" cy="420" r="45" fill="none" stroke="#e5484d" stroke-width="8"/><path d="M830 430 L850 520 L890 520 L910 430" fill="none" stroke="#fff" stroke-width="4"/>
<rect x="0" y="560" width="1080" height="16" fill="#b07a40"/><rect x="0" y="700" width="1080" height="16" fill="#b07a40"/>'''
    if name == "street":
        return f'''<rect width="1080" height="1920" fill="#3d3566"/><rect y="1380" width="1080" height="540" fill="#4a4f57"/><rect y="1360" width="1080" height="30" fill="#6b717a"/>
<rect x="40" y="420" width="300" height="960" fill="#5a4f8a" stroke="{INK}" stroke-width="7"/><rect x="760" y="360" width="300" height="1020" fill="#4f467d" stroke="{INK}" stroke-width="7"/>
<rect x="90" y="500" width="80" height="90" fill="#ffd166"/><rect x="210" y="500" width="80" height="90" fill="#2b2650"/><rect x="90" y="660" width="80" height="90" fill="#2b2650"/><rect x="210" y="660" width="80" height="90" fill="#ffd166"/>
<rect x="810" y="440" width="80" height="90" fill="#ffd166"/><rect x="930" y="440" width="80" height="90" fill="#2b2650"/><rect x="810" y="600" width="80" height="90" fill="#2b2650"/><rect x="930" y="600" width="80" height="90" fill="#ffd166"/>
<circle cx="880" cy="180" r="70" fill="#f4f1de" opacity=".9"/><rect x="520" y="330" width="14" height="1050" fill="#2b2b2b"/><ellipse cx="527" cy="330" rx="60" ry="20" fill="#ffe08a"/>
<g fill="#8fe36b" stroke="{INK}" stroke-width="5"><circle cx="150" cy="1300" r="40"/><circle cx="950" cy="1290" r="46"/></g><g fill="#fff"><circle cx="138" cy="1292" r="9"/><circle cx="162" cy="1292" r="9"/><circle cx="937" cy="1282" r="10"/><circle cx="963" cy="1282" r="10"/></g>'''
    if name == "dining":  # Nov 26: family Thanksgiving dining room (Malik). Table is drawn in the look's "extra" so it sits in front.
        return f'''<rect width="1080" height="1920" fill="#f1dcc0"/><rect y="0" width="1080" height="120" fill="#d9bd98"/>
<rect x="0" y="1360" width="1080" height="560" fill="#8a5a3a"/>
<rect x="680" y="250" width="320" height="380" rx="10" fill="#cfe6f2" stroke="{INK}" stroke-width="8"/><line x1="840" y1="250" x2="840" y2="630" stroke="{INK}" stroke-width="7"/><line x1="680" y1="440" x2="1000" y2="440" stroke="{INK}" stroke-width="7"/>
<path d="M660 240 Q700 450 650 650 L620 650 L620 240 Z" fill="#c0504d" stroke="{INK}" stroke-width="6"/><path d="M1020 240 Q980 450 1030 650 L1060 650 L1060 240 Z" fill="#c0504d" stroke="{INK}" stroke-width="6"/>
<rect x="70" y="260" width="230" height="170" fill="#fff8e7" stroke="{INK}" stroke-width="7" transform="rotate(-3 185 345)"/><text x="185" y="340" font-family="Inter" font-weight="900" font-size="34" text-anchor="middle" fill="#c0504d" transform="rotate(-3 185 345)">GIVE</text><text x="185" y="385" font-family="Inter" font-weight="900" font-size="34" text-anchor="middle" fill="#c0504d" transform="rotate(-3 185 345)">THANKS</text>
<g fill="#e9a23b" stroke="{INK}" stroke-width="5"><path d="M120 520 l18 30 l-36 0 z"/><path d="M220 560 l18 30 l-36 0 z"/><path d="M170 600 l18 30 l-36 0 z"/></g>'''
    if name == "store":  # Nov 25: grocery aisle (Malik's cranberry run)
        shelf = ""
        for row, y in enumerate((330, 560, 790, 1020)):
            for side, x0 in ((0, 0), (1, 760)):
                shelf += f'<rect x="{x0}" y="{y + 170}" width="320" height="22" fill="#9aa5ae" stroke="{INK}" stroke-width="5"/>'
                for k in range(4):
                    col = ["#d64545", "#f2b134", "#3d8bd9", "#6fbf5a"][(k + row + side) % 4]
                    shelf += f'<rect x="{x0 + 14 + k * 76}" y="{y + 70}" width="60" height="100" rx="8" fill="{col}" stroke="{INK}" stroke-width="4"/><rect x="{x0 + 14 + k * 76}" y="{y + 100}" width="60" height="34" fill="#fff" opacity=".85"/>'
        return f'''<rect width="1080" height="1920" fill="#eef1e6"/><rect y="1380" width="1080" height="540" fill="#d7d2c4"/><rect y="1360" width="1080" height="30" fill="#bdb7a6"/>
<rect x="0" y="300" width="320" height="1080" fill="#c9ced3" stroke="{INK}" stroke-width="7"/><rect x="760" y="300" width="320" height="1080" fill="#c9ced3" stroke="{INK}" stroke-width="7"/>
{shelf}<rect x="390" y="90" width="300" height="130" rx="14" fill="#2f6fb3" stroke="{INK}" stroke-width="7"/><line x1="540" y1="0" x2="540" y2="90" stroke="{INK}" stroke-width="6"/>
<text x="540" y="150" font-family="Inter" font-weight="900" font-size="52" text-anchor="middle" fill="#fff">AISLE 4</text><text x="540" y="198" font-family="Inter" font-weight="800" font-size="28" text-anchor="middle" fill="#ffd166">CANNED GOODS</text>'''
    if name == "shoestore":  # Nov 27 midday: Black Friday sneaker store (Malik vs Dez, one pair of size 11s)
        wall = ""
        for row, y in enumerate((300, 470, 640, 810, 980, 1150)):
            for side, x0 in ((0, 0), (1, 770)):
                wall += f'<rect x="{x0}" y="{y + 120}" width="310" height="18" fill="#8a6a4a" stroke="{INK}" stroke-width="4"/>'
                for k in range(3):
                    col = ["#e5484d", "#2f6fb3", "#f2b134", "#2a9d8f"][(k + row + side) % 4]
                    wall += f'<rect x="{x0 + 16 + k * 100}" y="{y + 40}" width="84" height="80" rx="6" fill="{col}" stroke="{INK}" stroke-width="4"/><rect x="{x0 + 16 + k * 100}" y="{y + 40}" width="84" height="18" fill="#fff" opacity=".7"/>'
        return f'''<rect width="1080" height="1920" fill="#f3ece2"/><rect y="1380" width="1080" height="540" fill="#3c3f46"/><rect y="1360" width="1080" height="30" fill="#25272c"/>
<rect x="0" y="300" width="310" height="1080" fill="#e3d5c3" stroke="{INK}" stroke-width="7"/><rect x="770" y="300" width="310" height="1080" fill="#e3d5c3" stroke="{INK}" stroke-width="7"/>{wall}
<rect x="320" y="80" width="440" height="150" rx="14" fill="#1f1b2d" stroke="{INK}" stroke-width="7"/><text x="540" y="150" font-family="Inter" font-weight="900" font-size="56" text-anchor="middle" fill="#ffd166">BLACK FRIDAY</text><text x="540" y="205" font-family="Inter" font-weight="800" font-size="34" text-anchor="middle" fill="#fff">SNEAKERS -40%</text>'''
    if name == "race":  # Nov 26 evening: outdoor turkey trot 5K (Danny Day 6)
        return f'''<rect width="1080" height="1920" fill="#bfe3f5"/><circle cx="880" cy="200" r="80" fill="#ffe08a"/>
<rect y="1100" width="1080" height="820" fill="#7fbf6a"/><path d="M380 1100 L700 1100 L1080 1920 L0 1920 Z" fill="#8d8f96"/><path d="M540 1100 L540 1920" stroke="#fff" stroke-width="10" stroke-dasharray="40 40"/>
<g fill="#4f9a5a" stroke="{INK}" stroke-width="6"><circle cx="90" cy="980" r="110"/><circle cx="1000" cy="960" r="120"/></g><rect x="80" y="1060" width="22" height="80" fill="#7a5a3a"/><rect x="990" y="1060" width="22" height="80" fill="#7a5a3a"/>
<rect x="160" y="300" width="760" height="150" rx="14" fill="#e76f3c" stroke="{INK}" stroke-width="8"/><text x="540" y="400" font-family="Inter" font-weight="900" font-size="80" text-anchor="middle" fill="#fff">TURKEY TROT 5K</text>
<line x1="180" y1="450" x2="180" y2="1100" stroke="{INK}" stroke-width="10"/><line x1="900" y1="450" x2="900" y2="1100" stroke="{INK}" stroke-width="10"/>'''
    if name == "museum":  # Nov 25 night: History host Gus. Exhibit frame inner area = x 735-1025, y 255-605 (paste the archival image there)
        return f'''<rect width="1080" height="1920" fill="#3a4160"/><rect y="1380" width="1080" height="540" fill="#7a5a3a"/><rect y="1360" width="1080" height="30" fill="#5e452c"/>
<rect x="710" y="230" width="340" height="400" fill="#b8893f" stroke="{INK}" stroke-width="10"/><rect x="735" y="255" width="290" height="350" fill="#6b7080"/>
<rect x="800" y="650" width="160" height="44" rx="6" fill="#f4f1de" stroke="{INK}" stroke-width="5"/>
<rect x="40" y="300" width="220" height="280" fill="#b8893f" stroke="{INK}" stroke-width="10"/><rect x="62" y="322" width="176" height="236" fill="#4f6b5a"/>
<path d="M0 1380 L300 1380 L120 1920 L0 1920 Z" fill="#ffe08a" opacity=".12"/>
<rect x="110" y="1250" width="40" height="130" fill="#c9a24a" stroke="{INK}" stroke-width="5"/><rect x="930" y="1250" width="40" height="130" fill="#c9a24a" stroke="{INK}" stroke-width="5"/><path d="M130 1270 Q540 1330 950 1270" fill="none" stroke="#b02a37" stroke-width="12"/>'''
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
