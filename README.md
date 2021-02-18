# My-NBA-scoreboard
### Installation
      git clone https://github.com/nanhoes/My-NBA-scoreboard
      cd My-NBA-scoreboard
      sudo ./install.sh
### bderr Crontab
      @reboot sleep 20; sudo python3 /home/pi/NBA-scoreboard/NBA_Data.py

      @reboot sleep 20; sudo python3 /home/pi/NBA-scoreboard/NBA_Render.py

      @reboot sleep 20; sudo python3 /home/pi/NBA-scoreboard/NBA_Spreads.py

      0 11 * * * sudo python3 /home/pi/NBA-scoreboard/Spreads_New_Day.py

      0 5 * * * sudo python3 /home/pi/NBA-scoreboard/NBA_Data.py

      */30 * * * * sudo python3 /home/pi/NBA-scoreboard/NBA_Spreads.py
### My Crontab
      @reboot sleep 20; sudo python3 /home/pi/My-NBA-scoreboard/NBA_Data.py

      @reboot sleep 20; sudo python3 /home/pi/My-NBA-scoreboard/NBA_Render.py

      @reboot sleep 20; sudo python3 /home/pi/My-NBA-scoreboard/NBA_Spreads.py

      0 11 * * * sudo python3 /home/pi/My-NBA-scoreboard/Spreads_New_Day.py

      0 5 * * * sudo python3 /home/pi/My-NBA-scoreboard/NBA_Data.py

      */30 * * * * sudo python3 /home/pi/My-NBA-scoreboard/NBA_Spreads.py
