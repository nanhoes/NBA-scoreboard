# app.py

# also importing the request module
from flask import Flask, render_template, request
import sys,os
import configparser
import dbus

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"

dir = os.path.dirname(__file__)
filename = os.path.join(dir, '/home/pi/NBA-scoreboard/config/matrix_options.ini')

# Configuration for the matrix
config = configparser.ConfigParser()
config.read(filename)

sysbus = dbus.SystemBus()
systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')

# home route
@app.route("/")
def saved_config():
    # Brightness from config file
    brightness = int(config['DEFAULT']['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    NBA = config['DEFAULT']['NBA']
    starboard = config['DEFAULT']['starboard']
    animation = config['DEFAULT']['animation']
    return render_template('index.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, animation = animation)

# handling form data
@app.route('/brightness', methods=['POST'])
def handle_brightness():
    config.set('DEFAULT', 'brightness', request.form['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    NBA = config['DEFAULT']['NBA']
    starboard = config['DEFAULT']['starboard']
    animation = config['DEFAULT']['animation']
    if NBA == 'on':
        job = manager.RestartUnit('render.service', 'fail')
    if starboard == 'on':
        job = manager.RestartUnit('starboard.service', 'fail')
    if animation == 'on':
        job = manager.RestartUnit('animation.service', 'fail')
    with open(filename, 'wb') as configfile:
        config.write(configfile)
    return render_template('index.html', brightness = request.form['brightness'], width = width, height = height, NBA = NBA, starboard = starboard, animation = animation)

# handling form data
@app.route('/size', methods=['POST'])
def handle_size():
    config.set('DEFAULT', 'rows', request.form['width'])
    config.set('DEFAULT', 'columns', request.form['height'])
    brightness = int(config['DEFAULT']['brightness'])
    NBA = config['DEFAULT']['NBA']
    starboard = config['DEFAULT']['starboard']
    animation = config['DEFAULT']['animation']
    if NBA == 'on':
        job = manager.RestartUnit('render.service', 'fail')
    if starboard == 'on':
        job = manager.RestartUnit('starboard.service', 'fail')
    if animation == 'on':
        job = manager.RestartUnit('animation.service', 'fail')
    with open(filename, 'wb') as configfile:
        config.write(configfile)
    return render_template('index.html', brightness = brightness, width = int(request.form['width']), height = int(request.form['height']), NBA = NBA, starboard = starboard, animation = animation)

# handling NBA status
@app.route("/NBA", methods=["GET", "POST"])
def handle_NBA():
    NBA = request.form['NBA']
    brightness = int(config['DEFAULT']['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    starboard = config['DEFAULT']['starboard']
    animation = config['DEFAULT']['animation']
    config.set('DEFAULT', 'NBA', request.form['NBA'])
    if NBA == 'on':
      job = manager.StartUnit('render.service', 'replace')
      job = manager.StopUnit('starboard.service', 'replace')
      job = manager.StopUnit('animation.service', 'replace')
      starboard = request.form['starboard']   
      animation = request.form['animation']
      config.set('DEFAULT', 'starboard', request.form['starboard'])
      config.set('DEFAULT', 'animation', request.form['animation'])    
    else:
      job = manager.StopUnit('render.service', 'replace')
    return render_template('index.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, animation = animation)

# handling starboard status
@app.route("/starboard", methods=["GET", "POST"])
def handle_starboard():
    starboard = request.form['starboard']
    brightness = int(config['DEFAULT']['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    NBA = config['DEFAULT']['NBA']
    animation = config['DEFAULT']['animation']
    config.set('DEFAULT', 'starboard', request.form['starboard'])
    if starboard == 'on':
      job = manager.StartUnit('starboard.service', 'replace')
      job = manager.StopUnit('render.service', 'replace')
      job = manager.StopUnit('animation.service', 'replace')
    else:
      job = manager.StopUnit('starboard.service', 'replace')
    return render_template('index.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, animation = animation)

# handling animation status
@app.route("/animation", methods=["GET", "POST"])
def handle_animation():
    animation = request.form['animation']
    brightness = int(config['DEFAULT']['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    NBA = config['DEFAULT']['NBA']
    starboard = config['DEFAULT']['starboard']
    config.set('DEFAULT', 'animation', request.form['animation'])
    if animation == 'on':
      job = manager.StartUnit('animation.service', 'replace')
      job = manager.StopUnit('render.service', 'replace')
      job = manager.StopUnit('starboard.service', 'replace')
    else:
      job = manager.StopUnit('animation.service', 'replace')
    return render_template('index.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, animation = animation)

app.run(host='0.0.0.0', port=80) 
