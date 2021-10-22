import sys,os
import configparser

dir = os.path.dirname(__file__)
filename = os.path.join(dir, '/home/pi/NBA-scoreboard/config/matrix_options.ini')

# Configuration for the matrix
config = configparser.ConfigParser()
config.read(filename)

def update():
    config.set('DEFAULT', 'update', "YES")
    brightness = int(config['DEFAULT']['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    NBA = config['DEFAULT']['NBA']
    starboard = config['DEFAULT']['starboard']
    conway = config['DEFAULT']['conway']
    gif = config['DEFAULT']['gif']
    with open(filename, 'w') as configfile:
        config.write(configfile)

def no_update():
    config.set('DEFAULT', 'update', "NO")
    brightness = int(config['DEFAULT']['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    NBA = config['DEFAULT']['NBA']
    starboard = config['DEFAULT']['starboard']
    conway = config['DEFAULT']['conway']
    gif = config['DEFAULT']['gif']
    with open(filename, 'w') as configfile:
        config.write(configfile)

if __name__ == "__main__":
    no_update()
