"""Turn last episode's REAL engagement into the HUD + LAST EPISODE scoreboard config (RUNBOOK 3b). Works for every series.
Usage: python3 -I pipeline/score.py <series> views=318 likes=2 comments=6 shares=0 saves=0 [days_left=27] [--save]
       python3 -I pipeline/score.py horde            (HUD tiles from boss/totals in state)
Prints JSON with "hud", "scoreboard" and a suggested "script_sb" to paste into the episode config.
--save writes the new aura value + a log line into state.json (only after the episode is posted)."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, "state.json")
state = json.load(open(P)); series = sys.argv[1]; s = state["series"][series]; fm = s.get("format", {})
m = {k: int(v) for k, v in (a.split("=") for a in sys.argv[2:] if "=" in a)}

if series == "horde":
    b, t = s["boss"], s["totals"]
    print(json.dumps({"hud": {"tiles": [
        {"label": "BOSS HP", "value": f"{b['hp']:,}", "color": [235, 80, 95]},
        {"label": "DAMAGE", "value": f"{t['damage']:,}", "color": [120, 225, 120]},
        {"label": "CLEANERS", "value": f"{t['cleaners']:,}", "color": [255, 214, 102]}]},
        "note": "Add 'from' + 'at' to a tile to animate today's change (e.g. BOSS HP from yesterday's value)."}, indent=1))
    sys.exit()

a = s["aura"]; rules = a["rules"]; lab = a.get("label", "AURA"); mx = a.get("max", 100)
rows, gained = [], 0
for key, (pts, per, label) in rules.items():
    v = m.get(key, 0); p = (v // per) * pts; gained += p
    rows.append([key.upper(), label, f"{v:,}", p])
old = a["value"]; new = min(mx, old + gained)
avg = sum(s["stats"].values()) / len(s["stats"])
prog = (lambda: f"{round(avg * 10)}") if fm.get("tile2_kind") == "ovr" else (lambda: f"{round(avg * 10)}%")
cols = fm.get("colors", [[255, 214, 102], [120, 225, 120], [235, 80, 95]])
t1 = fm.get("tile1", "DAYS LEFT")
t1v = str(m["days_left"]) if "days_left" in m else ("<day>/30" if t1 == "DAY" else "<days left after this episode>")
script = [[0.2, "Last episode..."]] + [[0.12, f"{r[2]} {r[0].lower()}."] for r in rows] + \
         [[0.2, f"That's {gained} more {lab.lower()}." if gained else f"Zero {lab.lower()}. Ouch."]]
out = {
    "hud": {"tiles": [
        {"label": t1, "value": t1v, "color": cols[0]},
        {"label": fm.get("tile2", "GLOW-UP"), "value": "<recompute after today's vote>", "from": prog(), "at": ["s2", 0], "color": cols[1]},
        {"label": lab, "value": f"{new}/{mx}", "from": f"{old}/{mx}", "at": ["sb", -1], "color": cols[2]}]},
    "scoreboard": {"title": "LAST EPISODE", "label": lab, "from": old, "to": new, "max": mx, "rows": rows},
    "script_sb": script,
    "note": f"{fm.get('tile2', 'GLOW-UP')} = average of the stats ({prog()} now); recompute after applying today's vote. {lab} {old} -> {new} (+{gained}).",
}
print(json.dumps(out, indent=1, ensure_ascii=False))
if "--save" in sys.argv:
    a["value"] = new; a.setdefault("log", []).append(f"{s.get('last_post_date')}: +{gained} from " + ", ".join(f"{k}={m.get(k, 0)}" for k in rules))
    open(P, "w").write(json.dumps(state, indent=1, ensure_ascii=False) + "\n"); print("saved", lab, new)
