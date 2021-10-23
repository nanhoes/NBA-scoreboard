#!/bin/bash
cd /home/pi/NBA-scoreboard
if [[ `git status -uno --porcelain` ]]; then
  echo "Update available!"
  sudo python3 update_handling/update.py
  sudo systemctl daemon-reload && sudo systemctl restart client
else
  echo "Already up to date."
  sudo python3 update_handling/no_update.py
fi
