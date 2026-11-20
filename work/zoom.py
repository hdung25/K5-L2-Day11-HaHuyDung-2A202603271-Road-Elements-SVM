"""Crop + upscale a region of an image with a labelled pixel grid, for reading coordinates.

python work/zoom.py IMG x0 y0 x1 y1 [--scale 3] [--grid 10] [--out PATH] [--overlay ann.json]
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("img")
ap.add_argument("box", nargs=4, type=int)
ap.add_argument("--scale", type=float, default=0)
ap.add_argument("--grid", type=int, default=0)
ap.add_argument("--out", default="")
ap.add_argument("--overlay", default="")
a = ap.parse_args()

im = Image.open(a.img).convert("RGB")
x0, y0, x1, y1 = a.box
crop = im.crop((x0, y0, x1, y1))
w, h = crop.size
scale = a.scale or max(1.0, min(1280 / w, 900 / h))
big = crop.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
d = ImageDraw.Draw(big)
font = ImageFont.load_default()
grid = a.grid or (10 if max(w, h) <= 200 else 20 if max(w, h) <= 400 else 50 if max(w, h) <= 900 else 100)
for gx in range((x0 // grid + 1) * grid, x1, grid):
    X = (gx - x0) * scale
    major = gx % (grid * 5) == 0
    d.line([(X, 0), (X, big.height)], fill=(0, 255, 255) if major else (0, 140, 160), width=1)
    d.text((X + 2, 2), str(gx), fill=(255, 255, 0), font=font)
for gy in range((y0 // grid + 1) * grid, y1, grid):
    Y = (gy - y0) * scale
    major = gy % (grid * 5) == 0
    d.line([(0, Y), (big.width, Y)], fill=(0, 255, 255) if major else (0, 140, 160), width=1)
    d.text((2, Y + 2), str(gy), fill=(255, 255, 0), font=font)

if a.overlay:
    ann = json.loads(Path(a.overlay).read_text(encoding="utf-8"))
    key = Path(a.img).name
    colors = {"lane": (255, 0, 0), "road_curb": (255, 128, 0), "crosswalk": (255, 0, 255), "drivable": (0, 255, 0),
              "traffic_light": (255, 255, 0), "traffic_sign": (0, 128, 255)}
    for s in ann.get(key, {}).get("shapes", []):
        pts = [((x - x0) * scale, (y - y0) * scale) for x, y in s["points"]]
        c = colors.get(s["label"], (255, 255, 255))
        if s["type"] == "rectangle":
            d.rectangle([pts[0], pts[1]], outline=c, width=1)
        elif s["type"] == "polygon":
            d.line(pts + [pts[0]], fill=c, width=1)
        else:
            d.line(pts, fill=c, width=1)
            for p in pts:
                d.ellipse([p[0] - 2, p[1] - 2, p[0] + 2, p[1] + 2], outline=c)

out = a.out or str(Path(__file__).parent / "views" / f"{Path(a.img).stem[:3]}_{x0}_{y0}_{x1}_{y1}.png")
Path(out).parent.mkdir(parents=True, exist_ok=True)
big.save(out)
print(out, big.size, "scale", round(scale, 2), "grid", grid)
