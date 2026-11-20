"""Merge two CVAT-for-images-1.1 job exports (core + extra task) into one zip, renumbering image ids.
python work/merge_export.py OUT.zip CORE.zip EXTRA.zip"""
import sys
import zipfile
import xml.etree.ElementTree as ET

out, core, extra = sys.argv[1:4]
root = ET.fromstring(zipfile.ZipFile(core).read("annotations.xml"))
n = len(root.findall("image"))
for im in ET.fromstring(zipfile.ZipFile(extra).read("annotations.xml")).findall("image"):
    im.set("id", str(n))
    n += 1
    root.append(im)
size = root.find("meta/job/size")
if size is not None:
    size.text = str(n)
data = b'<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(root, encoding="utf-8")
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("annotations.xml", data)
print(out, n, "images")
