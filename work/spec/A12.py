from helpers import *

IMAGE = "A12_c0f978fa-9b4e623f.jpg"
TAGS = tags("front", "day", "clear", "real")
L1 = [(408, 434), (420, 428), (431, 422), (442, 416), (454, 410), (464, 404), (475, 398), (481, 395)]
R1 = [(566, 434), (564, 428), (559, 418), (555, 410), (551, 400), (548, 392)]
SHAPES = [
    lane(L1, "L1", "solid", "white", halfwin=4, far_halfwin=3),
    lane(R1, "R1", "dashed", "white", halfwin=4, far_halfwin=3),
    curb([(1280, 480), (1120, 476), (1000, 466), (950, 458), (870, 447)]),
    crosswalk([(0, 452), (200, 444), (420, 440), (760, 440), (900, 443), (955, 450), (960, 470), (700, 469), (400, 470), (200, 474), (0, 479)]),
    drivable_between([(0, 648), (0, 613)] + L1, [(636, 616)] + R1, "direct", far=[(525, 385)], bottom=[(400, 620), (150, 635)]),
    drivable_between([(636, 616)] + R1, [(1280, 700), (1280, 597), (1000, 515), (860, 470), (760, 440), (700, 410)], "alternative", far=[(575, 386)], bottom=[(1000, 660), (850, 628)]),
    light(747, 48, 768, 114, "green"),
    light(724, 58, 751, 121, "unknown", facing="side"),
    light(965, 287, 1002, 315, "green", type="pedestrian"),
    sign(967, 232, 1013, 246, "information"),
    sign(940, 253, 987, 271, "mandatory"),
    sign(719, 305, 730, 319, "information"),
    sign(0, 275, 16, 293, "mandatory"),
]
