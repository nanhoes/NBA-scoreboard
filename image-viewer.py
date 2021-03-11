#!/usr/bin/env python
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import os
import json
import datetime as dt
import time
import sys
from PIL import Image, ImageFont, ImageDraw  



image = Image.open("/home/pi/My-NBA-scoreboard/lal.png")
image1 = Image.open("/home/pi/My-NBA-scoreboard/bkn.png")
draw = ImageDraw.Draw(image)  


# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 2
options.parallel = 2
options.disable_hardware_pulsing = True

font = graphics.Font()
font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf")
font2 = graphics.Font()
font2.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/8x13.bdf")
team_colors = {'ATL': [[225, 58, 62], [100, 100, 100]], 'BOS': [[0, 131, 72], [187, 151, 83]], 'BKN': [[100, 100, 100], [0, 0, 0]], 'CHA': [[29, 17, 96], [0, 140, 168]], 'CHI': [[206, 17, 65], [0, 0, 0]], 'CLE': [[134, 0, 56], [253, 187, 48]], 'DAL': [[0, 125, 197], [196, 206, 211]], 'DEN': [[77, 144, 205], [253, 185, 39]], 'DET': [[237, 23, 76], [0, 107, 182]], 'GSW': [[253, 185, 39], [0, 107, 182]], 'HOU': [[206, 17, 65], [196, 206, 211]], 'LAL': [[253, 185, 39], [85, 37, 130]], 'MEM': [[15, 88, 108], [190, 212, 233]], 'MIA': [[152, 0, 46], [0, 0, 0]], 'MIL': [[0, 71, 27], [240, 235, 210]], 'MIN': [[0, 80, 131], [0, 169, 79]], 'NOP': [[0, 43, 92], [227, 24, 55]], 'NYK': [[0, 107, 182], [245, 132, 38]], 'OKC': [[0, 125, 195], [240, 81, 51]], 'ORL': [[0, 125, 197], [0, 0, 0]], 'PHI': [[237, 23, 76], [0, 107, 182]], 'PHX': [[229, 96, 32], [29, 17, 96]], 'POR': [[224, 58, 62], [186, 195, 201]], 'SAC': [[114, 76, 159], [142, 144, 144]], 'SAS': [[186, 195, 201], [0, 0, 0]], 'TOR': [[206, 17, 65], [0, 0, 0]], 'UTA': [[0, 43, 92], [249, 160, 27]], 'WAS': [[0, 43, 92], [227, 24, 55]], 'IND': [[255, 198, 51], [0, 39, 93]], 'LAC': [[237, 23, 76], [0, 107, 182]]}

matrix = RGBMatrix(options = options)


# Make image fit our screen.
image.thumbnail((30, matrix.height))
matrix.SetImage(image.convert('RGB'),5,0)
image1.thumbnail((30, matrix.height))
matrix.SetImage(image1.convert('RGB'),93,0)

#graphics.DrawText(canvas, font2, 0, 0, graphics.Color(255, 255, 255), "LAL")
#for line in range(20,38):
 #   graphics.DrawLine(canvas, 0, line, 36, line, graphics.Color(255,0,0))    
#offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
draw.text((5,5),'LAL', font = font, align = "left")
   
try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)
