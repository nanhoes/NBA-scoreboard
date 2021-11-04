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
    brightness = int(config['DEFAULT']['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    NBA = config['DEFAULT']['NBA']
    starboard = config['DEFAULT']['starboard']
    conway = config['DEFAULT']['conway']
    gif = config['DEFAULT']['gif']
    update = config['DEFAULT']['update']
    custom_logo = config['DEFAULT']['custom_logo']
    if update == "YES":
        return render_template('index_update.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update, custom_logo = custom_logo)
    else:
        return render_template('index.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update, custom_logo = custom_logo)

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
    custom_logo = config['DEFAULT']['custom_logo']
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
        return render_template('index_update.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update, custom_logo = custom_logo)
    else:
        return render_template('index.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update, custom_logo = custom_logo)

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
    custom_logo = config['DEFAULT']['custom_logo']
    job = manager.RestartUnit('NBA.service', 'replace')
    job = manager.StopUnit('starboard.service', 'replace')
    job = manager.StopUnit('conway.service', 'replace')
    job = manager.StopUnit('gif.service', 'replace')
    if update == "YES":
        return render_template('index_update.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update, custom_logo = custom_logo)
    else:
        return render_template('index.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update, custom_logo = custom_logo)

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
    custom_logo = config['DEFAULT']['custom_logo']
    job = manager.RestartUnit('starboard.service', 'replace')
    job = manager.StopUnit('NBA.service', 'replace')
    job = manager.StopUnit('conway.service', 'replace')
    job = manager.StopUnit('gif.service', 'replace')
    if update == "YES":
        return render_template('index_update.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update, custom_logo = custom_logo)
    else:
        return render_template('index.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update, custom_logo = custom_logo)

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
    custom_logo = config['DEFAULT']['custom_logo']
    if update == "YES":
        return render_template('index_update.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update, custom_logo = custom_logo)
    else:
        return render_template('index.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update, custom_logo = custom_logo)

# handling gif status
@app.route("/gif", methods=["GET", "POST"])
def gif():
    update = config['DEFAULT']['update']
    gif = request.form['gif']
    config.set('DEFAULT', 'gif', request.form['gif'])
    brightness = int(config['DEFAULT']['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    custom_logo = config['DEFAULT']['custom_logo']
    job = manager.StopUnit('NBA.service', 'replace')
    job = manager.StopUnit('starboard.service', 'replace')
    job = manager.StopUnit('conway.service', 'replace')
    with open(filename, 'wb') as configfile:
        config.write(configfile)
    job = manager.RestartUnit('gif.service', 'replace')
    if update == "YES":
        return render_template('index_update.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update, custom_logo = custom_logo)
    else:
        return render_template('index.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update, custom_logo = custom_logo)

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
    custom_logo = config['DEFAULT']['custom_logo']
    job = manager.StopUnit('conway.service', 'replace')
    job = manager.StopUnit('NBA.service', 'replace')
    job = manager.StopUnit('starboard.service', 'replace')
    job = manager.StopUnit('gif.service', 'replace')
    if update == "YES":
        return render_template('index_update.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update, custom_logo = custom_logo)
    else:
        return render_template('index.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update, custom_logo = custom_logo)

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
    custom_logo = config['DEFAULT']['custom_logo']
    job = manager.StopUnit('conway.service', 'replace')
    job = manager.StopUnit('NBA.service', 'replace')
    job = manager.StopUnit('starboard.service', 'replace')
    job = manager.StopUnit('gif.service', 'replace')
    job = manager.StartUnit('update.service', 'replace')
    if update == "YES":
        return render_template('index_update.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update, custom_logo = custom_logo)
    else:
        return render_template('index.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update, custom_logo = custom_logo)

@app.route("/shutdown", methods=["GET", "POST"])
def shutdown():
    update = config['DEFAULT']['update']
    conway = config['DEFAULT']['conway']
    brightness = int(config['DEFAULT']['brightness'])
    width = int(config['DEFAULT']['rows'])
    height = int(config['DEFAULT']['columns'])
    NBA = config['DEFAULT']['NBA']
    gif = config['DEFAULT']['gif']
    starboard = config['DEFAULT']['starboard']
    custom_logo = config['DEFAULT']['custom_logo']
    job = manager.StopUnit('conway.service', 'replace')
    job = manager.StopUnit('NBA.service', 'replace')
    job = manager.StopUnit('starboard.service', 'replace')
    job = manager.StopUnit('gif.service', 'replace')
    return render_template('indextest.html', brightness = brightness, width = width, height = height, NBA = NBA, starboard = starboard, conway = conway, gif = gif, update = update, custom_logo = custom_logo)
    job = manager.StartUnit('shutdown.service', 'replace')

@app.errorhandler(404)
def not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(e):
  return render_template('403.html'), 403

@app.errorhandler(410)
def gone(e):
  return render_template('410.html'), 410

@app.errorhandler(500)
def int_server_error(e):
  return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0')
