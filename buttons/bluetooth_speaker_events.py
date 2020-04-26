#!/usr/bin/env python3
import subprocess
from evdev import InputDevice, categorize, ecodes
dev = InputDevice('/dev/input/event0')

print(dev)

def cmd(cmd_str: str):
        subprocess.run(cmd_str, shell=True)

for event in dev.read_loop():
	if event.type == ecodes.EV_KEY:
		print(categorize(event))
		if event.code == ecodes.KEY_PAUSECD:
			cmd("dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Pause")
		elif event.code == ecodes.KEY_PLAYCD:
			cmd("dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Play")
		elif event.code == ecodes.KEY_PREVIOUSSONG:
			cmd("dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous")
		elif event.code == ecodes.KEY_NEXTSONG:
			cmd("dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next")
