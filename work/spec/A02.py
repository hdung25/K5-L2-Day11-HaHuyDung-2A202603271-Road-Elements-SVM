from helpers import *

IMAGE = "A02_b3c26aff-63a0d7d6.jpg"
TAGS = tags("front", "day", "clear", "real")
SHAPES = [
    lane([(0, 586), (100, 554), (200, 523), (295, 497), (410, 457), (465, 442), (510, 424), (545, 410)], "L2", "dashed", "white", halfwin=7, far_halfwin=4),
    lane([(380, 720), (450, 634), (504, 567), (565, 492), (588, 457), (597, 440), (600, 420)], "L1", "dashed", "white", halfwin=7, far_halfwin=4),
    lane([(1160, 720), (1080, 667), (990, 603), (900, 541), (820, 493), (740, 450), (700, 432), (675, 421), (650, 410)], "R1", "solid", "white", halfwin=9, far_halfwin=2.5),
    drivable_between("L1", "R1", "direct", far=[(622, 404)]),
    drivable_between("L2", "L1", "alternative", far=[(572, 404)], bottom=[(0, 720)]),
]
