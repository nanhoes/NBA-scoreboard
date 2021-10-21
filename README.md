## Supported Matrices
      P2 128x64 (NBA_Render_P2.py)
      P4 64x32 (NBA_Render.py)
      Four P5 64x32 chained together (NBA_Render_2x2.py)
      Nine P5 64x32 chained together (NBA_Render_Big.py) (3x3)

## Raspberry Pi Setup
1. Download the [BerryLan flavoured Raspbian image](https://downloads.nymea.io/images/berrylan/)
2. Download [Etcher](https://www.balena.io/etcher/)
3. Open Etcher, plug SD card into computer, install raspbian image download from file.
4. Insert the SD Card and power on your Raspberry Pi.
5. Install the BerryLan iOS or Android App and follow the instructions.
6. SSH into pi, change hostname and password: *System Options > hostname, password*, set local timezone: *Localisation Options > timezone*, reboot raspberry pi.
7. Create NBAlog.txt file: mkdir Documents && sudo touch /home/pi/Documents/NBAlog.txt && cd

## Installation
      sudo apt-get update &&
      sudo apt-get install git python-pip &&
      git clone -b experimental https://github.com/nanhoes/NBA-scoreboard &&
      cd NBA-scoreboard &&
      sudo bash install.sh

## Crontab (run 'sudo crontab -e', paste this crontab below ▼ at end of file)
      58 8 * * * sudo python3 /home/pi/My-NBA-scoreboard/Spreads_New_Day.py
      0 */2 * * * sudo python3 /home/pi/My-NBA-scoreboard/Spreads_Update.py
