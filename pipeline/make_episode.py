"""Render one episode from a JSON config.
Usage: python3 make_episode.py episodes/<series>_dNN.json OUTDIR
Config keys: see episodes/malik_d01.json. 'image' is relative to pipeline/assets.
Steps: voice -> mix -> render. Output: OUTDIR/final.mp4 and OUTDIR/cover.jpg"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from engine import Episode
cfg = json.load(open(sys.argv[1])); out = sys.argv[2]
cfg["image"] = os.path.join(HERE, "assets", cfg["image"])
for k in ("accent",): cfg[k] = tuple(cfg[k])
if "color" in cfg["notif"]: cfg["notif"]["color"] = tuple(cfg["notif"]["color"])
cfg["stats"] = [tuple(s) for s in cfg["stats"]]; cfg["options"] = [tuple(o) for o in cfg["options"]]
cfg["script"] = {k: [tuple(x) for x in v if x[1].strip()] for k, v in cfg["script"].items()}
ep = Episode(cfg, out)
mode = sys.argv[3] if len(sys.argv) > 3 else "all"
if mode in ("all", "voice"): ep.voice()
ep.load_timing()
if mode == "stills": ep.render(stills=True)
elif mode == "all": ep.mix(); ep.render()
