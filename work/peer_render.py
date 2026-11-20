"""Render a peer's CVAT export onto the class images: python work/peer_render.py ZIP [ZIP...] --out DIR"""
import sys, zipfile, json
import xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import build

args = sys.argv[1:]
out = Path(args[args.index("--out") + 1]); zips = args[:args.index("--out")]
out.mkdir(parents=True, exist_ok=True)
dump = {}
for z in zips:
    r = ET.fromstring(zipfile.ZipFile(z).read("annotations.xml"))
    for im in r.findall("image"):
        tags = {t.get("label"): (t.find("attribute").text if t.find("attribute") is not None else None) for t in im.findall("tag")}
        shapes = []
        for i, s in enumerate(c for c in im if c.tag != "tag"):
            pts = [[float(v) for v in p.split(",")] for p in s.get("points").split(";")] if s.tag != "box" else \
                  [[float(s.get("xtl")), float(s.get("ytl"))], [float(s.get("xbr")), float(s.get("ybr"))]]
            typ = {"box": "rectangle"}.get(s.tag, s.tag)
            shapes.append({"label": s.get("label"), "type": typ, "points": pts, "occluded": s.get("occluded") == "1",
                           "attributes": {a.get("name"): a.text for a in s.findall("attribute")}, "idx": i})
        dump[im.get("name")] = {"tags": tags, "shapes": shapes}
        build.OVL = out
        build.render(im.get("name"), dump[im.get("name")])
(out / "peer.json").write_text(json.dumps(dump, indent=1, ensure_ascii=False), encoding="utf-8")
print(len(dump), "images ->", out)
