#!/usr/bin/env bash

export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket

# Optional step - it takes couple of seconds (or longer) to establish a WiFi connection
# sometimes. In this case, following checks will fail and wifi-connect
# will be launched even if the device will be able to connect to a WiFi network.
# If this is your case, you can wait for a while and then check for the connection.
sleep 15

# Choose a condition for running WiFi Connect according to your use case:

# 1. Is there a default gateway?
# ip route | grep default

# 2. Is there Internet connectivity?
# nmcli -t g | grep full

# 3. Is there Internet connectivity via a google ping?
# wget --spider http://google.com 2>&1

# 4. Is there an active WiFi connection?
iwgetid -r

if [ $? -eq 0 ]; then
    printf 'Skipping WiFi Connect\n'

else
    printf 'Starting WiFi Connect\n'
    sudo systemctl stop client
    sudo python3 /home/pi/NBA-scoreboard/wifi_connecting/Wifi_Not_Connected.py & 
    sudo wifi-connect -s NBA-WiFi-Setup
    while true; do    
        iwgetid -r
        if [ $? -eq 0 ]; then
            sudo pkill -f /home/pi/NBA-scoreboard/wifi_connecting/Wifi_Not_Connected.py
            sudo python3 /home/pi/NBA-scoreboard/wifi_connecting/Wifi_Connected.py
        else
            continue
        fi
        break
fi
printf 'Starting NBA Render\n'
sudo systemctl start client
sudo systemctl start NBA

sleep infinity
