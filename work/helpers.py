"""Small constructors used by work/spec/*.py."""


def tags(camera="front", timeofday="day", weather="clear", source="real"):
    return {"camera": camera, "timeofday": timeofday, "weather": weather, "source": source}


def lane(pts, position, style="solid", color="white", kind="single", occluded=False, snap=True, key=None, **snapkw):
    sk = None
    if snap:
        sk = {"color": "yellow" if color == "yellow" else "white", "double": kind == "double"}
        sk.update(snapkw)
    return {"label": "lane", "pts": pts, "attrs": {"position": position, "style": style, "color": color, "kind": kind},
            "occluded": occluded, "snap": sk, "key": key}


def curb(pts, snap=None, key="curb"):
    return {"label": "road_curb", "pts": pts, "snap": snap, "key": key}


def drivable(pts, area_type="direct"):
    return {"label": "drivable", "pts": pts, "attrs": {"area_type": area_type}}


def crosswalk(pts):
    return {"label": "crosswalk", "pts": pts}


def light(x0, y0, x1, y1, color, type="vehicle", facing="front", edge_zone=False):
    return {"label": "traffic_light", "pts": [(x0, y0), (x1, y1)],
            "attrs": {"color": color, "type": type, "facing": facing, "edge_zone": edge_zone}}


def sign(x0, y0, x1, y1, group, facing="front", edge_zone=False):
    return {"label": "traffic_sign", "pts": [(x0, y0), (x1, y1)],
            "attrs": {"group": group, "facing": facing, "edge_zone": edge_zone}}


def drivable_between(left, right, area_type="direct", far=(), bottom=(), left_pre=(), ymax=1e9):
    """Polygon: left polyline (near->far) + far pts + right polyline (far->near) + bottom pts (right->left).
    left/right: lane position name ("L1"), a key=..., or an explicit point list."""
    return {"between": (left, right), "area_type": area_type, "far": list(far), "bottom": list(bottom),
            "left_pre": list(left_pre), "ymax": ymax}


def double_center(image, rough_a, rough_b, color="yellow", step_y=6, **kw):
    """Snap each line of a double marking separately, return the centre line (near->far, by y)."""
    import numpy as np
    from pathlib import Path
    import snap as _snap
    path = str(Path(__file__).resolve().parents[1] / "data" / image)
    a = _snap.snap(path, rough_a, color=color, tol=0.5, **kw)
    b = _snap.snap(path, rough_b, color=color, tol=0.5, **kw)

    def xy(p):
        p = sorted(p, key=lambda t: t[1])
        return np.array([t[1] for t in p]), np.array([t[0] for t in p])
    ya, xa = xy(a)
    yb, xb = xy(b)
    lo, hi = max(ya.min(), yb.min()), min(ya.max(), yb.max())
    ys = np.arange(hi, lo - 1e-6, -step_y)
    pts = [((np.interp(y, ya, xa) + np.interp(y, yb, xb)) / 2, y) for y in ys]
    P = _snap.dp(np.array(pts), 0.8)
    return [(round(float(x), 1), round(float(y), 1)) for x, y in P]
