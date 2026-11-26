"""Reusable SVG props for toon.py looks (Nov 26 evening run), so each run doesn't redraw phones/signs by hand.

Usage (Python):
    import props, toon
    extra = props.table() + props.phone(700, 1050, ["is your sister", "single?"], title="MATCH") + props.sign(540, 420, ["KIDS' TABLE"])
    props.render_many([{"out": "pipeline/assets/x.jpg", "who": "jess", "scene": "dining", "look": {...}, "extra": extra}, ...])
render_many() renders every spec with ONE Chromium launch and saves JPEG (quality 92).
All coordinates are on the 1080x1920 canvas; the character's head is centred at (540, 900), body from y ~1130.
Keep props inside x 230-850, y 1000-1450 when they must survive the camera push (RUNBOOK 5l.2.3)."""
import os, sys, html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
INK = "#1f1b2d"

def esc(t): return html.escape(str(t))

def phone(x, y, lines, title="", w=300, h=420, angle=-6, screen="#ffffff", fg="#1f1b2d", size=34, title_bg="#4a6cf7"):
    """A hand holding nothing, just a phone: centre (x, y). lines = text lines on the screen."""
    s = f'<g transform="rotate({angle} {x} {y})">'
    s += f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="34" fill="#22222c" stroke="{INK}" stroke-width="7"/>'
    s += f'<rect x="{x - w / 2 + 16}" y="{y - h / 2 + 40}" width="{w - 32}" height="{h - 70}" rx="12" fill="{screen}"/>'
    ty = y - h / 2 + 40
    if title:
        s += f'<rect x="{x - w / 2 + 16}" y="{ty}" width="{w - 32}" height="58" rx="12" fill="{title_bg}"/>'
        s += f'<text x="{x}" y="{ty + 41}" font-family="Inter" font-weight="900" font-size="30" text-anchor="middle" fill="#fff">{esc(title)}</text>'
        ty += 70
    for i, ln in enumerate(lines):
        s += f'<text x="{x}" y="{ty + 50 + i * (size + 14)}" font-family="Inter" font-weight="800" font-size="{size}" text-anchor="middle" fill="{fg}">{esc(ln)}</text>'
    return s + '</g>'

def sign(x, y, lines, w=None, bg="#fff8e7", fg="#c0504d", size=52, angle=-4, pad=26):
    w = w or max(len(l) for l in lines) * size * 0.62 + pad * 2
    h = len(lines) * (size + 10) + pad * 2 - 10
    s = f'<g transform="rotate({angle} {x} {y})"><rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="12" fill="{bg}" stroke="{INK}" stroke-width="7"/>'
    for i, ln in enumerate(lines):
        s += f'<text x="{x}" y="{y - h / 2 + pad + size * 0.82 + i * (size + 10)}" font-family="Inter" font-weight="900" font-size="{size}" text-anchor="middle" fill="{fg}">{esc(ln)}</text>'
    return s + '</g>'

def burst(x, y, text, r=120, fill="#ffd166", fg="#d62839", size=56, angle=-8):
    import math
    pts = []
    for k in range(24):
        rr = r if k % 2 == 0 else r * 0.68
        a = math.pi * 2 * k / 24
        pts.append(f"{x + rr * math.cos(a):.0f},{y + rr * math.sin(a):.0f}")
    return (f'<g transform="rotate({angle} {x} {y})"><polygon points="{" ".join(pts)}" fill="{fill}" stroke="{INK}" stroke-width="7"/>'
            f'<text x="{x}" y="{y + size * 0.35}" font-family="Inter" font-weight="900" font-size="{size}" text-anchor="middle" fill="{fg}">{esc(text)}</text></g>')

def table(y=1400, color="#a0673f", cloth="#f4efe6"):
    return (f'<rect x="0" y="{y}" width="1080" height="{1920 - y}" fill="{color}" stroke="{INK}" stroke-width="8"/>'
            f'<rect x="0" y="{y}" width="1080" height="70" fill="{cloth}" stroke="{INK}" stroke-width="6"/>')

def plate(x, y, food="#c98a4b", rx=150):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * 0.32:.0f}" fill="#fff" stroke="{INK}" stroke-width="6"/>'
            f'<ellipse cx="{x}" cy="{y - 6}" rx="{rx * 0.55:.0f}" ry="{rx * 0.16:.0f}" fill="{food}" stroke="{INK}" stroke-width="4"/>')

def turkey(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="0" rx="150" ry="95" fill="#c8813f" stroke="{INK}" stroke-width="7"/>'
            f'<ellipse cx="-30" cy="-25" rx="70" ry="35" fill="#dc9a55" opacity=".8"/>'
            f'<path d="M120 -40 L190 -80 L205 -60 L140 -10 Z" fill="#c8813f" stroke="{INK}" stroke-width="6"/><circle cx="200" cy="-75" r="16" fill="#fff" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M-120 -40 L-190 -80 L-205 -60 L-140 -10 Z" fill="#c8813f" stroke="{INK}" stroke-width="6"/><circle cx="-200" cy="-75" r="16" fill="#fff" stroke="{INK}" stroke-width="5"/>'
            f'<ellipse cx="0" cy="70" rx="210" ry="40" fill="#fff" stroke="{INK}" stroke-width="6"/></g>')

def placecard(x, y, name, angle=-3, w=200):
    return sign(x, y, [name], w=w, bg="#ffffff", fg=INK, size=40, angle=angle, pad=18)

def chip(x, y, text, bg="#ffd166", fg=INK, size=40, angle=0):
    return sign(x, y, [text], bg=bg, fg=fg, size=size, angle=angle, pad=16)

def render_many(specs):
    """Render toon specs (see toon.py) with one browser; writes JPEGs."""
    import toon
    from playwright.sync_api import sync_playwright
    from PIL import Image
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        for spec in specs:
            pg.set_content(f'<html><body style="margin:0;background:#000">{toon.svg(spec)}</body></html>')
            tmp = spec["out"] + ".png"
            pg.screenshot(path=tmp, clip={"x": 0, "y": 0, "width": 1080, "height": 1920})
            Image.open(tmp).convert("RGB").save(spec["out"], quality=92); os.remove(tmp)
            print(spec["out"])
        b.close()

def strip(paths, out, w=216):
    """Contact strip of looks for a quick visual check."""
    from PIL import Image
    h = int(w * 1920 / 1080); W = Image.new("RGB", (w * len(paths), h), "white")
    for i, pth in enumerate(paths):
        W.paste(Image.open(pth).convert("RGB").resize((w, h)), (i * w, 0))
    W.save(out); return out
