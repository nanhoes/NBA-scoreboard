# app.py
##
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
    conway = config['DEFAULT']['conway']
    gif = config['DEFAULT']['gif']
    update = config['DEFAULT']['update']
    if update == "YES":
        return render_template('index_update.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update)
    else:
        return render_template('index.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update)

# handling form data
@app.route('/brightness', methods=['POST'])
def brightness():
    update = config['DEFAULT']['update']
    config.set('DEFAULT', 'brightness', request.form['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    NBA = config['DEFAULT']['NBA']
    starboard = config['DEFAULT']['starboard']
    conway = config['DEFAULT']['conway']
    gif = config['DEFAULT']['gif']
    if NBA == 'ON':
        job = manager.RestartUnit('NBA.service', 'fail')
    else:
        pass
    if starboard == 'ON':
        job = manager.RestartUnit('starboard.service', 'fail')
    else:
        pass
    if conway == 'ON':
        job = manager.RestartUnit('conway.service', 'fail')
    if gif == 'ON':
        job = manager.RestartUnit('gif.service', 'fail')
    else:
        pass
    with open(filename, 'wb') as configfile:
        config.write(configfile)
    if update == "YES":
        return render_template('index_update.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update)
    else:
        return render_template('index.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update)

# handling form data
@app.route('/size', methods=['POST'])
def size():
    update = config['DEFAULT']['update']
    config.set('DEFAULT', 'rows', request.form['width'])
    config.set('DEFAULT', 'columns', request.form['height'])
    brightness = int(config['DEFAULT']['brightness'])
    NBA = config['DEFAULT']['NBA']
    starboard = config['DEFAULT']['starboard']
    conway = config['DEFAULT']['conway']
    gif = config['DEFAULT']['gif']
    if NBA == 'ON':
        job = manager.RestartUnit('NBA.service', 'fail')
    if starboard == 'ON':
        job = manager.RestartUnit('starboard.service', 'fail')
    if conway == 'ON':
        job = manager.RestartUnit('conway.service', 'fail')
    if gif == 'ON':
        job = manager.RestartUnit('gif.service', 'fail')
    with open(filename, 'wb') as configfile:
        config.write(configfile)
    if update == "YES":
        return render_template('index_update.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update)
    else:
        return render_template('index.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update)

# handling NBA status
@app.route("/NBA", methods=["GET", "POST"])
def NBA():
    update = config['DEFAULT']['update']
    NBA = request.form['NBA']
    config.set('DEFAULT', 'NBA', request.form['NBA'])
    brightness = int(config['DEFAULT']['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    conway = config['DEFAULT']['conway']
    gif = config['DEFAULT']['gif']
    starboard = config['DEFAULT']['starboard']
    job = manager.RestartUnit('NBA.service', 'replace')
    job = manager.StopUnit('starboard.service', 'replace')
    job = manager.StopUnit('conway.service', 'replace')
    job = manager.StopUnit('gif.service', 'replace')
    if update == "YES":
        return render_template('index_update.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update)
    else:
        return render_template('index.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update)

# handling starboard status
@app.route("/starboard", methods=["GET", "POST"])
def starboard():
    update = config['DEFAULT']['update']
    starboard = request.form['starboard']
    config.set('DEFAULT', 'starboard', request.form['starboard'])
    brightness = int(config['DEFAULT']['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    NBA = config['DEFAULT']['NBA']
    conway = config['DEFAULT']['conway']
    gif = config['DEFAULT']['gif']
    job = manager.RestartUnit('starboard.service', 'replace')
    job = manager.StopUnit('NBA.service', 'replace')
    job = manager.StopUnit('conway.service', 'replace')
    job = manager.StopUnit('gif.service', 'replace')
    if update == "YES":
        return render_template('index_update.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update)
    else:
        return render_template('index.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update)

# handling conway status
@app.route("/conway", methods=["GET", "POST"])
def conway():
    update = config['DEFAULT']['update']
    conway = request.form['conway']
    config.set('DEFAULT', 'conway', request.form['conway'])
    brightness = int(config['DEFAULT']['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    starboard = config['DEFAULT']['starboard']
    NBA = config['DEFAULT']['NBA']
    gif = config['DEFAULT']['gif']
    job = manager.RestartUnit('conway.service', 'replace')
    job = manager.StopUnit('NBA.service', 'replace')
    job = manager.StopUnit('starboard.service', 'replace')
    job = manager.StopUnit('gif.service', 'replace')
    if update == "YES":
        return render_template('index_update.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update)
    else:
        return render_template('index.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update)

# handling gif status
@app.route("/gif", methods=["GET", "POST"])
def gif():
    update = config['DEFAULT']['update']
    gif = request.form['gif']
    config.set('DEFAULT', 'gif', request.form['gif'])
    brightness = int(config['DEFAULT']['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    job = manager.StopUnit('NBA.service', 'replace')
    job = manager.StopUnit('starboard.service', 'replace')
    job = manager.StopUnit('conway.service', 'replace')
    with open(filename, 'wb') as configfile:
        config.write(configfile)
    job = manager.RestartUnit('gif.service', 'replace')
    if update == "YES":
        return render_template('index_update.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update)
    else:
        return render_template('index.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update)

# handling power status
@app.route("/off", methods=["GET", "POST"])
def off():
    update = config['DEFAULT']['update']
    conway = config['DEFAULT']['conway']
    brightness = int(config['DEFAULT']['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    NBA = config['DEFAULT']['NBA']
    gif = config['DEFAULT']['gif']
    starboard = config['DEFAULT']['starboard']
    job = manager.StopUnit('conway.service', 'replace')
    job = manager.StopUnit('NBA.service', 'replace')
    job = manager.StopUnit('starboard.service', 'replace')
    job = manager.StopUnit('gif.service', 'replace')
    if update == "YES":
        return render_template('index_update.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update)
    else:
        return render_template('index.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update)

# handling update
@app.route("/update", methods=["GET", "POST"])
def update():
    update = config['DEFAULT']['update']
    conway = config['DEFAULT']['conway']
    brightness = int(config['DEFAULT']['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    NBA = config['DEFAULT']['NBA']
    gif = config['DEFAULT']['gif']
    starboard = config['DEFAULT']['starboard']
    job = manager.StopUnit('conway.service', 'replace')
    job = manager.StopUnit('NBA.service', 'replace')
    job = manager.StopUnit('starboard.service', 'replace')
    job = manager.StopUnit('gif.service', 'replace')
    if update == "YES":
        return render_template('index_update.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update)
    else:
        return render_template('index.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update)

@app.errorhandler(400)
def not_found(e):
  return render_template('indextest.html'), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0')
