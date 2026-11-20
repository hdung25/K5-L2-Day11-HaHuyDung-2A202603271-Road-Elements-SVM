"""Minimal CVAT REST client (stdlib only) for the local CVAT at http://localhost:8080.

python work/cvat_api.py setup            # project d11-road-<name> + 4 tasks with images
python work/cvat_api.py upload ann.json  # replace job annotations from work/ann.json
python work/cvat_api.py finish           # set every job to stage acceptance / state completed
python work/cvat_api.py export OUTDIR    # CVAT for images 1.1 without images, per task group
"""
from __future__ import annotations

import base64
import json
import mimetypes
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CRED = dict(l.split("=", 1) for l in Path("D:/cvat-local/cvat_admin.local.txt").read_text().split())
BASE = CRED["url"].replace("localhost", "127.0.0.1")
AUTH = "Basic " + base64.b64encode(f"{CRED['user']}:{CRED['password']}".encode()).decode()
NAME = "hahuydung"
PROJECT = f"d11-road-{NAME}"
TASKS = {
    "front": [f"A{i:02d}" for i in range(1, 13)],
    "front-extra": [f"A{i:02d}" for i in range(13, 17)],
    "fisheye": [f"B{i:02d}" for i in range(1, 9)],
    "fisheye-extra": [f"B{i:02d}" for i in range(9, 13)],
}


def req(method: str, path: str, body=None, raw: bytes | None = None, ctype: str | None = None, ok=(200, 201, 202, 204)):
    url = (BASE + "/" + path.split("/", 3)[3]) if path.startswith("http") else BASE + path
    data = raw
    headers = {"Authorization": AUTH, "Accept": "application/vnd.cvat+json, */*", "Host": "localhost"}
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    if ctype:
        headers["Content-Type"] = ctype
    r = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(r, timeout=300) as resp:
            content = resp.read()
            if resp.status not in ok:
                raise RuntimeError(f"{method} {path}: {resp.status}")
            ct = resp.headers.get("Content-Type", "")
            return json.loads(content) if content and "json" in ct else content
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{method} {path}: {e.code} {e.read()[:500]!r}") from None


def paged(path: str):
    out, url = [], path + ("&" if "?" in path else "?") + "page_size=100"
    while url:
        r = req("GET", url)
        out += r["results"]
        url = r.get("next")
    return out


def image_files(slots):
    files = {p.name[:3]: p for p in (ROOT / "data").iterdir()}
    return [files[s] for s in slots]


def multipart(fields: list[tuple[str, str]], files: list[Path]) -> tuple[bytes, str]:
    b = uuid.uuid4().hex
    parts = []
    for k, v in fields:
        parts.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    for i, f in enumerate(files):
        mt = mimetypes.guess_type(f.name)[0] or "application/octet-stream"
        parts.append(f'--{b}\r\nContent-Disposition: form-data; name="client_files[{i}]"; filename="{f.name}"\r\n'
                     f"Content-Type: {mt}\r\n\r\n".encode() + f.read_bytes() + b"\r\n")
    parts.append(f"--{b}--\r\n".encode())
    return b"".join(parts), f"multipart/form-data; boundary={b}"


def project():
    for p in paged(f"/api/projects?name={PROJECT}"):
        if p["name"] == PROJECT:
            return p
    return None


def setup():
    p = project()
    if p is None:
        labels = json.loads((ROOT / "configs/road_v1_labels.json").read_text(encoding="utf-8"))
        p = req("POST", "/api/projects", {"name": PROJECT, "labels": labels})
        print("project", p["id"], PROJECT)
    tasks = {t["name"]: t for t in paged(f"/api/tasks?project_id={p['id']}")}
    for tname, slots in TASKS.items():
        if tname in tasks:
            print("task exists", tname, tasks[tname]["id"])
            continue
        t = req("POST", "/api/tasks", {"name": tname, "project_id": p["id"]})
        files = image_files(slots)
        body, ct = multipart([("image_quality", "95"), ("sorting_method", "predefined"),
                              *[(f"server_files_order[{i}]", f.name) for i, f in enumerate(files)]], files)
        rq = req("POST", f"/api/tasks/{t['id']}/data", raw=body, ctype=ct)
        rid = rq.get("rq_id") if isinstance(rq, dict) else None
        while rid:
            s = req("GET", f"/api/requests/{rid}")
            if s["status"] in ("finished", "failed"):
                if s["status"] == "failed":
                    raise RuntimeError(s)
                break
            time.sleep(1.5)
        print("task", tname, t["id"], [f.name for f in files])


