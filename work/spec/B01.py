from helpers import *

IMAGE = "B01_02688_FV.png"
TAGS = tags("fisheye_front", "day", "clear", "real")
L1 = [(88, 566), (110, 553), (140, 536), (170, 518), (200, 500), (230, 484), (260, 468), (290, 453), (320, 438), (350, 425), (380, 413), (410, 401)]
R1 = [(1212, 512), (1200, 504), (1160, 478), (1120, 460), (1080, 443), (1040, 427), (1000, 412), (960, 398)]
SHAPES = [
    lane(L1, "L1", "solid", "white", halfwin=8, far_halfwin=5, step=3),
    lane(R1, "R1", "solid", "white", halfwin=6, far_halfwin=4, step=3),
    crosswalk([(128, 688), (188, 625), (253, 566), (327, 512), (423, 452), (521, 396), (557, 379), (638, 377), (749, 381),
               (849, 433), (997, 574), (1160, 693), (1080, 678), (640, 670), (200, 670)]),
    # red-paved strip left of the zebra is a bike lane (NL): not drivable; direct starts at the grey asphalt edge
    drivable_between([(150, 670), (188, 625), (253, 566), (327, 512), (423, 452), (521, 396), (557, 379)], "R1", "direct",
                     far=[(640, 360), (760, 365)], bottom=[(1185, 690), (1080, 678), (640, 670), (200, 670)]),
]
