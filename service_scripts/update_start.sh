#!/bin/bash
cd /home/pi/NBA-scoreboard
git pull
sudo python3 /home/pi/NBA-scoreboard/update_handling/no_update.py
sudo systemctl daemon-reload
