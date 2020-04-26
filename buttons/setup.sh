set -x
#see: https://unix.stackexchange.com/questions/251211/why-doesnt-my-systemd-user-unit-start-at-boot
sudo cp bluetooth_to_vlc.service /etc/systemd/user/
systemctl --user daemon-reload
systemctl --user enable bluetooth_to_vlc
