## Supported Matrices
      P2 128x64 (NBA_Render_P2.py)
      P4 64x32 (NBA_Render.py)
      Four P5 64x32 chained together (NBA_Render_2x2.py)
      Nine P5 64x32 chained together (NBA_Render_Big.py) (3x3)

## Update Raspberry Pi
      sudo apt-get update &&
      sudo apt-get install git python-pip
      
## Clone Repo, Install [Balena WiFi Connect](https://github.com/balena-os/wifi-connect)
      sudo apt-get update &&
      sudo apt-get install git python-pip &&
      git clone -b master https://github.com/nanhoes/NBA-scoreboard &&
      cd NBA-scoreboard &&
      chmod +x service_scripts/install-wifi-connect.sh &&
      nohup bash service_scripts/install-wifi-connect.sh & tail -f nohup.out
      
## Setup WiFI
1. Connect to "NBA_Setup_WiFi" from your phone.
2. Enter your wifi credentials (2.4 gHz network only).

## Install NBA-Scoreboard
      sudo bash install.sh

## Crontab

    0 9 * * * sudo python3 /home/pi/NBA-scoreboard/scoreboard/Spreads_New_Day.py

    1 9 * * * cd NBA-scoreboard && bash /home/pi/NBA-scoreboard/update_handling/check_for_update.sh

    0 */2 * * * sudo python3 /home/pi/NBA-scoreboard/scoreboard/Spreads_Update.py
    
## Web App
Access the web app at `hostname.local`, where hostname is your raspberry pi's hostname.
