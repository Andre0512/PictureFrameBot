# Digital Picture Frame with Telegram Bot
#### This Project is to controll a digital Picture Frame with a Telegram Bot

## Idea 
* Digital Picture Frame is connected via HDMI to a Raspberry Pi
* The Raspberry Pi with Raspbian starts on Boot a fullscreen webbrowser 
* The webborwser is controlled by a python script 


## Installation

### Install Raspbian Jessie

1. Install Raspbian Debian Jessie

2. `sudo raspi-config`
	- Update the Raspi config tool (Advanced Options)
	- Enable SSH
	- Disable overscan. (Advanced Options)

3. Start the terminal and update your system:
	```
    sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get dist-upgrade -y && sudo apt-get autoremove -y && sudo reboot
	```

### Autostart Chromium on boot

1. Install unclutter (hide the cursor from the screen)
	```
	sudo apt-get install unclutter
	```

2. When the GUI starts up chromium needs to boot in kiosk-mode and open the webpage. Because of that we edit the autostart file:
	```
	nano ~/.config/lxsession/LXDE-pi/autostart
	```

	The autostart files needs to look like this:
	```
    @lxpanel --profile LXDE-pi
	@pcmanfm --desktop --profile LXDE-pi
	@xscreensaver -no-splash
	@xset s off
	@xset -dpms
	@xset s noblank
	@sed -i 's/"exited_cleanly": false/"exited_cleanly": true/' ~/.config/chromium Default/Preferences
	@chromium-browser --noerrdialogs --kiosk chrome://newtab/ --incognito --disable-translate
	@unclutter -display :0 -noevents -grab
	```