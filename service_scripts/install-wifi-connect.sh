#!/bin/bash
bash <(curl -L https://raw.githubusercontent.com/nanhoes/wifi-connect/master/scripts/raspbian-install.sh) -- -y
sudo wifi-connect -s NBA-WiFi-Setup
