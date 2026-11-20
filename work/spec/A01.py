from helpers import *

IMAGE = "A01_bc5fadac-fa6dd225.jpg"
TAGS = tags("front", "day", "clear", "real")
SHAPES = [
    lane([(0, 600), (100, 571), (200, 545), (300, 516), (335, 506)], "L2", "solid", "white", "double", halfwin=8),
    lane([(108, 720), (190, 655), (283, 573), (318, 540), (340, 520), (356, 509)], "L1", "dashed", "white", halfwin=8, far_halfwin=4),
    lane([(657, 682), (640, 669), (575, 630), (520, 588), (485, 559), (455, 537), (430, 518)], "R1", "dashed", "white", halfwin=9, far_halfwin=4),
    lane([(1280, 704), (1100, 663), (1000, 639), (901, 615), (800, 590), (700, 565), (600, 543), (520, 525), (470, 512), (440, 505)], "R2", "solid", "yellow", snap=False),
    drivable_between("L1", "R1", "direct", far=[(395, 504)], bottom=[(700, 720)]),
    drivable_between("L2", "L1", "alternative", far=[(345, 503)], bottom=[(0, 720)]),
    drivable_between("R1", "R2", "alternative", far=[(436, 510)], bottom=[(1280, 720), (700, 720)]),
    sign(551, 408, 604, 481, "information"),
    sign(434, 464, 452, 487, "information"),
]
