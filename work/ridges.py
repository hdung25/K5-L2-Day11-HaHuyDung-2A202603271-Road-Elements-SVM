"""Print bright-ridge positions along columns (or rows): python work/ridges.py IMG col|row x0 x1 step lo hi [yellow]"""
import sys
import numpy as np
from PIL import Image
img = np.asarray(Image.open(sys.argv[1]).convert("RGB"), dtype=float)
mode, a, b, st, lo, hi = sys.argv[2], *map(int, sys.argv[3:8])
yellow = len(sys.argv) > 8
sc = ((img[..., 0] + img[..., 1]) / 2 - img[..., 2]) if yellow else img.mean(axis=2)
for v in range(a, b + 1, st):
    prof = sc[lo:hi, v] if mode == "col" else sc[v, lo:hi]
    prof = np.convolve(prof, np.ones(3) / 3, mode="same")
    k = int(__import__("os").environ.get("RK", "6"))
    out = []
    for i in range(k, len(prof) - k):
        bg = max(prof[i - k:i - 2].mean(), prof[i + 3:i + k + 1].mean())
        r = prof[i] - bg
        if r > 15 and prof[i] == prof[max(0, i - 3):i + 4].max():
            out.append(f"{lo + i}({r:.0f})")
    print(v, " ".join(out))
