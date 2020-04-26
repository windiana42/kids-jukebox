set -x
#see: https://unix.stackexchange.com/questions/251211/why-doesnt-my-systemd-user-unit-start-at-boot
sudo cp kids_jukebox.service /etc/systemd/user/
sudo loginctl enable-linger pi
systemctl --user daemon-reload
systemctl --user enable kids_jukebox
