## Supported Matrices
      P2 128x64 (NBA_Render_P2.py)
      P4 64x32 (NBA_Render.py)
      Four P5 64x32 chained together (NBA_Render_2x2.py)
      Nine P5 64x32 chained together (NBA_Render_Big.py) (3x3)
      
## Clone NBA-Scoreboard
      sudo apt-get install git python3-pip
      git clone -b master https://github.com/nanhoes/NBA-scoreboard
      
## Start wifi-connect
       sudo chmod +x /home/pi/NBA-scoreboard/service_scripts/install-wifi-connect.sh
       nohup bash /home/pi/NBA-scoreboard/service_scripts/install-wifi-connect.sh & tail -F nohup.out
      
## Install NBA-scoreboard
      cd NBA-scoreboard
      sudo bash install.sh

## Crontab

    0 9 * * * sudo python3 /home/pi/NBA-scoreboard/scoreboard/Spreads_New_Day.py

    1 9 * * * cd NBA-scoreboard && bash /home/pi/NBA-scoreboard/update_handling/check_for_update.sh

    0 */2 * * * sudo python3 /home/pi/NBA-scoreboard/scoreboard/Spreads_Update.py
        
