## Raspberry Pi Setup
1. Download the [BerryLan flavoured Raspbian image](https://downloads.nymea.io/images/berrylan/)
2. Download [Etcher](https://www.balena.io/etcher/)
3. Open Etcher, plug SD card into computer, install raspbian image download from file.
4. Insert the SD Card and power on your Raspberry Pi.
5. Install the BerryLan iOS or Android App and follow the instructions.
6. SSH into pi, run `sudo raspi-config`, set network at boot on: *System Options > Network at Boot > Yes*, pick timezone: *Localisation Options > Timezone*, change hostname and password, `sudo nano /boot/config.txt` set dtparam=audio=off.
7. Create NBAlog.txt file (enter linebreak to save file): `mkdir Documents && sudo nano /home/pi/Documents/NBAlog.txt && Log:`

## Installation
      sudo apt-get update &&
      sudo apt-get install git python-pip &&
      git clone https://github.com/nanhoes/NBA-scoreboard &&
      cd NBA-scoreboard &&
      sudo bash setup.sh
           
## Crontab (run 'sudo crontab -e', paste this crontab below ▼ at end of file)
      @reboot sudo python3 /home/pi/NBA-scoreboard/scoreboard/NBA_Data.py

      @reboot sudo python3 /home/pi/NBA-scoreboard/scoreboard/NBA_Render.py

      @reboot sudo python3 /home/pi/NBA-scoreboard/scoreboard/NBA_Spreads.py

      0 11 * * * sudo python3 /home/pi/NBA-scoreboard/scoreboard/Spreads_New_Day.py

      0 5 * * * sudo python3 /home/pi/NBA-scoreboard/scoreboard/NBA_Data.py

      */30 * * * * sudo python3 /home/pi/NBA-scoreboard/scoreboard/NBA_Spreads.py
      
      
## Manage Homebridge and Connect Raspberry Pi to Homekit
Follow steps on Homebridge github: https://github.com/homebridge/homebridge-raspbian-image/wiki/Getting-Started
