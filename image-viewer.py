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
#image.thumbnail((30, matrix.height))

#matrix.SetImage(image.convert('RGB'))
matrix.SetImage(image)

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)
