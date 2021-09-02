#!/bin/bash

echo "Installing rpi-rgb-led-matrix:"
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git

reconfig() {
	grep $2 $1 >/dev/null
	if [ $? -eq 0 ]; then
		# Pattern found; replace in file
		sed -i "s/$2/$3/g" $1 >/dev/null
	else
		# Not found; append (silently)
		echo $3 | sudo tee -a $1 >/dev/null
	fi
}

reconfig /boot/config.txt "^.*dtparam=audio.*$" "dtparam=audio=off"

cd
mkdir Documents
sudo touch /home/pi/Documents/NBAlog.txt

cd
cd /home/pi/NBA-scoreboard/rpi-rgb-led-matrix

echo "Installing python3:"
sudo apt-get update && sudo apt-get install python3-pip python3-dev python3-pillow -y
make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)
sudo apt-get install python3-bs4

echo "Creating image-viewer:"
cd utils
sudo apt-get update
sudo apt-get install libgraphicsmagick++-dev libwebp-dev -y
sudo make led-image-viewer

echo "Installing font dependencies:"
cd
sudo apt-get install otf2bdf
cd /home/pi/NBA-scoreboard
otf2bdf -v -o Minimal-Mono-Bold.bdf -r 72 -p 18 /home/pi/NBA-scoreboard/Minimal-Mono-Bold.otf

cd /home/pi/NBA-scoreboard/client

echo "Installing nginx:"
sudo apt-get nginx

echo "Creating virtual environment:"
python3 -m venv NBA-scoreboard-venv
source NBA-scoreboard-venv/bin/activate

echo "Installing flask and gunicorn:"
pip install gunicorn flask

deactivate

echo "Removing client service if it exists:"
sudo systemctl stop client
sudo rm -rf /etc/systemd/system/client.*
sudo systemctl daemon-reload
echo "...done"

echo "Creating client service:"
sudo cp ./config/client.service /etc/systemd/system/
sudo sed -i -e "/\[Service\]/a ExecStart=/home/pi/.local/bin/gunicorn --workers 3 --bind unix:app.sock -m 007 wsgi:app &" /etc/systemd/system/client.service
sudo systemctl daemon-reload
sudo systemctl start client
sudo systemctl enable client
echo "...done"

cd /etc/nginx/

cd /home/pi/NBA-scoreboard
install_path=$(pwd)

echo "Installing config-parser"
git clone https://gitlab.com/chilladx/config-parser.git

read -n 1 -r -s -p $'\n----------------------------------\nPLEASE CONFIGURE YOUR MATRIX PROFILE NOW\nCopy your profile and paste under "[DEFAULT]"\nChange gpio-mapping to your mapping: regular, adafruit-hat, adafruit-hat-pwm, or complete-module\nPRESS ANY KEY TO CONTINUE...\n'
sudo nano config/matrix_options.ini

echo "Removing NBA service if it exists:"
sudo systemctl stop NBA
sudo rm -rf /etc/systemd/system/NBA.*
sudo systemctl daemon-reload
echo "...done"

echo "Removing starboard service if it exists:"
sudo systemctl stop starboard
sudo rm -rf /etc/systemd/system/starboard.*
sudo systemctl daemon-reload
echo "...done"

echo "Removing conway service if it exists:"
sudo systemctl stop conway
sudo rm -rf /etc/systemd/system/conway.*
sudo systemctl daemon-reload
echo "...done"

echo "Removing gif service if it exists:"
sudo systemctl stop gif
sudo rm -rf /etc/systemd/system/gif.*
sudo systemctl daemon-reload
echo "...done"

echo "Creating NBA service:"
sudo cp ${install_path}/service_scripts/NBA_start.sh /usr/bin
sudo chmod +x /usr/bin/NBA_start.sh
sudo cp ./config/NBA.service /etc/systemd/system/
sudo sed -i -e "/\[Service\]/a ExecStart=/usr/bin/NBA_start.sh < /dev/zero &> /dev/null &" /etc/systemd/system/NBA.service
sudo mkdir /etc/systemd/system/NBA.service.d
NBA_env_path=/etc/systemd/system/NBA.service.d/NBA_env.conf
sudo touch $NBA_env_path
sudo echo "[Service]" >> $NBA_env_path
sudo systemctl daemon-reload
sudo systemctl enable NBA
echo "...done"

