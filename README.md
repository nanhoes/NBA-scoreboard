# My-NBA-scoreboard
### Raspberry Pi Setup
1. Download raspbian image with Berrylan: https://downloads.nymea.io/images/berrylan/latest
2. Download Etcher: https://www.balena.io/etcher/
3. Open Etcher, plug in SD card, install raspbian image download from file.
4. Open Berrylan app connect to 'BT WLAN setup' and connect to 2.4 GHz wifi.
5. SSH into pi and 
### Installation
      sudo apt-get update
      sudo apt-get install git python-pip
      git clone https://github.com/nanhoes/My-NBA-scoreboard
      cd My-NBA-scoreboard
      sudo chmod +x install.sh
      sudo ./install.sh
### bderr Crontab
      @reboot sleep 20; sudo python3 /home/pi/NBA-scoreboard/NBA_Data.py

      @reboot sleep 20; sudo python3 /home/pi/NBA-scoreboard/NBA_Render.py

      @reboot sleep 20; sudo python3 /home/pi/NBA-scoreboard/NBA_Spreads.py

      0 11 * * * sudo python3 /home/pi/NBA-scoreboard/Spreads_New_Day.py

      0 5 * * * sudo python3 /home/pi/NBA-scoreboard/NBA_Data.py

      */30 * * * * sudo python3 /home/pi/NBA-scoreboard/NBA_Spreads.py
### My Crontab
      @reboot sudo python3 /home/pi/My-NBA-scoreboard/NBA_Data.py

      @reboot sudo python3 /home/pi/My-NBA-scoreboard/NBA_Render.py

      @reboot sudo python3 /home/pi/My-NBA-scoreboard/NBA_Spreads.py

      0 11 * * * sudo python3 /home/pi/My-NBA-scoreboard/Spreads_New_Day.py

      0 5 * * * sudo python3 /home/pi/My-NBA-scoreboard/NBA_Data.py

      */30 * * * * sudo python3 /home/pi/My-NBA-scoreboard/NBA_Spreads.py
