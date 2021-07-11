# My-NBA-scoreboard
### Raspberry Pi Setup
1. Download raspbian image with Homebridge: https://github.com/homebridge/homebridge-raspbian-image/releases/latest
2. Download Etcher: https://www.balena.io/etcher/
3. Open Etcher, plug in SD card, install raspbian image download from file.
4. Power on raspberry pi, wait 1-2 minutes, connect to network name Homebridge WiFi Setup
5. Wait a few moments until the captive portal opens, this portal will allow you to connect the Raspberry Pi to your local WiFi network.
6. SSH into pi, boot on network connection, change region, dtparam=audio=off in /boot/config.txt.
7. Create NBAlog.txt file in /home/pi/Documents

### Installation
      sudo apt-get update &&
      sudo apt-get install git python-pip &&
      git clone https://github.com/nanhoes/My-NBA-scoreboard &&
      cd My-NBA-scoreboard &&
      sudo chmod +x install.sh &&
      sudo ./install.sh
      
### Crontab (run 'sudo crontab -e', paste this crontab below ▼ at end of file)
      @reboot sudo python3 /home/pi/My-NBA-scoreboard/NBA_Data.py

      @reboot sudo python3 /home/pi/My-NBA-scoreboard/NBA_Render.py

      @reboot sudo python3 /home/pi/My-NBA-scoreboard/NBA_Spreads.py

      0 11 * * * sudo python3 /home/pi/My-NBA-scoreboard/Spreads_New_Day.py

      0 5 * * * sudo python3 /home/pi/My-NBA-scoreboard/NBA_Data.py

      */30 * * * * sudo python3 /home/pi/My-NBA-scoreboard/NBA_Spreads.py
      
### Manage Homebridge
      The Homebridge UI web interface will allow you to install, remove and update plugins, and modify the Homebridge config.json and manage other aspects of your Homebridge service.

      The default user is admin with password admin.

      If you're using macOS or a mobile device, you should be able to access the UI via http://homebridge.local.

      If you're using Windows, or http://homebridge.local does not work for you, you will need to find the IP address of your Raspberry Pi another way:

      Login to your router and find the "connected devices" or "dhcp clients" page to find the IP address that was assigned to the Raspberry Pi.
      Use an iPhone to access http://homebridge.local, once you login using the default username and password (admin/admin) you can find the IP address under System Information.
      Download the Fing app for iOS or Android to scan your network to find the IP address of your Raspberry Pi.
      As a last resort, if you plug a monitor into your Raspberry Pi, the IP address will be displayed on the attached screen once it has finished booting.
      Once you've found your IP address, login to the web interface by going to http://<ip address of your server>.
