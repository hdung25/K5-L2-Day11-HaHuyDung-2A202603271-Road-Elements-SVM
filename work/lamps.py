"""Find small lit lamp blobs (green / red / yellow) to locate traffic lights.
python work/lamps.py IMG x0 y0 x1 y1"""
import sys
import cv2
import numpy as np
img = cv2.imread(sys.argv[1])
x0, y0, x1, y1 = map(int, sys.argv[2:6])
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
H, S, V = hsv[..., 0].astype(int), hsv[..., 1].astype(int), hsv[..., 2].astype(int)
cols = {"green": (H >= 60) & (H <= 95), "red": (H <= 8) | (H >= 170), "yellow": (H >= 12) & (H <= 32)}
for name, m in cols.items():
    mm = (m & (S > 90) & (V > 150)).astype(np.uint8)
    sub = np.zeros_like(mm); sub[y0:y1, x0:x1] = mm[y0:y1, x0:x1]
    n, lab, st, cen = cv2.connectedComponentsWithStats(sub, 8)
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if a >= 3:
            print(name, f"x {x}-{x+w} y {y}-{y+h} area {a} centre ({cen[i][0]:.0f},{cen[i][1]:.0f})")
