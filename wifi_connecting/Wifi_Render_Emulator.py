#!/usr/bin/python3

from RGBMatrixEmulator import graphics, RGBMatrix, RGBMatrixOptions
import os
import sys
import signal
import configparser
import datetime as dt
import time
import socket
from PIL import Image, ImageChops

class Render:
    def __init__(self):
        
        # Configuration file
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, '/home/pi/NBA-scoreboard/config/matrix_options.ini')

        # Configuration for the matrix
        config = configparser.ConfigParser()
        config.read(filename)

        self.options = RGBMatrixOptions()
        self.options.hardware_mapping = 'regular'
        self.options.gpio_slowdown = 3
        self.options.rows = 32
        self.options.cols = 64
        self.options.drop_privileges = False

        self.path = '/Users/nanhoes/NBAscoreboard02/home/pi/NBAscoreboard/'

        self.font = graphics.Font()
        self.font.LoadFont("/Users/nanhoes/NBAscoreboard02/home/pi/NBAscoreboard/rpi-rgb-led-matrix/fonts/6x12.bdf")
        self.font2 = graphics.Font()
        self.font2.LoadFont("/Users/nanhoes/NBAscoreboard02/home/pi/NBAscoreboard/rpi-rgb-led-matrix/fonts/4x6.bdf")
        self.font3 = graphics.Font()
        self.font3.LoadFont("/Users/nanhoes/NBAscoreboard02/home/pi/NBAscoreboard/rpi-rgb-led-matrix/fonts/5x8.bdf")


    def Wifi_Not_Connected(self, printer=False):
        matrix = RGBMatrix(options=self.options)
        canvas1 = matrix.CreateFrameCanvas()
        textColor1 = graphics.Color(255, 255, 255)
        textColor2 = graphics.Color(0, 0, 255)
        pos = canvas1.width
        text1 = "CONNECT TO NETWORK "
        text2 = "NBA-WIFI-SETUP"
        text3 = " FROM YOUR PHONE"
        image_file1 = '/home/pi/NBA-scoreboard/board_images/nba.png'
        image_file2 = '/home/pi/NBA-scoreboard/board_images/wifi.png'

        while True:
            self.image = Image.open(image_file1).convert('RGB')
            self.image.thumbnail((18, 18), Image.ANTIALIAS)
            canvas1.SetImage(self.image, 18, 4)

            self.image = Image.open(image_file2).convert('RGB')
            self.image.thumbnail((20, 20), Image.ANTIALIAS)
            canvas1.SetImage(self.image, 33, 5)

            # Clear scrolling text
            for line in range(0,64):
                graphics.DrawLine(canvas1, line, 21, line, 31, graphics.Color(0, 0, 0))

            length = graphics.DrawText(canvas1, self.font, pos, 31, textColor1, text1) + graphics.DrawText(canvas1, self.font, pos+len(text1)*5, 31, textColor2, text2) + graphics.DrawText(canvas1, self.font, pos+len(text2+text1)*5, 31, textColor1, text3)
            pos -= 1
            if (pos + length < 0):
                pos = canvas1.width

            canvas1 = matrix.SwapOnVSync(canvas1)
            time.sleep(0.04)

    def Wifi_Connected(self, printer=False):
        matrix = RGBMatrix(options=self.options)
        canvas1 = matrix.CreateFrameCanvas()
        textColor1 = graphics.Color(255, 255, 255)
        textColor2 = graphics.Color(0, 0, 255)
        pos = canvas1.width
        hname = socket.gethostname()
        text1 = "CONNECTED! GO TO "
        text2 = hname.upper() + ".LOCAL:6969"
        text3 = " AND ADD SITE TO YOUR HOME SCREEN"
        image_file1 = '/home/pi/NBA-scoreboard/board_images/nba.png'
        image_file2 = '/home/pi/NBA-scoreboard/board_images/wifi_green.png'

        while True:
            self.image = Image.open(image_file1).convert('RGB')
            self.image.thumbnail((18, 18), Image.ANTIALIAS)
            canvas1.SetImage(self.image, 18, 4)

            self.image = Image.open(image_file2).convert('RGB')
            self.image.thumbnail((20, 20), Image.ANTIALIAS)
            canvas1.SetImage(self.image, 33, 5)

            # Clear scrolling text
            for line in range(0,64):
                graphics.DrawLine(canvas1, line, 21, line, 31, graphics.Color(0, 0, 0))

            length = graphics.DrawText(canvas1, self.font, pos, 31, textColor1, text1) + graphics.DrawText(canvas1, self.font, pos+len(text1)*5, 31, textColor2, text2) + graphics.DrawText(canvas1, self.font, pos+len(text1+text2)*5, 31, textColor1, text3)
            pos -= 1
            if (pos + length < 0):
                pos = canvas1.width

            canvas1 = matrix.SwapOnVSync(canvas1)
            time.sleep(0.04)

if __name__=='__main__':
    while True:
        Render().Wifi_Not_Connected()
        Render().Wifi_Connected()
