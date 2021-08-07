#!/bin/bash
install_path=$(pwd)
source ${install_path}/config-parser/config-parser.sh
config_parser ${install_path}/config/matrix_options.ini
config.section.DEFAULT
sudo ${install_path}/rpi-rgb-led-matrix/examples-api-use/demo --led-rows=${rows} --led-cols=${columns} --led-chain=${chain_length} --led-parallel=${parallel} --led-gpio-mapping=${hardware_mapping} —led-slowdown-gpio=${slowdown_gpio} --led-brightness=${brightness} --led-row-addr-type=${row_address_type} --led-pwm-bits=10 -D 7
