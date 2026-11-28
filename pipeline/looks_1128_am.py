"""Nov 28 morning extras: looks for Jess (the dress-color reply-all), Theo (37 drafts), Danny (push-up practice),
Wes (Brooke arrives at 9). Run: python3 -I pipeline/looks_1128_am.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import props
from props import phone, sign, burst, chip, INK
A = os.path.join(HERE, "assets")
ONLY = sys.argv[1] if len(sys.argv) > 1 else None

JL = {"hair_style": "long_waves", "top": "dress", "top_color": "#8a2846", "top_dark": "#6a1d35", "earrings": True,
      "makeup": 1, "phone": False, "bags": False}
def jl(**k):
    d = dict(JL); d.update(k); return d
X = '<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="#d62828" stroke-width="16" stroke-linecap="round"/>'

specs = []
# ---------------- Jess (jess_bedroom: the pink BRIDESMAID dress hangs on the left = the color Ryan wants)
specs += [
    {"out": f"{A}/jess_b1128_replyall.jpg", "who": "jess", "scene": "jess_bedroom", "look": jl(mouth="shock", brow_tilt=16, sweat=True),
     "extra": phone(560, 1240, ["GRANDMA:", "from the fitting!", "[photo: pliers]", "", "Ryan liked this"], title="WEDDING CHAT (14)", w=340, h=330, size=28, angle=-4, title_bg="#e05a8c")
              + burst(800, 1080, "REPLY ALL", r=120, size=30)},
    {"out": f"{A}/jess_b1128_ha.jpg", "who": "jess", "scene": "jess_bedroom", "look": jl(mouth="flat", brow_tilt=-6, gaze=1),
     "extra": phone(560, 1240, ["what color", "is the dress", "for my tie", "", "you: ha"], title="RYAN", w=320, h=330, size=32, angle=-4)},
    {"out": f"{A}/jess_b1128_beige.jpg", "who": "jess", "scene": "jess_bedroom", "look": jl(mouth="smirk", brow_tilt=-12, gaze=1),
     "extra": phone(560, 1240, ["you: beige", "", "MOM: it's BLUSH", "sweetie"], title="WEDDING CHAT (14)", w=340, h=320, size=32, angle=-5, title_bg="#e05a8c")},
    {"out": f"{A}/jess_b1128_delete.jpg", "who": "jess", "scene": "jess_bedroom", "look": jl(mouth="sad", brow_tilt=14),
     "extra": phone(560, 1240, ["Delete for", "everyone", "", "> Delete for me"], title="DELETE?", w=320, h=320, size=34, angle=-5, title_bg="#d62828")},
    {"out": f"{A}/jess_b1128_added.jpg", "who": "jess", "scene": "jess_bedroom", "look": jl(mouth="flat", brow_tilt=10, tired=0.4),
     "extra": phone(560, 1240, ["Jess left", "", "Chloe added Jess", "role: MAID OF", "HONOR"], title="WEDDING CHAT (14)", w=340, h=330, size=30, angle=-5, title_bg="#e05a8c")},
    {"out": f"{A}/jess_b1128_walter.jpg", "who": "jess", "scene": "jess_bedroom", "look": jl(mouth="shock", brow_tilt=12, gaze=-1),
     "extra": phone(370, 1240, ["got the tie.", "blush."], title="RYAN", w=270, h=280, size=34, angle=-7)
              + phone(730, 1250, ["also bought", "blush. shall", "we match? - W"], title="WALTER (81)", w=290, h=300, size=30, angle=6, title_bg="#2f9e8f")},
]
# ---------------- Theo (3D base: the Sharpie brow from Friday)
TB = f"{A}/theo_b1128_base.jpg"
BROW = '<path d="M548 628 Q640 528 742 598" fill="none" stroke="#111" stroke-width="30" stroke-linecap="round"/>'
theo = [
    {"base": f"{A}/theo_teeth_drawnbrow.jpg", "out": TB, "svg": BROW},
    {"base": TB, "out": f"{A}/theo_b1128_drafts.jpg",
     "svg": phone(540, 1210, ["it's for you", "it's for a frie", "ok so basically", "the suit is f", "..."], title="DRAFTS (37)", w=380, h=380, size=34, angle=-4)},
    {"base": TB, "out": f"{A}/theo_b1128_you.jpg",
     "svg": phone(540, 1210, ["it's for you"], title="TO: MAYA", w=360, h=300, size=40, angle=-4)
            + X.format(a=380, b=1150, c=700, d=1300) + chip(540, 1400, "DELETED", bg="#d62828", fg="#fff", size=46, angle=4)},
    {"base": TB, "out": f"{A}/theo_b1128_friend.jpg",
     "svg": phone(540, 1210, ["it's for a friend", "", "(which friend??)"], title="TO: MAYA", w=380, h=320, size=36, angle=5)
            + chip(540, 1410, "DELETED", bg="#d62828", fg="#fff", size=46, angle=-4)},
    {"base": TB, "out": f"{A}/theo_b1128_memo.jpg",
     "svg": phone(540, 1210, ["VOICE MEMO 0:04", "▂▅▇▃▁▇▅▂", "\"the SUIT-\""], title="TO: MAYA", w=380, h=320, size=34, angle=-4)
            + burst(790, 1060, "CRACK", r=110, size=46)},
    {"base": TB, "out": f"{A}/theo_b1128_mom.jpg",
     "svg": sign(540, 1210, ["MOM (DOWNSTAIRS):", "DID YOU TELL", "HER YET??"], bg="#fff8e7", fg="#c0504d", size=44, angle=-3)},
    {"base": TB, "out": f"{A}/theo_b1128_what.jpg",
     "svg": phone(540, 1210, ["tell me what?", "", "typing..."], title="MAYA", w=360, h=330, size=40, angle=4)},
]
# ---------------- Danny (danny_bedroom: push-up practice for Sunday)
DL = {"top": "polo"}
specs += [
    {"out": f"{A}/danny_b1128_hook.jpg", "who": "danny", "scene": "danny_bedroom", "look": {"mouth": "shock", "brow_tilt": 12, "sweat": True},
     "extra": sign(330, 1250, ["GOAL: 100", "DONE: 11"], bg="#fff8e7", fg="#c0504d", size=50, angle=-4)
              + chip(740, 1330, "SUNDAY", bg="#e5484d", fg="#fff", size=44, angle=5)},
    {"out": f"{A}/danny_b1128_brock.jpg", "who": "danny", "scene": "danny_bedroom", "look": {"mouth": "flat", "brow_tilt": 6, "gaze": 1},
     "extra": phone(560, 1250, ["[video]", "warm-up set: 100", "", "see u sunday ceo"], title="BROCK", w=340, h=340, size=32, angle=-5, title_bg="#e5484d")},
    {"out": f"{A}/danny_b1128_89.jpg", "who": "danny", "scene": "danny_bedroom", "look": {"mouth": "grin", "brow_tilt": -12},
     "extra": sign(360, 1260, ["NEW GOAL: 89", "(@h.nguy3n07", "believes)"], bg="#ffd166", fg=INK, size=40, angle=-4)},
    {"out": f"{A}/danny_b1128_floor.jpg", "who": "danny", "scene": "danny_bedroom", "look": {"mouth": "sad", "brow_tilt": 16, "sweat": True, "tired": 0.6},
     "extra": sign(330, 1300, ["SET 1: 11", "ARMS: NO"], bg="#fff8e7", fg="#c0504d", size=46, angle=4)
              + burst(760, 1060, "THUD", r=110, size=48)},
    {"out": f"{A}/danny_b1128_tara.jpg", "who": "danny", "scene": "danny_bedroom", "look": {"mouth": "shock", "brow_tilt": 10, "gaze": 1, "sweat": True},
     "extra": phone(560, 1250, ["FaceTime", "", "are you doing", "push-ups AT me?"], title="TARA", w=340, h=340, size=34, angle=-5, title_bg="#e05a8c")},
    {"out": f"{A}/danny_b1128_total.jpg", "who": "danny", "scene": "danny_bedroom", "look": {"mouth": "flat", "brow_tilt": -4, "tired": 0.5},
     "extra": sign(340, 1260, ["TODAY: 14", "TOMORROW: 100"], bg="#fff8e7", fg="#c0504d", size=44, angle=-3)
              + chip(760, 1340, "TAB: $1,140", bg="#e5484d", fg="#fff", size=40, angle=5)},
]
# ---------------- Wes (street: the park, Saturday 7 AM, Brooke arrives at 9)
def donutbox(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-150" y="-60" width="300" height="120" rx="10" fill="#f7b6cd" stroke="{INK}" stroke-width="7"/>'
            f'<text x="0" y="14" font-family="Inter" font-weight="900" font-size="38" text-anchor="middle" fill="{INK}">DONUTS</text></g>')
def slide(x, y, full=False):
    g = (f'<g transform="translate({x} {y})"><path d="M-160 120 L80 -120 L120 -120 L-120 120 Z" fill="#e5484d" stroke="{INK}" stroke-width="7"/>'
         f'<line x1="100" y1="-120" x2="100" y2="140" stroke="{INK}" stroke-width="12"/>')
    if full:
        for i, (dx, dy, c) in enumerate([(-80, 90, "#ffd166"), (-30, 60, "#ef8354"), (20, 20, "#8fe36b"), (-120, 110, "#bde0fe"), (40, 80, "#ffd166"), (-50, 120, "#cdb4db")]):
            g += f'<rect x="{dx}" y="{dy}" width="60" height="40" rx="8" fill="{c}" stroke="{INK}" stroke-width="5" transform="rotate({i * 23} {dx + 30} {dy + 20})"/>'
    return g + '</g>'
def bags_walk(x, y):
    g = ""
    for k, dx in enumerate((-110, 20, 150)):
        g += (f'<g transform="translate({x + dx} {y})"><path d="M-55 60 Q-70 -40 0 -70 Q70 -40 55 60 Z" fill="#2b2d42" stroke="{INK}" stroke-width="6"/>'
              f'<circle cx="-18" cy="-10" r="12" fill="#8fe36b"/><circle cx="18" cy="-10" r="12" fill="#8fe36b"/>'
              f'<line x1="-25" y1="60" x2="-35" y2="100" stroke="{INK}" stroke-width="8"/><line x1="25" y1="60" x2="35" y2="100" stroke="{INK}" stroke-width="8"/></g>')
    return g
def butt_goblin(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-50" y="-150" width="100" height="260" rx="20" fill="#f4efe6" stroke="{INK}" stroke-width="7"/>'
            f'<rect x="-50" y="30" width="100" height="80" rx="16" fill="#e9a14b" stroke="{INK}" stroke-width="7"/>'
            f'<circle cx="-18" cy="-80" r="14" fill="#8fe36b" stroke="{INK}" stroke-width="4"/><circle cx="18" cy="-80" r="14" fill="#8fe36b" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M-25 -40 Q0 -20 25 -40" fill="none" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M-50 -150 Q-30 -190 0 -170 Q30 -200 50 -150" fill="#9aa0a6" stroke="{INK}" stroke-width="5" opacity=".8"/></g>')
WL = {}
specs += [
    {"out": f"{A}/wes_b1128_hook.jpg", "who": "wes", "scene": "street", "look": {"mouth": "shock", "brow_tilt": 12, "sweat": True},
     "extra": sign(330, 1250, ["BROOKE: 9 AM", "PARK: 4% CLEAN"], bg="#fff8e7", fg="#c0504d", size=40, angle=-4)
              + chip(760, 1340, "NOW: 11 PM", bg="#1f1b2d", fg="#ffd166", size=44, angle=5)},
    {"out": f"{A}/wes_b1128_cole.jpg", "who": "wes", "scene": "street", "look": {"mouth": "flat", "brow_tilt": 8, "gaze": 1},
     "extra": phone(560, 1260, ["WES.", "SHE'S BRINGING", "DONUTS.", "DO NOT LET HER", "PICK UP ANYTHING"], title="RANGER COLE", w=360, h=380, size=30, angle=-5, title_bg="#2f6b3a")},
    {"out": f"{A}/wes_b1128_slide.jpg", "who": "wes", "scene": "street", "look": {"mouth": "grin", "brow_tilt": -10, "sweat": True},
     "extra": '<g transform="translate(-260 -560) scale(1.5)">' + slide(420, 1240, full=True) + '</g>' + burst(820, 1060, "STUFFED", r=130, size=36)},
    {"out": f"{A}/wes_b1128_bags.jpg", "who": "wes", "scene": "street", "look": {"mouth": "shock", "brow_tilt": 14, "gaze": -1},
     "extra": bags_walk(480, 1290) + chip(540, 1460, "THEY WALKED BACK", bg="#e5484d", fg="#fff", size=40, angle=-3)},
    {"out": f"{A}/wes_b1128_goblin.jpg", "who": "wes", "scene": "street", "look": {"mouth": "sad", "brow_tilt": 16, "sweat": True},
     "extra": butt_goblin(330, 1250, 0.9) + chip(700, 1330, "HP 2,600", bg="#e5484d", fg="#fff", size=46, angle=4)},
    {"out": f"{A}/wes_b1128_car.jpg", "who": "wes", "scene": "street", "look": {"mouth": "flat", "brow_tilt": 4, "gaze": 1},
     "extra": chip(330, 1180, "8:59", bg="#1f1b2d", fg="#ffd166", size=60, angle=-4) + donutbox(660, 1300, 0.95)},
]
if ONLY:
    specs = [s for s in specs if ONLY in s["out"]]; theo = [t for t in theo if ONLY in t["out"]]
props.render_many(specs)
if theo: props.overlay_many(theo)
outs = [s["out"] for s in specs] + [t["out"] for t in theo]
props.strip(outs, "/tmp/claude-0/looks_1128am.jpg", w=140)