def frames_of(task_id: int) -> dict[str, int]:
    meta = req("GET", f"/api/tasks/{task_id}/data/meta")
    return {f["name"]: i for i, f in enumerate(meta["frames"])}


def label_ids(project_id: int):
    out = {}
    for lb in paged(f"/api/labels?project_id={project_id}"):
        out[lb["name"]] = {"id": lb["id"], "attrs": {a["name"]: a["id"] for a in lb["attributes"]}}
    return out


def upload(ann_path: str):
    ann = json.loads(Path(ann_path).read_text(encoding="utf-8"))
    p = project()
    L = label_ids(p["id"])
    for t in paged(f"/api/tasks?project_id={p['id']}"):
        fr = frames_of(t["id"])
        shapes, tags = [], []
        for name, idx in fr.items():
            a = ann.get(name)
            if not a:
                continue
            for label, value in a["tags"].items():
                lb = L[label]
                tags.append({"frame": idx, "label_id": lb["id"], "group": 0, "source": "manual",
                             "attributes": [{"spec_id": lb["attrs"]["value"], "value": value}]})
            for s in a["shapes"]:
                lb = L[s["label"]]
                attrs = [{"spec_id": lb["attrs"][k], "value": str(v).lower() if isinstance(v, bool) else v}
                         for k, v in s.get("attributes", {}).items()]
                pts = [c for xy in s["points"] for c in xy]
                shapes.append({"type": s["type"], "frame": idx, "label_id": lb["id"], "group": 0, "source": "manual",
                               "occluded": bool(s.get("occluded", False)), "outside": False, "z_order": s.get("z", 0),
                               "rotation": 0.0, "points": pts, "attributes": attrs})
        for job in paged(f"/api/jobs?task_id={t['id']}"):
            req("PUT", f"/api/jobs/{job['id']}/annotations", {"version": 0, "tags": tags, "shapes": shapes, "tracks": []})
            print("uploaded", t["name"], "job", job["id"], len(tags), "tags", len(shapes), "shapes")


def finish():
    p = project()
    for t in paged(f"/api/tasks?project_id={p['id']}"):
        for job in paged(f"/api/jobs?task_id={t['id']}"):
            req("PATCH", f"/api/jobs/{job['id']}", {"stage": "acceptance", "state": "completed"})
            print("job", job["id"], t["name"], "-> completed")


def export_job(job_id: int, out: Path):
    rq = req("POST", f"/api/jobs/{job_id}/dataset/export?format=CVAT+for+images+1.1&save_images=false")
    rid = rq["rq_id"]
    while True:
        s = req("GET", f"/api/requests/{rid}")
        if s["status"] == "finished":
            data = req("GET", s["result_url"])
            out.write_bytes(data)
            return
        if s["status"] == "failed":
            raise RuntimeError(s)
        time.sleep(1.5)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "setup":
        setup()
    elif cmd == "upload":
        upload(sys.argv[2])
    elif cmd == "finish":
        finish()
    elif cmd == "info":
        p = project()
        print(json.dumps({"project": p["id"], "tasks": [(t["name"], t["id"], [(j["id"], j["state"], j["stage"]) for j in paged(f"/api/jobs?task_id={t['id']}")]) for t in paged(f"/api/tasks?project_id={p['id']}")]}, indent=1))
    elif cmd == "export":
        outdir = Path(sys.argv[2])
        outdir.mkdir(parents=True, exist_ok=True)
        p = project()
        for t in paged(f"/api/tasks?project_id={p['id']}"):
            for job in paged(f"/api/jobs?task_id={t['id']}"):
                export_job(job["id"], outdir / f"{t['name']}.zip")
                print("exported", t["name"])
