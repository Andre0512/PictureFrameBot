#!/bin/sh
DISPLAY=:0
xset -dpms
xset s off
xset s noblank
matchbox-window-manager &
unclutter &
midori -e Fullscreen 
rm -f /home/pi/PictureFrameBot/Fullscreen
