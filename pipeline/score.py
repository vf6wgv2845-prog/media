"""Turn last episode's REAL engagement into the HUD + LAST EPISODE scoreboard config (RUNBOOK 3b).
Usage: python3 -I pipeline/score.py <series> views=318 likes=2 comments=6 shares=0 saves=0 [--save]
Prints a JSON block with "hud" and "scoreboard" to paste into the episode config, and a suggested "sb" script.
--save writes the new aura value + a log line into state.json (do this only after the episode is posted)."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, "state.json")
state = json.load(open(P)); series = sys.argv[1]; s = state["series"][series]
m = {k: int(v) for k, v in (a.split("=") for a in sys.argv[2:] if "=" in a)}
a = s["aura"]; rules = a["rules"]  # {"comments": [1, 1, "+1 each"], "views": [1, 100, "+1 per 100"], ...} = [points, per, label]
rows, gained = [], 0
for key, (pts, per, label) in rules.items():
    v = m.get(key, 0); p = (v // per) * pts; gained += p
    rows.append([key.upper(), label, f"{v:,}", p])
old = a["value"]; new = min(a.get("max", 100), old + gained)
glow = lambda st: f"{round(100 * sum(st.values()) / (10 * len(st)))}%"
words = {0: "zero"}
script = [[0.2, "Last episode..."]] + [[0.12, f"{r[2]} {r[0].lower()}."] for r in rows] + [[0.2, f"That's {gained} more aura." if gained else "Zero aura. Ouch."]]
out = {
    "hud": {"tiles": [
        {"label": "DAYS LEFT", "value": "<days left after this episode>", "color": [255, 214, 102]},
        {"label": "GLOW-UP", "value": "<new %, see note>", "from": glow(s["stats"]), "at": ["s2", 0], "color": [120, 225, 120]},
        {"label": "AURA", "value": f"{new}/{a.get('max', 100)}", "from": f"{old}/{a.get('max', 100)}", "at": ["sb", -1], "color": [235, 80, 95]}]},
    "scoreboard": {"title": "LAST EPISODE", "label": "AURA", "from": old, "to": new, "max": a.get("max", 100), "rows": rows},
    "script_sb": script,
    "note": f"GLOW-UP = average of the stats as %. Current {glow(s['stats'])}; recompute after applying today's vote. Aura {old} -> {new} (+{gained}).",
}
print(json.dumps(out, indent=1, ensure_ascii=False))
if "--save" in sys.argv:
    a["value"] = new; a.setdefault("log", []).append(f"{s.get('last_post_date')}: +{gained} from " + ", ".join(f"{k}={m.get(k, 0)}" for k in rules))
    open(P, "w").write(json.dumps(state, indent=1, ensure_ascii=False) + "\n"); print("saved aura", new)
