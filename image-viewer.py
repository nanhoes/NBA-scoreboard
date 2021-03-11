#!/usr/bin/env python
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image



image = Image.open("/home/pi/My-NBA-scoreboard/lal.png")

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 2
options.parallel = 2
options.disable_hardware_pulsing = True

matrix = RGBMatrix(options = options)

# Make image fit our screen.
#image.thumbnail((40, matrix.height))
#(left, upper, right, lower) = (20, 20, 100, 100)
#image.crop((left, upper, right, lower))
matrix.SetImage(image.convert('RGB'))

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)
