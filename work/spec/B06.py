from helpers import *

IMAGE = "B06_04068_MVL.png"
TAGS = tags("fisheye_left", "day", "clear", "real")
LA = [(219, 277), (247, 248), (278, 214), (310, 186), (340, 161), (372, 140), (405, 122), (448, 103)]
LB = [(1150, 760), (1130, 720), (1110, 688), (1090, 655), (1068, 625), (1045, 595), (1020, 568), (990, 540), (960, 515), (930, 495)]
SHAPES = [
    lane(LB, "other", "solid", "white", halfwin=7, far_halfwin=6, step=3, key="B"),
    lane(LA, "other", "dashed", "white", halfwin=5, far_halfwin=3, step=3, key="A"),
    drivable([(170, 300)] + LA + [(560, 110), (760, 160), (880, 230), (900, 330), (890, 380)] + LB[::-1] +
             [(1110, 790), (1000, 740), (800, 660), (600, 560), (400, 420), (250, 320)], "direct"),
]