echo "Creating data service:"
sudo cp ./config/data.service /etc/systemd/system/
sudo sed -i -e "/\[Service\]/a ExecStart=python3 ${install_path}/scoreboard/NBA_Data.py < /dev/zero &> /dev/null &" /etc/systemd/system/data.service
sudo mkdir /etc/systemd/system/data.service.d
data_env_path=/etc/systemd/system/data.service.d/data_env.conf
sudo touch $data_env_path
sudo echo "[Service]" >> $data_env_path
sudo systemctl daemon-reload
sudo systemctl start data
sudo systemctl enable data
echo "...done"

echo "Creating spreads service:"
sudo cp ./config/spreads.service /etc/systemd/system/
sudo sed -i -e "/\[Service\]/a ExecStart=python3 ${install_path}/scoreboard/NBA_Spreads.py < /dev/zero &> /dev/null &" /etc/systemd/system/spreads.service
sudo mkdir /etc/systemd/system/spreads.service.d
spreads_env_path=/etc/systemd/system/spreads.service.d/spreads_env.conf
sudo touch $spreads_env_path
sudo echo "[Service]" >> $spreads_env_path
sudo systemctl daemon-reload
sudo systemctl start spreads
sudo systemctl enable spreads
echo "...done"

echo "Creating starboard service:"
sudo cp ./config/starboard.service /etc/systemd/system/
sudo sed -i -e "/\[Service\]/a ExecStart=python3 ${install_path}/animations/starboard.py < /dev/zero &> /dev/null &" /etc/systemd/system/starboard.service
sudo mkdir /etc/systemd/system/starboard.service.d
starboard_env_path=/etc/systemd/system/starboard.service.d/starboard_env.conf
sudo touch $starboard_env_path
sudo echo "[Service]" >> $starboard_env_path
sudo systemctl daemon-reload
sudo systemctl disable starboard
echo "...done"

echo "Creating conway service:"
sudo cp ${install_path}/service_scripts/conway_start.sh /usr/bin
sudo chmod +x /usr/bin/conway_start.sh
sudo cp ./config/conway.service /etc/systemd/system/
sudo sed -i -e "/\[Service\]/a ExecStart=/usr/bin/conway_start.sh < /dev/zero &> /dev/null &" /etc/systemd/system/conway.service
sudo mkdir /etc/systemd/system/conway.service.d
conway_env_path=/etc/systemd/system/conway.service.d/conway_env.conf
sudo touch $conway_env_path
sudo echo "[Service]" >> $conway_env_path
sudo systemctl daemon-reload
sudo systemctl disable conway
echo "...done"

echo "Creating gif service:"
sudo cp ${install_path}/service_scripts/gif_start.sh /usr/bin
sudo chmod +x /usr/bin/gif_start.sh
sudo cp ./config/gif.service /etc/systemd/system/
sudo sed -i -e "/\[Service\]/a ExecStart=/usr/bin/gif_start.sh < /dev/zero &> /dev/null &" /etc/systemd/system/gif.service
sudo mkdir /etc/systemd/system/gif.service.d
gif_env_path=/etc/systemd/system/gif.service.d/gif_env.conf
sudo touch $gif_env_path
sudo echo "[Service]" >> $gif_env_path
sudo systemctl daemon-reload
sudo systemctl disable gif
echo "...done"

echo -n "In order to finish setup a reboot is necessary..."
echo -n "REBOOT NOW? [y/N] "
read
if [[ ! "$REPLY" =~ ^(yes|y|Y)$ ]]; then
        echo "Exiting without reboot."
        exit 0
fi
echo "Reboot started..."
reboot
sleep infinity
