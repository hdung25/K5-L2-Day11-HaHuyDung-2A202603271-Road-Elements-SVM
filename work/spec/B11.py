from helpers import *

IMAGE = "B11_07282_RV.png"
TAGS = tags("fisheye_rear", "day", "overcast", "real")
# Car park: only parking-bay / hatch markings, no longitudinal lane line -> no lane (bay lines are not lanes).
SHAPES = [
    drivable([(60, 505), (100, 420), (170, 352), (260, 335), (345, 400), (455, 440), (545, 488), (700, 530), (920, 588),
              (700, 598), (400, 588), (170, 560)], "direct"),
]
