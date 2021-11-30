#!/usr/bin/env bash

export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket

# Optional step - it takes couple of seconds (or longer) to establish a WiFi connection
# sometimes. In this case, following checks will fail and wifi-connect
# will be launched even if the device will be able to connect to a WiFi network.
# If this is your case, you can wait for a while and then check for the connection.
# sleep 15

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
<<<<<<< HEAD

else
    printf 'Starting WiFi Connect\n'
    sudo python3 Wifi_Not_Connected.py
=======
else
    printf 'Starting WiFi Connect\n'
>>>>>>> ab3d565afa88d4625eba37a96c77b8b496eedd4a
    sudo wifi-connect -s NBA-WiFi-Setup

fi

<<<<<<< HEAD
sudo pkill -f Wifi_Not_Connected.py
sudo python3 Wifi_Connected.py
=======
#sudo systemctl stop starboard
>>>>>>> ab3d565afa88d4625eba37a96c77b8b496eedd4a
sudo systemctl start NBA

sleep infinity
