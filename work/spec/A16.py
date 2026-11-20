from helpers import *

IMAGE = "A16_b6f77fda-33d2260f.jpg"
TAGS = tags("front", "dusk", "overcast", "real")
SHAPES = [
    lane([(352, 532), (383, 503), (412, 476), (440, 432), (463, 392), (473, 377)], "L1", "dashed", "white", halfwin=6, far_halfwin=3),
    lane([(985, 545), (930, 516), (880, 490), (820, 455), (761, 421), (730, 396), (712, 383)], "R1", "dashed", "white", occluded=True, halfwin=6, far_halfwin=3),
    crosswalk([(262, 340), (470, 342), (655, 346), (800, 350), (856, 355), (856, 372), (250, 370)]),
    drivable_between("L1", "R1", "direct", far=[(560, 300), (640, 300)], bottom=[(640, 540)]),
    light(764, 104, 786, 152, "green"),
    light(374, 152, 395, 188, "green"),
    light(595, 228, 608, 246, "green"),
    light(487, 232, 498, 246, "green"),
    light(852, 244, 880, 262, "red", type="pedestrian"),
]
