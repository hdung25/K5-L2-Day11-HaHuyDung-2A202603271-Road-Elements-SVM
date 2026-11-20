from helpers import *

IMAGE = "A09_c7e6d5d1-c8af9fe3.jpg"
TAGS = tags("front", "day", "clear", "real")
SHAPES = [
    lane([(447, 655), (446, 610), (445, 580), (443, 540), (442, 510), (444, 485), (450, 462), (457, 450)], "L2", "solid", "white", "double", snap=False),
    lane([(526, 655), (548, 622), (584, 567), (603, 536), (624, 507), (642, 482), (660, 447), (668, 433)], "L1", "dashed", "white", halfwin=8, far_halfwin=4),
    sign(832, 318, 850, 347, "information"),
    sign(312, 276, 326, 322, "other", facing="back"),
    drivable_between("L1", [(1280, 662), (1150, 600), (1000, 535), (880, 480), (790, 440), (740, 420)], "direct", far=[(700, 418)], bottom=[(800, 663)]),
]
