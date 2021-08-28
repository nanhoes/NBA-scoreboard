#!/bin/bash
install_path=/home/pi/NBA-scoreboard
source ${install_path}/config-parser/config-parser.sh
config_parser ${install_path}/config/matrix_options.ini
config.section.DEFAULT
sudo python3 ${install_path}/scoreboard/${render_file}
