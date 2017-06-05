#!/bin/sh
DISPLAY=:0
xset -dpms
xset s off
xset s noblank
matchbox-window-manager &
unclutter &
midori -e Fullscreen 
rm /home/pi/Picture-Frame-Bot/Fullscreen
