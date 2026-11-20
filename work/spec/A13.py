from helpers import *

IMAGE = "A13_c179d309-b446fda3.jpg"
TAGS = tags("front", "day", "rain", "real")
L1 = [(318, 513), (338, 500), (361, 480), (386, 460), (413, 440), (444, 420), (462, 400), (478, 386)]
R1 = [(868, 622), (820, 585), (777, 555), (736, 527), (696, 500), (660, 468), (627, 436), (609, 425), (590, 400)]
R2 = [(1240, 566), (1176, 546), (1095, 523), (1014, 500), (975, 440 + 0), (935, 430)]
SHAPES = [
    lane(L1, "L1", "solid", "yellow", snap=False),
    lane(R1, "R1", "dashed", "white", halfwin=8, far_halfwin=4),
    lane([(1240, 566), (1176, 546), (1095, 523), (1014, 500), (960, 478), (905, 455), (860, 437)], "R2", "dashed", "white", halfwin=8, far_halfwin=4),
    drivable_between([(190, 622)] + L1, "R1", "direct", far=[(560, 370)], bottom=[(500, 622)]),
    drivable_between("R1", "R2", "alternative", far=[(640, 372)], bottom=[(1280, 575), (1280, 620)]),
]
