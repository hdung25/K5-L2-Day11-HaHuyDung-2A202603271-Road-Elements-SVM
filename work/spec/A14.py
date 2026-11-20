from helpers import *

IMAGE = "A14_ca04d99f-c1282bb7.jpg"
TAGS = tags("front", "night", "clear", "real")
L1 = [(311, 600), (340, 570), (369, 540), (398, 510), (427, 480), (439, 468)]
R1 = [(1280, 554), (1230, 538), (1177, 520), (1148, 510), (1124, 500), (1089, 490), (1057, 480), (1028, 470), (1001, 460), (985, 455)]
SHAPES = [
    lane(L1, "L1", "solid", "yellow", "double", snap=False),
    lane(R1, "R1", "solid", "white", halfwin=5, far_halfwin=4, min_contrast=10),
    drivable_between(L1, "R1", "direct", far=[(560, 440), (900, 440)], bottom=[(1280, 603), (800, 603)]),
    light(395, 118, 415, 163, "green"),
    light(414, 122, 432, 162, "unknown", facing="side"),
    light(753, 100, 775, 148, "green"),
    light(811, 176, 831, 222, "green"),
    light(502, 270, 517, 290, "green"),
    light(575, 276, 586, 291, "green"),
    light(1186, 252, 1208, 282, "red", type="pedestrian"),
]
