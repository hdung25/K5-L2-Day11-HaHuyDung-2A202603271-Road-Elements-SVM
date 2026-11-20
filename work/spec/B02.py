from helpers import *

IMAGE = "B02_03177_FV.png"
TAGS = tags("fisheye_front", "day", "clear", "real")
# No painted lane line on this approach (zebra + curbs only): no L1/R1, lint QC1-02 expected.
SHAPES = [
    drivable([(140, 668), (230, 565), (310, 500), (420, 428), (470, 418), (560, 374), (700, 370), (830, 412), (950, 472),
              (1080, 560), (1160, 668), (1080, 680), (640, 672), (200, 672)], "direct"),
    light(100, 77, 160, 218, "unknown", facing="side", edge_zone=True),
    light(1077, 20, 1140, 170, "unknown", facing="side", edge_zone=True),
    light(1158, 100, 1200, 192, "unknown", facing="side", edge_zone=True),
    light(45, 363, 61, 391, "red", edge_zone=True),
    light(262, 347, 277, 368, "unknown", facing="back"),
]
