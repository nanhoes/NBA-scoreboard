git clone https://github.com/hzeller/rpi-rgb-led-matrix.git

cd
cd /home/pi/My-NBA-scoreboard/rpi-rgb-led-matrix

sudo apt-get update && sudo apt-get install python3-dev python3-pillow -y
make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)
sudo apt-get install python3-bs4

cd
sudo apt-get install otf2bdf
cd /home/pi/My-NBA-scoreboard
otf2bdf -v -o Minimal-Mono-Bold.bdf -r 72 -p 18 /home/pi/My-NBA-scoreboard/Minimal-Mono-Bold.otf
