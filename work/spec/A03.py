from helpers import *

IMAGE = "A03_b1c66a42-6f7d68ca.jpg"
TAGS = tags("front", "day", "overcast", "real")
SHAPES = [
    lane([(238, 695), (272, 650), (310, 600), (345, 560), (390, 520), (435, 480), (470, 440), (505, 400), (527, 375)], "L1", "solid", "yellow", halfwin=9, far_halfwin=4),
    lane([(700, 467), (673, 446), (650, 428), (631, 414), (612, 400), (597, 386)], "R1", "dashed", "white", halfwin=5, far_halfwin=3),
    lane([(1280, 541), (1180, 523), (1090, 497), (1013, 486), (927, 471), (845, 455), (770, 440)], "R2", "dashed", "white", occluded=True, halfwin=5, far_halfwin=3),
    drivable_between("L1", [(983, 690), (700, 467), (597, 386)], "direct", far=[(560, 372)], bottom=[(600, 692)]),
    drivable_between([(983, 690), (700, 467), (597, 386)], "R2", "alternative", far=[(640, 395)], bottom=[(1280, 690)]),
]
