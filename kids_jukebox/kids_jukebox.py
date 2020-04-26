#!/usr/bin/env python3
import time
import subprocess
import RPi.GPIO as GPIO
import time
import os

def get_touchpad_status(outs, ins, measurements=5):
    y = []
    for i in range(measurements):
        x = []
        for out_idx, out in enumerate(outs):
            GPIO.output(out, GPIO.HIGH)
            time.sleep(0.001)  # wait 1ms (pins can do > 200kHz)
            for in_idx, _in in enumerate(ins):
                # print(f"{out_idx}/{in_idx}:{GPIO.input(_in)} {GPIO.input(_in) == GPIO.HIGH}")
                if GPIO.input(_in) == GPIO.HIGH:
                    x.append(out_idx * len(ins) + in_idx)
            GPIO.output(out, GPIO.LOW)
            time.sleep(0.01)  # wait 10ms (pins can do > 200kHz)
        y.append(x)
        time.sleep(0.1)  # sleep 100ms per measurement
    z = set()
    occurances = {}
    for x in y:
        z.update(x)
    for val in z:
        occurances[val] = sum([sum([1 for v in x if v == val]) for x in y])
    return occurances

def print_touchpad_status(occurances):
    print("".join([f"{k}({v})   " for k,v in occurances.items()]))

def init_touchpad():
    outs = [23, 22, 27, 17]
    ins = [16, 26, 13, 12, 6, 5]

    GPIO.setmode(GPIO.BCM)
    for out in outs:
        print(f"Configuring pin {out} as output")
        GPIO.setup(out, GPIO.OUT, initial=GPIO.LOW)

    for _in in ins:
        print(f"Configuring pin {_in} as input")
        GPIO.setup(_in, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    return outs, ins
    
def cmd(cmd_str: str):
        subprocess.run(cmd_str, shell=True)

def connect_bluetooth():
    # TODO: loop over connect until `sudo -u pulse pactl info | grep bluez` is true
    # connect to bluetooth device if not yet completed
    cmd(r"sudo -u pulse pactl info | grep bluez || { systemctl --user stop bluetooth_to_vlc; sudo service bluetooth stop; sleep 1; sudo service bluetooth start; sleep 2; bluetoothctl < /home/pi/kids_jukebox/connect; echo waiting 10s; sleep 10; }")
    # start bluetooth buttons
    cmd(r"systemctl --user status bluetooth_to_vlc || systemctl --user start bluetooth_to_vlc")


def play_collection(collection_dir: str, num: int):
    # kill already running vlcs
    cmd("killall vlc")
    # start vlc
    cmd(f"cvlc {collection_dir}/{num}/ &")
    # set volume (set initial volume which is too loud on connect)
    cmd(r"dbus-send --print-reply --session --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Set string:org.mpris.MediaPlayer2.Player string:Volume variant:double:0.7")
    cmd(r"sh -c 'sleep 2; dbus-send --print-reply --session --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Set string:org.mpris.MediaPlayer2.Player string:Volume variant:double:0.7' &")

def main():
    collection_dir = "~/kids_jukebox/playlist/current"
    collection_dirs = {
        0: "~/kids_jukebox/playlist/pi1",
        6: "~/kids_jukebox/playlist/demo",
    }
    shutdown = 23  # use bottom right field as shutdown
    measurements = 5
    outs, ins = init_touchpad()
    # wait until shutdown is released
    while True:
        pad = get_touchpad_status(outs, ins, measurements)
        if shutdown not in pad.keys():
            break
        if len(pad) == 2 and shutdown in pad.keys():
            # check for changes in collection sheet signaled by two magnets 
            for key, directory in collection_dirs.items():
                if key in pad and pad[key] == measurements:
                    print(f"Changing music collection to: {directory}")
                    cmd = f"ln -n -s -f {directory} {collection_dir}"
                    print(cmd)
                    os.system(cmd)

    connect_bluetooth()
        
    cur = -1
    while True:
        time.sleep(1)
        pad = get_touchpad_status(outs, ins, measurements)
        print_touchpad_status(pad)
        # detect unambiguous selection
        if len(pad) == 1 and list(pad.keys())[0] != cur and list(pad.values())[0] == measurements:
            cur = list(pad.keys())[0]

            if cur == shutdown:
                print(f"{cur} -> shutting down")
                cmd("sudo /sbin/poweroff")
                exit(0)
            
            # try to switch to song
            connect_bluetooth()  # just in case currently not connected
        
            play_collection(collection_dir, cur)
            
if __name__ == "__main__":
    main()
