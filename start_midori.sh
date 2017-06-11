#!/bin/sh
DISPLAY=:0
xset -dpms
xset s off
xset s noblank
rm -f /home/pi/PictureFrameBot/Fullscreen
mkdir -p /home/pi/PictureFrameBot/pictures
matchbox-window-manager &
unclutter &
python3 /home/pi/PictureFrameBot/Bot.py &
midori -e Fullscreen