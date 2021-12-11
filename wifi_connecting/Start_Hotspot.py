import os
import pty
import subprocess
import datetime as dt
import time
from threading import Thread


# config
maxHotspotRetries = 5

# runtime vars
hotspotFailedCounter = 0


hotspot_name = 'NBA-Wifi-Setup'


def runHotspot():
    # remove old hotspotconnection, to make sure it won't conflict with the new hotspot
    os.system('sudo nmcli connection delete id NBA-Wifi-Setup || true')

    # we need to use pseudoterminal since wifi-connect outputs to tty, thus we can't read stdout
    # -> READ THIS: https://stackoverflow.com/a/42008071
    master, slave = pty.openpty()
    hotspotProcess = subprocess.Popen(["/usr/local/sbin/wifi-connect", "-s", hotspot_name], stdin=subprocess.PIPE,
                                      stdout=slave, stderr=slave, close_fds=True)
    # the code above duplicates the slaveFD for use with the hotspotProcess, so both slaves need to be closed to make s$
    os.close(slave)


    readLine = ""
    while True:
        try:
            read = str(os.read(master, 1), 'utf-8')
        except OSError: # the process has ended
            break
        if read is not None:
            if read == '\n':
                print(readLine)

                if readLine.find("User connected to the captive portal") != -1:
                    # we can do something like fire an event: userHasInteractionWithHotspotEvent()
                    print("user connected")


                # because of some strange bug of NMCLI sometimes only the connected wifi-network is returned.
                # If that is the case: restart
                if readLine.find("Access points") != -1:
                    if readLine.count(',') == 0: # zero or one ssids found, not good: restart hotspot
                        global hotspotFailedCounter
                        global maxHotspotRetries

                        if hotspotFailedCounter < maxHotspotRetries:
                            hotspotFailedCounter = hotspotFailedCounter + 1
                            print("zero or one ssids found; not good: restart hotspot")
                            time.sleep(5) # add a delay, so that the hotspot is started first; this may trigger a resca$
                            hotspotProcess.terminate() # stop the hotspot process
                            print("process stopped, restarting in 5 seconds")
                            time.sleep(5)
                            t = Thread(target=runHotspot) # restart this function in new thread
                            t.start()
                            return # end this instance of runHotspot
                        else:
                            # if still the case after maxHotspotRetries -> continue, there is probably only one ssid
                            print("not many hotspots found, but continue after "+str(maxHotspotRetries)+" retries")
                        hotspotFailedCounter = 0


                readLine = ""
            else:
                readLine = readLine + read
        else:
            break


runHotspot()
