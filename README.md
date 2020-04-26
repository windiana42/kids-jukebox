# Kids Jukebox - Self build tutorial using Raspberry Pi

## Introduction:

A jukebox is probably more outdated than anything playing music that we know
today. But none the less, it delivered the most classy experience of listening. 

![jukebox](/doc/pics/diner-clipart-jukebox-6-original.png?raw=true)

The idea of building a jukebox for kids came during christmas unpacking
several CDs which might be another means of listening to music endangered
of extinction. Yet, CDs deliver a nice haptic sense of control that
especially kids love in an age where they cannot read and thus are not yet
capable of dealing with graphical iPod displays.

Thus, I wanted to build a haptic touchpad for controlling which music to play
using a Raspberri Pi and the bluetooth speaker I have at hand. It is the
perfect extension of the tigerbox
([amazon](https://www.amazon.de/tigerbox-Musik-Mix-Jetzt-H%C3%B6rbox-Lautsprecher/dp/B077MT8Z6N))
if you do not buy into the cards feature where you need to pay for content again.

The conrete idea of building materials came from random sightings within the
house, starting with a magnet in my pocket and cotton pads on the
changing table.

Here is how the result currently looks:

![complete](/doc/pics/complete.jpg?raw=true)

If you manage to build a nicer version, I would be thrilled to receive
your photos!

## Prerequisites:

Besides a Raspberry Pi and a random bluetooth speaker, you need the following material:

![material](/doc/pics/material.jpg?raw=true)

- aluminium foil (I used what I found in the kitchen and cut it in 1.5cm wide
lanes)
- thumbtacks (I only found ones with plastic cover that I removed with a pair
of pliers)
- cotton pads or any other material that is soft, may be compressed and
creates a force against the pressure
- pin board made from cork (> 40cm x 30cm)
- sheet protector to allow chaning the song album selection easily
- 1-2 strong magnets as from photo ropes [i.e from Amazon](https://www.amazon.com/Walther-MD150B-Strong-Neodymium-Magnets/dp/B000VI38PA/ref=sr_1_7?dchild=1&keywords=magnet+picture+rope&qid=1587910544&sr=8-7)

I used a raspberry pi 4b 1GB for less than 40 USD. Other versions with bluetooth support should do fine
as well. Minor adaptions of the code might be needed. Please let me know if
you have problems in geting it to work.
- Raspberry 4b [i.e 2GB from Reichelt](https://www.reichelt.com/ch/de/raspberry-pi-4-b-4x-1-5-ghz-2-gb-ram-wlan-bt-rasp-pi-4-b-2gb-p259919.html?&trstct=pos_1&nbc=1)
- Normal USB-C Power supply
[i.e from Reichelt](https://www.reichelt.com/ch/de/raspberry-pi-netzteil-5-1-v-3-0-a-usb-type-c-eu-stecker-s-rpi-ps-15w-bk-eu-p260010.html?&trstct=pos_0&nbc=1)
- 2x cable with crocodile clips [i.e from
Reichelt](https://www.reichelt.com/ch/de/entwicklerboards-steckbrueckenkabel-20cm-10-polig-auf-krokodi-debo-kabelset6-p242774.html?&trstct=pos_0&nbc=1)
- 10x 2kOhm resistor [from Reichelt](https://www.reichelt.com/ch/de/duennschichtwiderstand-axial-0-4-w-2-kohm-1-vi-mba02040c2001-p233633.html?&trstct=pos_10&nbc=1)

## Hardware Setup:

![grid](/doc/pics/grid.jpg?raw=true)

The aluminium foil works as a conductor just like a cable. You can pin stripes
of it on the board using the thumbtacks. I suggest putting the 4 long stripes
down first with 6 thumbtacks on each stripe with a 2cm by 2cm cotton pad piece
underneath. Press the thumbtacks firmly such that the cotton pad gets higher at
the corners. The 4 times 6 = 24 thumbtacks with cotton pads underneath should
cover the area that you like to use as touch pad (I used A4 format). Then add
the 6 shorter stripes on top with a thumbtack above and below the touch
pad area. They must be placed with high strain, so their surface does not
touch the 24 thumbtacks of the touch pad.

Here is a detailed view of the cotton pads in action:

![grid detail](/doc/pics/grid_detail.jpg?raw=true)

After adding the sheet protector and the magnet on a random thumbtack it looks
like this:

![complete touchpad](/doc/pics/complete_touchpad?raw=true)

Finally, you need to connect the 4 long stripes and the 6 short stripes to the
GPIO section of the Raspberry Pi. Please bear in mind that the Raspberry GPIO
pins have no protection against short circuits. It may easily fry the
device. That is why I put a 2kOhm resistor to each stripe of the touchpad with
another thumbtack and connected the crocodile clips coming from the GPIO pins
only to the other side of the resistors.

In my setup I used the GPIO pins 23, 22, 27 and 17 for the 4 long stripes from
top to bottom and the pins 16, 26, 13, 12, 6, 5 for the 6 short stripes from
left to right.

## Software prerequisites:

I [setup](https://www.raspberrypi.org/downloads/raspbian/) my raspberry by copying [Raspbian Buster
full](https://downloads.raspberrypi.org/raspbian_full_latest) on the micro SD
card of the raspberry pi. Then I added an empty file called `ssh` to the boot
folder in order to activate
the ssh server and configured the wifi-connection of the raspberry by
placing another file called `wpa_supplicant.conf` on the card according to this
[instruction](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md).

Please make sure you installed python3 and you have it on the path. This
should be the case for raspbian buster full.

## Software Installation:

The code in this repo is just a quick-hack prototype of the idea. However, it
works too well to do it right. If you like to build other things with the
touchpad, please let me know. I am willing to implement a nice gpiozero
wrapper in case someone actually uses it.

Configuration:
- You need to put the mac address of the bluetooth speaker you like to connect
in two locations. There are .example files in the repo that you can copy and modify.
  - `kids_jukebox/connect`
  - `pulseaudio/autoConnect.sh`
- Please make sure you used the exact same GPIO pins as hard-coded in the
source code:
  - `kids_jukebox/kids_jukebox.py`
  - `mytouchpad/mytouchpad.py`
- Copy or link 23 directories with sound files that can be played by vlc to
`kids_jukebox/playlist/current/0` up to
`kids_jukebox/playlist/current/22`. Each directory is an album.
  - Number 23 does not exist since the field bottom right is reserved to
  shutdown the jukebox
  - Please look at `kids_jukebox/playlist/readme.txt` if you like to support
  multiple sets of albums. They can be changed on startup using two magnets.

The code can be installed on your pi using:
- `rsync -av buttons kids_jukebox mytouchpad pulseaudio pi@pi:`
Where the pi at the end is the host name of the raspberry pi.

Log into your raspberry with ssh and run as user pi:
```bash
cd ~/pulseaudio; ./setup_pulseaudio.sh; cd -;
cd ~/kids_jukebox; ./setup.sh; cd -;
cd ~/buttons; ./setup.sh; cd -;
```

Restart your raspberry to see whether it works reliably.

You can use [this template](print_templates/example.odp) to put your album cover pictures
and/or album names on the touchpad. The orange circles are meant for the case with multiple 
sets of albums where you can change the set with two magnets on the orange circled fields.

I hope you and your kids enjoy the jukebox and the touchpad!
Please let me know if you have trouble following these instructions.
Feel free to add issues or pull requests to this repo.

## Problem solving:

Whenever you change the magnet, kids_jukebox will try to reconnect to the bluetooth speaker. 
This solves quite some connectivity problems. It would be possible to monitor the status of 
pulseaudio and try to reconnect as long as no speaker is connected. But again, this is just a 
quick-hack prototype that happens to work pretty well for me.

If you just want to test your touchpad, you can disable the kids_jukebox
service using `systemctl --user stop kids_jukebox` and run
`mytouchpad/mytouchpad.py`.
It will display the touch pad points that it detects as pressed and it will
show in brackets how often it detected those when trying to detect 5
times. The touch pad points are numbered 0 to 23 from top left to bottom
right. The kids_jukebox only reacts to changes of the magnet if it finds 5 
consecutive measurements pointing to only a single magnet on one field of the touchpad.

Please, bear in mind that the kids_jukebox service will shutdown the raspberry pi when
placing the magnet on field 23 (bottom right).
