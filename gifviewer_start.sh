#!/bin/bash
install_path=/home/pi/NBA-scoreboard
source ${install_path}/config-parser/config-parser.sh
config_parser ${install_path}/config/matrix_options.ini
config.section.DEFAULT
sudo ${install_path}/rpi-rgb-led-matrix/utils/led-image-viewer --led-gpio-mapping=${hardware_mapping} --led-cols=${columns} ${install_path}/images/${gifviewer}.gif
