cd /home/pi/NBA-scoreboard
if [[ `git status -uno --porcelain` ]]; then
  echo "Update available!"
else
  echo "Already up to date."
fi
