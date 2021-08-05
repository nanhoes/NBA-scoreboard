# app.py

# also importing the request module
from flask import Flask, render_template, request
import sys,os
import configparser
import dbus

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"

dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../../config/matrix_options.ini')

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
    power = config['DEFAULT']['power']
    return render_template('index.html', brightness = brightness, width = width, height = height, power = power)

# handling power status
@app.route("/power", methods=["GET", "POST"])
def handle_power():
    power = request.form['power']
    brightness = int(config['DEFAULT']['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    config.set('DEFAULT', 'power', request.form['power'])
    if power == 'on':
      job = manager.StartUnit('render.service', 'replace')
    else:
      job = manager.StopUnit('render.service', 'replace')
    return render_template('index.html', brightness = brightness, width = width, height = height, power = power)

# handling form data
@app.route('/brightness', methods=['POST'])
def handle_brightness():
    config.set('DEFAULT', 'brightness', request.form['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    power = config['DEFAULT']['power']
    with open(filename, 'wb') as configfile:
        config.write(configfile)
    job = manager.RestartUnit('render.service', 'fail')
    return render_template('index.html', brightness = request.form['brightness'], width = width, height = height, power = power)

# handling form data
@app.route('/size', methods=['POST'])
def handle_size():
    config.set('DEFAULT', 'rows', request.form['width'])
    config.set('DEFAULT', 'columns', request.form['height'])
    brightness = int(config['DEFAULT']['brightness'])
    power = config['DEFAULT']['power']
    with open(filename, 'wb') as configfile:
        config.write(configfile)
    job = manager.RestartUnit('render.service', 'fail')
    return render_template('index.html', brightness = brightness, width = int(request.form['width']), height = int(request.form['height']), power = power)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80) 
