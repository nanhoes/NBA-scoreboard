#!/bin/bash
install_path=/home/pi/NBA-scoreboard
source ${install_path}/config-parser/config-parser.sh
config_parser ${install_path}/config/matrix_options.ini
config.section.DEFAULT
sudo ${install_path}/rpi-rgb-led-matrix/utils/led-image-viewer --led-rows=${rows} --led-cols=${columns} --led-chain=${chain_length} --led-parallel=${parallel} --led-gpio-mapping=${hardware_mapping} --led-slowdown-gpio=${gpio_slowdown} --led-brightness=${brightness} --led-row-addr-type=${row_address_type} ${install_path}/board_images/${gif}
