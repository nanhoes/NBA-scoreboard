## Supported Matrices
      P4 64x32 (NBA_Render.py)
      Nine P5 64x32 chained together (NBA_Render_Big.py) (3x3)
      P2 128x64 (NBA_Render_P2.py) (partial support)
      Four P5 64x32 chained together (NBA_Render_2x2.py) (partial support)
      
## Prerequisites
      sudo apt-get update
      sudo apt-get install git python3-pip
      
## Clone NBA-Scoreboard
      git clone -b master https://github.com/nanhoes/NBA-scoreboard
      
## Start Wifi-Connect
      sudo chmod +x /home/pi/NBA-scoreboard/service_scripts/install-wifi-connect.sh
      nohup bash /home/pi/NBA-scoreboard/service_scripts/install-wifi-connect.sh & tail -F nohup.out
      
## Install NBA-Scoreboard
      cd NBA-scoreboard
      sudo bash install.sh

## Crontab

    0 9 * * * sudo python3 /home/pi/NBA-scoreboard/scoreboard/Spreads_New_Day.py

    1 9 * * * cd /home/pi/NBA-scoreboard && bash /home/pi/NBA-scoreboard/update_handling/check_for_update.sh

    0 */2 * * * sudo python3 /home/pi/NBA-scoreboard/scoreboard/Spreads_Update.py
        
