#!/bin/bash

echo "Installing rpi-rgb-led-matrix:"
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git

cd
cd /home/pi/NBA-scoreboard/rpi-rgb-led-matrix

echo "Installing python3:"
sudo apt-get update && sudo apt-get install python3-dev python3-pillow -y
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
cd /home/pi/NBA-scoreboard

install_path=$(pwd)
echo "Installing flask library:"
pip install flask --upgrade

echo "Installing config-parser"
git clone https://gitlab.com/chilladx/config-parser.git

echo "Removing NBA service if it exists:"
sudo systemctl stop NBA
sudo rm -rf /etc/systemd/system/NBA.*
sudo systemctl daemon-reload
echo "...done"

echo "Removing render-client service if it exists:"
sudo systemctl stop render-client
sudo rm -rf /etc/systemd/system/render-client.*
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
sudo cp ./config/NBA.service /etc/systemd/system/
sudo sed -i -e "/\[Service\]/a ExecStart=python3 ${install_path}/scoreboard/NBA_Render_Big.py < /dev/zero &> /dev/null &" /etc/systemd/system/NBA.service
sudo mkdir /etc/systemd/system/NBA.service.d
NBA_env_path=/etc/systemd/system/NBA.service.d/NBA_env.conf
sudo touch $NBA_env_path
sudo echo "[Service]" >> $NBA_env_path
sudo systemctl daemon-reload
sudo systemctl start NBA
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
sudo cp ${install_path}/conway_start.sh /usr/bin
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
sudo cp ${install_path}/gif_start.sh /usr/bin
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

echo "Creating render-client service:"
sudo cp ./config/render-client.service /etc/systemd/system/
sudo sed -i -e "/\[Service\]/a ExecStart=python ${install_path}/client/app.py &" /etc/systemd/system/render-client.service
sudo systemctl daemon-reload
sudo systemctl start render-client
sudo systemctl enable render-client
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
