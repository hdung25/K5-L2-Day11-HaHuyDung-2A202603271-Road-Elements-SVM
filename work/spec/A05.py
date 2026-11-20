from helpers import *

IMAGE = "A05_b2576c8c-2de20b8a.jpg"
TAGS = tags("front", "day", "overcast", "real")
# No painted lane line on this street: no L1/R1 (lint QC1-02 expected; waiver per guide section 6).
SHAPES = [
    curb([(1280, 426), (1200, 411), (1110, 397), (1040, 386), (990, 372), (950, 358), (915, 345)]),
    drivable([(0, 545), (0, 415), (100, 392), (200, 369), (300, 346), (425, 316), (520, 292), (600, 273),
              (640, 268), (680, 272), (705, 285), (735, 300), (790, 333), (900, 395), (1020, 462), (1144, 533),
              (960, 536), (640, 533), (320, 537)], "direct"),
]
