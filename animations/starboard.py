from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from time import sleep
import random
import colorsys
import configparser
import os

# Configuration file
dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../config/matrix_options.ini')

# Configuration for the matrix
config = configparser.ConfigParser()
config.read(filename)

options = RGBMatrixOptions()
options.rows = int(config['DEFAULT']['rows'])
options.cols = int(config['DEFAULT']['columns'])
options.chain_length = int(config['DEFAULT']['chain_length'])
options.parallel = int(config['DEFAULT']['parallel'])
options.hardware_mapping = config['DEFAULT']['hardware_mapping']
options.gpio_slowdown = int(config['DEFAULT']['gpio_slowdown'])
options.brightness = int(config['DEFAULT']['brightness'])
options.row_address_type = int(config['DEFAULT']['row_address_type'])
options.pwm_bits = 11

mode = 1
if options.chain_length == 3:
    maxdrops = random.randint(100, 200) # Amount of stars
else:
    maxdrops = random.randint(20, 75) # Amount of stars

class Drop:
    def __init__(self):
        global mode
        self.x = 0
        self.y = random.randint(0, options.rows*options.parallel - 1)
        self.r = self.b = self.g = 0
        self.generateColor()
        if options.chain_length == 3:
            self.speed = 1 + (random.random() * 2)
        else:
            self.speed = 1 + (random.random() * .5)
        self.strength = random.randint(40, 100)/100.0
    def generateColor(self):
        (r, g, b) = colorsys.hsv_to_rgb(random.random(), 1, 1)
        if (mode == 0):
            (r, g, b) = colorsys.hsv_to_rgb((self.y / 31.0), 1, 1)
        #mode == 2 leaves it at hsv
        self.r = int(r * 255)
        self.g = int(g * 255)
        self.b = int(b * 255)

        if (mode == 1):
            self.r = random.randint(0, 255)
            self.g = random.randint(0, 255)
            self.b = random.randint(0, 255)
        self.altr = int(r * 255)
        self.altg = int(g * 255)
        self.altb = int(b * 255)
        if (random.random() > .01 and mode == 3):
            self.r = self.g = self.b = random.randint(0, 255)

    def tick(self):
        self.erase()
        self.x += (self.speed / 2.0)
        if self.x > options.cols*options.chain_length - 1:
            self.x = options.cols*options.chain_length - 1
            self.strength = 0
        self.strength = self.strength * .977
        if (self.strength < 0):
            self.strength = 0
        self.draw()
    def draw(self):
        matrix.SetPixel(self.x, self.y, self.b*(self.strength), self.g*(self.strength), self.r*(self.strength))
        if (random.random() < .001):
            matrix.SetPixel(self.x, self.y, self.altb, self.altg, self.altr)

    def erase(self):
        matrix.SetPixel(self.x, self.y, 0, 0, 0)

matrix = RGBMatrix(options = options)
print ("Matrix initialized\n")


drops = []
for k in range (0, maxdrops):
    drops.append(Drop())

modeTicks = 1000
while (True):
    for j in range(0, len(drops)):
        drops[j].tick()
        if drops[j].strength == 0:
           drops[j].erase()
           drops[j] = Drop()

    sleep(.01)
    modeTicks -= 1
    if modeTicks < 0:
        modeTicks = 10000
        mode += 1
        mode = mode % 4
