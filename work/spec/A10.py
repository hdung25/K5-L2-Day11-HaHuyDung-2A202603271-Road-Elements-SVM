from helpers import *

IMAGE = "A10_b6ff1331-f6d3fba8.jpg"
TAGS = tags("front", "day", "rain", "real")
SHAPES = [
    lane([(78, 652), (180, 576), (280, 502), (380, 428), (431, 390), (478, 360), (519, 330)], "L2", "solid", "white", halfwin=9, far_halfwin=4),
    lane([(431, 604), (460, 545), (490, 482), (507, 450), (521, 420), (538, 388), (545, 375)], "R1" if False else "L1", "solid", "white", halfwin=9, far_halfwin=5),
    lane([(1190, 658), (1100, 605), (1020, 560), (952, 521), (870, 477), (776, 431), (762, 423)], "R1", "solid", "white", occluded=True, halfwin=7, far_halfwin=4),
    sign(46, 49, 90, 80, "prohibitory"),
    sign(48, 80, 91, 125, "prohibitory"),
    sign(48, 125, 94, 170, "prohibitory"),
    sign(440, 151, 455, 167, "other"),
    sign(423, 191, 448, 199, "information"),
    sign(441, 200, 456, 215, "supplementary"),
    sign(431, 225, 441, 238, "prohibitory"),
    sign(765, 190, 783, 204, "information"),
    drivable_between("L1", "R1", "direct", far=[(640, 300)], bottom=[(800, 606), (600, 604)]),
    drivable_between("L2", "L1", "alternative", far=[(540, 300)], bottom=[(250, 650)]),
]
