![Image of Web App]
(https://i.ibb.co/Ny0fKQB/webapp.png)

## Raspberry Pi Setup
1. Download the [BerryLan flavoured Raspbian image](https://downloads.nymea.io/images/berrylan/)
2. Download [Etcher](https://www.balena.io/etcher/)
3. Open Etcher, plug SD card into computer, install raspbian image download from file.
4. Insert the SD Card and power on your Raspberry Pi.
5. Install the BerryLan iOS or Android App and follow the instructions.
6. SSH into pi, run `sudo raspi-config`, set network at boot on: *System Options > Network at Boot > Yes*, pick timezone: *Localisation Options > Timezone*, change hostname and password, `sudo nano /boot/config.txt` set dtparam=audio=off.
7. Create NBAlog.txt file: `mkdir Documents && sudo touch /home/pi/Documents/NBAlog.txt && cd`

## Installation
      sudo apt-get update &&
      sudo apt-get install git python-pip &&
      git clone https://github.com/nanhoes/NBA-scoreboard &&
      cd NBA-scoreboard &&
      sudo bash install.sh
      
## Supported Matrices
      P2 128x64
      P4 64x32
      Four P4 64x32 chained together (2x2)
           
## Crontab (run 'sudo crontab -e', paste this crontab below ▼ at end of file)
      58 8 * * * sudo python3 /home/pi/My-NBA-scoreboard/Spreads_New_Day.py
      0 */2 * * * sudo python3 /home/pi/My-NBA-scoreboard/Spreads_Update.py
