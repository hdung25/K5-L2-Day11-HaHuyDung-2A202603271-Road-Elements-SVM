from helpers import *

IMAGE = "B09_02686_FV.png"
TAGS = tags("fisheye_front", "day", "clear", "real")
# No traffic light / traffic sign facing the road in this frame (signs at the right are shop signs); no lane paint.
BODY = [(1073, 667), (800, 712), (640, 722), (545, 712), (300, 680), (132, 679)]
SHAPES = [
    crosswalk([(69, 597), (113, 562), (181, 518), (265, 472), (347, 435), (537, 426), (662, 425), (780, 429), (797, 432), (864, 479),
               (911, 516), (979, 574)] + BODY + [(103, 650), (83, 626)]),
    drivable([(83, 626), (69, 597), (180, 500), (280, 425), (350, 405), (450, 372), (600, 360), (720, 362), (840, 412), (900, 470),
              (980, 540), (1080, 650)] + BODY, "direct"),
]
