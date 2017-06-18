#!/bin/bash


pidir="/home/pi/.config/midori/config"
rootdir="/root/.config/midori/config"

setting=$(cat << 'EOF'
[settings]
default-encoding=ISO-8859-1
enable-site-specific-quirks=true
last-window-width=1920
last-window-height=1080
last-panel-position=254
load-on-startup=MIDORI_STARTUP_HOMEPAGE
homepage=file:///home/pi/PictureFrameBot/html/startpage.html
location-entry-search=https://duckduckgo.com/?q=%s
open-new-pages-in=MIDORI_NEW_PAGE_CURRENT
open-tabs-next-to-current=false
enable-spell-checking=false
enable-html5-database=true
user-agent=Mozilla/5.0 (Macintosh; U; Intel Mac OS X; de-de) AppleWebKit/535+ (KHTML, like Gecko) Version/5.0 Safari/535.22+ Midori/0.4
EOF
)


mkdir -p /home/pi/.config/midori
echo "$setting" > "$pidir"
echo "$setting" > "$rootdir"
