"""Build work/ann.json from work/spec/*.py (hand-placed points) and render overlays.

python work/build.py [SLOT ...]      # only rebuild / render these slots (default: all)

Each spec file defines IMAGE (file name), TAGS (dict) and SHAPES (list of dicts):
  {"label": "lane", "pts": [...near->far...], "attrs": {...}, "snap": {"color": "white", ...} or None,
   "occluded": bool}
Lane / road_curb with "snap" are moved onto the paint centre by work/snap.py.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
import snap as snapmod  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "work" / "spec"
OUT = ROOT / "work" / "ann.json"
OVL = ROOT / "work" / "overlay"
TYPES = {"lane": "polyline", "road_curb": "polyline", "crosswalk": "polygon", "drivable": "polygon",
         "traffic_light": "rectangle", "traffic_sign": "rectangle"}
COL = {"lane": (255, 40, 40), "road_curb": (255, 140, 0), "crosswalk": (255, 0, 255), "drivable": (0, 255, 0),
       "traffic_light": (255, 255, 0), "traffic_sign": (0, 160, 255)}


def load_spec(p: Path):
    s = importlib.util.spec_from_file_location(p.stem, p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _keep_border(rough0, pts, W, H):
    """If the hand-placed first point sat on the image border, extend the snapped line back to that border."""
    (x0, y0), (x1, y1) = pts[0], pts[1]
    rx, ry = rough0
    if ry >= H - 2 and y1 != y0:
        t = (H - y0) / (y1 - y0)
        pts[0] = (round(x0 + t * (x1 - x0), 1), float(H))
    elif rx <= 2 and x1 != x0:
        t = (0 - x0) / (x1 - x0)
        pts[0] = (0.0, round(y0 + t * (y1 - y0), 1))
    elif rx >= W - 2 and x1 != x0:
        t = (W - x0) / (x1 - x0)
        pts[0] = (float(W), round(y0 + t * (y1 - y0), 1))
    return pts


def build_one(m) -> dict:
    img = str(ROOT / "data" / m.IMAGE)
    W, H = Image.open(img).size
    shapes = []
    by_pos = {}
    for sh in m.SHAPES:
        if "between" in sh:  # drivable polygon built from two finished polylines
            lp = by_pos[sh["between"][0]] if isinstance(sh["between"][0], str) else sh["between"][0]
            rp = by_pos[sh["between"][1]] if isinstance(sh["between"][1], str) else sh["between"][1]
            lp = [p for p in lp if p[1] <= sh.get("ymax", 1e9)]
            rp = [p for p in rp if p[1] <= sh.get("ymax", 1e9)]
            pts = sh.get("left_pre", []) + lp + sh.get("far", []) + rp[::-1] + sh.get("bottom", [])
            pts = [tuple(map(float, p)) for p in pts]
            shapes.append({"label": "drivable", "type": "polygon", "points": [list(p) for p in pts],
                           "attributes": {"area_type": sh["area_type"]}, "occluded": False, "z": 0, "note": ""})
            continue
        pts = [tuple(map(float, p)) for p in sh["pts"]]
        if sh.get("snap") is not None and TYPES[sh["label"]] == "polyline":
            rough0 = pts[0]
            pts = snapmod.snap(img, pts, **sh["snap"])
            pts = _keep_border(rough0, pts, *Image.open(img).size)
        if TYPES[sh["label"]] == "rectangle":
            (x0, y0), (x1, y1) = pts
            pts = [(min(x0, x1), min(y0, y1)), (max(x0, x1), max(y0, y1))]
        if sh["label"] in ("lane", "road_curb"):
            by_pos[sh.get("key") or sh.get("attrs", {}).get("position", "curb")] = [tuple(p) for p in pts]
        shapes.append({"label": sh["label"], "type": TYPES[sh["label"]], "points": [list(p) for p in pts],
                       "attributes": sh.get("attrs", {}), "occluded": bool(sh.get("occluded", False)),
                       "z": sh.get("z", 0), "note": sh.get("note", "")})
    for sh in shapes:  # keep every vertex inside the image frame
        sh["points"] = [[round(min(max(x, 0.0), W), 1), round(min(max(y, 0.0), H), 1)] for x, y in sh["points"]]
    return {"tags": m.TAGS, "shapes": shapes}


def render(name: str, a: dict, scale: float = 1.0):
    im = Image.open(ROOT / "data" / name).convert("RGB")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    dl = ImageDraw.Draw(im)
    font = ImageFont.load_default()
    for s in a["shapes"]:
        c = COL[s["label"]]
        pts = [tuple(p) for p in s["points"]]
        if s["type"] == "polygon":
            d.polygon(pts, fill=c + (60,), outline=c + (255,))
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    dl = ImageDraw.Draw(im)
    for s in a["shapes"]:
        c = COL[s["label"]]
        pts = [tuple(p) for p in s["points"]]
        if s["type"] == "rectangle":
            dl.rectangle(pts, outline=c, width=1)
            txt = s["attributes"].get("color") or s["attributes"].get("group", "")
            dl.text((pts[0][0], pts[1][1] + 1), txt[:4], fill=c, font=font)
        elif s["type"] == "polyline":
            dl.line(pts, fill=c, width=1)
            for p in pts:
                dl.ellipse([p[0] - 2, p[1] - 2, p[0] + 2, p[1] + 2], outline=c)
            at = s["attributes"]
            lab = at.get("position", "curb") + ("" if s["label"] != "lane" else f" {at['style'][0]}{at['color'][0]}{at['kind'][0]}") + (" occ" if s["occluded"] else "")
            dl.ellipse([pts[0][0] - 4, pts[0][1] - 4, pts[0][0] + 4, pts[0][1] + 4], fill=c)
            dl.text((pts[0][0] + 5, pts[0][1] - 12), lab, fill=(255, 255, 255), font=font)
    dl.text((5, 5), " ".join(f"{k}={v}" for k, v in a["tags"].items()), fill=(255, 255, 255), font=font)
    OVL.mkdir(parents=True, exist_ok=True)
    out = OVL / (Path(name).stem[:3] + ".png")
    im.save(out)
    return out


def main(slots: list[str]):
    ann = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    for p in sorted(SPEC.glob("*.py")):
        if slots and p.stem[:3] not in slots:
            continue
        m = load_spec(p)
        a = build_one(m)
        ann[m.IMAGE] = a
        print(m.IMAGE, len(a["shapes"]), "shapes ->", render(m.IMAGE, a))
    OUT.write_text(json.dumps(dict(sorted(ann.items())), indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1:])
