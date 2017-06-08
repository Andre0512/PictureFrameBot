#!/bin/sh
DISPLAY=:0
xset -dpms
xset s off
xset s noblank
rm -f /home/pi/PictureFrameBot/Fullscreen
matchbox-window-manager &
unclutter &
midori -e Fullscreen 
