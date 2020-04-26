set -x
#systemctl --user start pulseaudio
#systemctl --user enable pulseaudio

## disable user based pulseaudio
mv /usr/lib/systemd/user/pulseaudio.service /usr/lib/systemd/user/pulseaudio.disabled_service
#mv /usr/lib/systemd/user/pulseaudio.socket /usr/lib/systemd/user/pulseaudio.disabled_socket

## see: https://www.raspberrypi.org/forums/viewtopic.php?t=156120
cp pulseaudio.service /etc/systemd/system/
systemctl daemon-reload
systemctl start pulseaudio
systemctl enable pulseaudio

## see: https://github.com/ev3dev/ev3dev.github.io/pull/24/files
cp after/system.pa /etc/pulse/
cp after/pulseaudio-system.conf /etc/dbus-1/system.d/
cp /etc/pulse/system.pa before/
cp /etc/dbus-1/system.d/pulseaudio-system.conf before/

## see: https://www.raspberrypi.org/forums/viewtopic.php?t=156120
#crontab -l
#@reboot sleep 15 && /home/pi/autoConnect.sh
