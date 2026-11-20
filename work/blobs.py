"""White paint blobs in a region -> convex hull (crosswalk helper).
python work/blobs.py IMG x0 y0 x1 y1 [--thr 150] [--minarea 15] [--exclude x0,y0,x1,y1 ...]"""
import argparse
import cv2
import numpy as np
ap = argparse.ArgumentParser()
ap.add_argument("img"); ap.add_argument("box", nargs=4, type=int)
ap.add_argument("--thr", type=float, default=150); ap.add_argument("--sat", type=float, default=45)
ap.add_argument("--minarea", type=int, default=15); ap.add_argument("--exclude", nargs="*", default=[])
ap.add_argument("--local", type=float, default=35)
a = ap.parse_args()
im = cv2.imread(a.img).astype(np.float32)
x0, y0, x1, y1 = a.box
g = im.mean(axis=2)
sat = im.max(axis=2) - im.min(axis=2)
bg = cv2.blur(g, (41, 41))
m = ((g > a.thr) | (g - bg > a.local)) & (sat < a.sat)
mask = np.zeros(g.shape, np.uint8)
mask[y0:y1, x0:x1] = m[y0:y1, x0:x1]
for e in a.exclude:
    ex0, ey0, ex1, ey1 = map(int, e.split(","))
    mask[ey0:ey1, ex0:ex1] = 0
n, lab, st, cen = cv2.connectedComponentsWithStats(mask, 8)
pts = []
for i in range(1, n):
    x, y, w, h, area = st[i]
    if area < a.minarea:
        continue
    print(f"blob {i}: x {x}-{x+w} y {y}-{y+h} area {area}")
    ys, xs = np.where(lab == i)
    pts.append(np.stack([xs, ys], 1))
if pts:
    P = np.concatenate(pts).astype(np.int32)
    hull = cv2.convexHull(P).reshape(-1, 2)
    hull = cv2.approxPolyDP(hull.reshape(-1, 1, 2), 1.0, True).reshape(-1, 2)
    print("HULL", [(int(x), int(y)) for x, y in hull])
