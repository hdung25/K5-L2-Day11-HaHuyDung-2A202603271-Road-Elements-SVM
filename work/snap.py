"""Snap a hand-placed rough polyline onto the centre of the painted line.

For every sample along the rough polyline (every `step` px of arc length) we read an intensity
profile along the normal (+-halfwin px), score "paint" (bright for white, R+G-2B for yellow),
and move the sample to the centroid of the paint pixels nearest to the rough line.
Samples without paint (gaps of a dashed line, occluders) are interpolated along the arc.
The result is simplified (Douglas-Peucker, tol px) and returned near->far as drawn.
"""
from __future__ import annotations

import math

import numpy as np
from PIL import Image

_cache: dict[str, np.ndarray] = {}


def load(path: str) -> np.ndarray:
    if path not in _cache:
        _cache[path] = np.asarray(Image.open(path).convert("RGB"), dtype=np.float32)
    return _cache[path]


def bilinear(img: np.ndarray, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
    h, w = img.shape[:2]
    xs = np.clip(xs, 0, w - 1.001)
    ys = np.clip(ys, 0, h - 1.001)
    x0 = np.floor(xs).astype(int)
    y0 = np.floor(ys).astype(int)
    fx = (xs - x0)[..., None]
    fy = (ys - y0)[..., None]
    a = img[y0, x0]
    b = img[y0, x0 + 1]
    c = img[y0 + 1, x0]
    d = img[y0 + 1, x0 + 1]
    return a * (1 - fx) * (1 - fy) + b * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy


def resample(pts: list[tuple[float, float]], step: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Points every `step` px along the polyline, their unit normals, and arc positions."""
    P = np.asarray(pts, dtype=float)
    seg = np.diff(P, axis=0)
    L = np.hypot(seg[:, 0], seg[:, 1])
    cum = np.concatenate([[0], np.cumsum(L)])
    s = np.arange(0, cum[-1] + 1e-9, step)
    if s[-1] < cum[-1] - 1e-6:
        s = np.append(s, cum[-1])
    out, nor = [], []
    for si in s:
        i = min(np.searchsorted(cum, si, side="right") - 1, len(L) - 1)
        t = (si - cum[i]) / L[i] if L[i] else 0
        out.append(P[i] + t * seg[i])
        dx, dy = seg[i] / (L[i] or 1)
        nor.append((-dy, dx))
    return np.asarray(out), np.asarray(nor), s


def score_profile(rgb: np.ndarray, color: str) -> np.ndarray:
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    if color == "yellow":
        return (r + g) / 2 - b + 0.15 * (r + g + b) / 3
    return (r + g + b) / 3


def snap(path: str, rough: list[tuple[float, float]], color: str = "white", halfwin: float = 10,
         step: float = 4, double: bool = False, min_contrast: float = 18, tol: float = 1.0,
         far_halfwin: float | None = None, debug: bool = False,
         pw_near: float = 0, pw_far: float = 0):
    img = load(path)
    S, N, arc = resample(rough, step)
    n = len(S)
    hw = np.linspace(halfwin, far_halfwin if far_halfwin is not None else halfwin, n)
    pwid = np.linspace(pw_near if pw_near else 0.8 * halfwin, pw_far if pw_far else 0.8 * hw[-1], n)
    found = np.full(n, np.nan)
    for i in range(n):
        k = int(math.ceil(hw[i]))
        pmax = max(1.5, pwid[i])
        best = None
        for pw in [x for x in (1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.5, 8.0, 10.0) if x <= pmax] or [pmax]:
            offs = np.arange(-k - 3 * pw - 2, k + 3 * pw + 2.5, 0.5)
            prof = score_profile(bilinear(img, S[i, 0] + offs * N[i, 0], S[i, 1] + offs * N[i, 1]), color)
            cs = np.concatenate([[0], np.cumsum(prof)])

            def boxmean(lo_, hi_):
                ia = np.clip(np.round((offs + lo_ - offs[0]) / 0.5), 0, len(prof) - 1).astype(int)
                ib = np.clip(np.round((offs + hi_ - offs[0]) / 0.5), 1, len(prof)).astype(int)
                ib = np.maximum(ib, ia + 1)
                return (cs[ib] - cs[ia]) / (ib - ia)

            # ridge: brighter than BOTH shoulders (rejects bright-background edges)
            ridge = prof - np.maximum(boxmean(-2.2 * pw - 2, -pw - 0.5), boxmean(pw + 0.5, 2.2 * pw + 2))
            inner = np.abs(offs) <= hw[i]
            peak = ridge[inner].max()
            if best is None or peak > best[0] * 1.08:
                best = (peak, offs, ridge, inner)
        peak, offs, ridge, inner = best
        if peak < min_contrast:
            continue
        thr = 0.5 * peak
        mask = (ridge >= thr) & inner
        if not double:
            j = int(np.argmax(np.where(inner, ridge, -1e9)))
            lo = j
            while lo - 1 >= 0 and mask[lo - 1]:
                lo -= 1
            hi = j
            while hi + 1 < len(mask) and mask[hi + 1]:
                hi += 1
            mask = np.zeros_like(mask)
            mask[lo:hi + 1] = True
        wts = (ridge - thr).clip(min=0) * mask
        if wts.sum() <= 0:
            continue
        found[i] = (offs * wts).sum() / wts.sum()
    ok = ~np.isnan(found)
    if ok.sum() < 2:
        raise ValueError(f"{path}: không tìm thấy vạch dọc polyline")
    # robust smoothing: median of neighbours, reject outliers
    f = found.copy()
    idx = np.where(ok)[0]
    med = np.array([np.median(found[idx[max(0, k - 3):k + 4]]) for k in range(len(idx))])
    bad = np.abs(found[idx] - med) > 2.5
    f[idx[bad]] = np.nan
    ok = ~np.isnan(f)
    idx = np.where(ok)[0]
    # outside the first/last detection: keep the rough line's own offset trend (extrapolate the nearest)
    f = np.interp(arc, arc[idx], f[idx])
    # light smoothing
    k = 2
    fs = np.array([f[max(0, i - k):i + k + 1].mean() for i in range(n)])
    P = S + fs[:, None] * N
    simp = dp(P, tol)
    if debug:
        return simp, found, S, N
    return [(round(float(x), 1), round(float(y), 1)) for x, y in simp]


def dp(P: np.ndarray, tol: float) -> np.ndarray:
    if len(P) <= 2:
        return P
    a, b = P[0], P[-1]
    ab = b - a
    L = np.hypot(*ab) or 1e-9
    d = np.abs(np.cross(ab, P - a)) / L
    i = int(np.argmax(d))
    if d[i] > tol:
        return np.vstack([dp(P[: i + 1], tol)[:-1], dp(P[i:], tol)])
    return np.vstack([a, b])


def coverage(path: str, pts, color="white", halfwin=4, step=4, min_contrast=18):
    """Fraction of samples along pts that sit on paint (diagnostic)."""
    img = load(path)
    S, N, _ = resample(pts, step)
    hits = 0
    for i in range(len(S)):
        offs = np.arange(-halfwin - 8, halfwin + 9, 1.0)
        prof = score_profile(bilinear(img, S[i, 0] + offs * N[i, 0], S[i, 1] + offs * N[i, 1]), color)
        inner = np.abs(offs) <= halfwin
        if prof[inner].max() - np.median(prof[~inner]) >= min_contrast:
            hits += 1
    return hits / len(S)
