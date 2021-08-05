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

echo "Installing font dependencies:"
cd
sudo apt-get install otf2bdf
cd /home/pi/NBA-scoreboard
otf2bdf -v -o Minimal-Mono-Bold.bdf -r 72 -p 18 /home/pi/NBA-scoreboard/Minimal-Mono-Bold.otf
cd /home/pi/NBA-scoreboard

install_path=$(pwd)
echo "Installing flask library:"
pip install flask --upgrade

echo "Creating render service:"
sudo cp ./config/render.service /etc/systemd/system/
sudo sed -i -e "/\[Service\]/a ExecStart=python3 ${install_path}/NBA_Render_P2.py < /dev/zero &> /dev/null &" /etc/systemd/system/render.service
sudo mkdir /etc/systemd/system/render.service.d
render_env_path=/etc/systemd/system/render.service.d/render_env.conf
sudo touch $render_env_path
sudo echo "[Service]" >> $render_env_path
sudo systemctl daemon-reload
sudo systemctl start render
sudo systemctl enable render
echo "...done"

echo "Creating render-client service:"
sudo cp ./config/render-client.service /etc/systemd/system/
sudo sed -i -e "/\[Service\]/a ExecStart=python3 ${install_path}/client/app.py &" /etc/systemd/system/render-client.service
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

