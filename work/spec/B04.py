from helpers import *

IMAGE = "B04_05535_RV.png"
TAGS = tags("fisheye_rear", "day", "overcast", "real")
L1 = [(517, 321), (536, 310), (555, 300), (570, 288), (582, 278), (592, 268)]
SHAPES = [
    lane(L1, "L1", "dashed", "white", halfwin=4, far_halfwin=3, step=3),
    crosswalk([(115, 615), (245, 543), (385, 524), (540, 494), (700, 474), (850, 459), (935, 453), (980, 455), (1060, 525), (1140, 630),
               (1060, 668), (900, 706), (600, 708), (430, 700), (250, 665)]),
    # direct stops at the body edge of the own car; bus lane (left, "BUS") is not part of it
    drivable_between([(250, 662), (300, 560), (353, 480), (430, 400), (500, 345)] + L1,
                     [(1165, 615), (1140, 560), (1080, 495), (1000, 430), (900, 370), (800, 318), (700, 278)], "direct",
                     far=[(615, 262), (650, 263)], bottom=[(1060, 668), (900, 706), (600, 708), (430, 700)]),
]
