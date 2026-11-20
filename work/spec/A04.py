from helpers import *

IMAGE = "A04_b7a8e795-0ff55db2.jpg"
TAGS = tags("front", "day", "overcast", "real")
HOOD = [(1280, 548), (1100, 541), (900, 536), (700, 534), (500, 535), (300, 538), (100, 545), (40, 548)]
SHAPES = [
    lane([(40, 544), (150, 501), (300, 443), (440, 389), (500, 366), (550, 346)], "L1", "solid", "yellow", "double", halfwin=12, far_halfwin=6),
    lane([(728, 534), (705, 510), (684, 487), (638, 393), (621, 357), (612, 340), (607, 330)], "R1", "dashed", "white", halfwin=7, far_halfwin=3),
    lane([(1280, 536), (1240, 523), (1180, 504), (1120, 485), (1060, 466), (1000, 447), (940, 429), (880, 410), (820, 390), (760, 370), (710, 353), (680, 342)], "R2", "solid", "white", halfwin=4, far_halfwin=3),
    drivable_between("L1", "R1", "direct", far=[(600, 327)], bottom=[(700, 534), (500, 535), (300, 538), (100, 545)]),
    drivable_between("R1", "R2", "alternative", bottom=[(900, 536)], far=[(640, 330)]),
]
