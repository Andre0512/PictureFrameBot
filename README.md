# Digital Picture Frame with Telegram Bot
#### This Project is to controll a digital Picture Frame with a Telegram Bot

## Table of contents
1. [Setup Raspberry Pi](#setup-raspberry-pi)  
 1.1. [Install Raspbian Jessie](#install-raspbian-jessie)  
 1.2 [Autostart Chromium on boot](#autostart-chromium-on-boot)

## Idea 
* Digital Picture Frame is connected via HDMI to a Raspberry Pi
* The Raspberry Pi with Raspbian starts on Boot a fullscreen webbrowser 
* The webborwser is controlled by a python script 


## 1. Setup Raspberry Pi

### 1.1. Install Raspbian Jessie ###

#### 1.1.1 Download Image 
Downlad and unzip [Raspbian Jessie with Pixel](https://www.raspberrypi.org/downloads/raspbian/)

#### 1.1.2. Format your sd card 
__On Windows:__
1. Download [SDFormatter](https://www.sdcard.org/downloads/formatter_4/)
2. Install Setup
3. Set _fomat size adjustment_ to _on_
4. Format sd card 

#### 1.1.3. Install Image 
__On Windows:__
1. Download [Win32DiskImager](https://sourceforge.net/projects/win32diskimager/)
2. Install Setup
3. Choose Raspbian Jessie as Image File and your sd card as device
4. Write

#### 1.1.4. Setup WiFi-Connection (optional) 
With the Raspberry Pi Zero W or the Raspberry Pi 3 It is possible to establish a wifi connection without connecting any USB device. Two files must be created on the boot partition before the first boot. An empty file named `ssh` and a file named `wpa_supplicant.conf` with the following content:
```
network={
       ssid="wifi-name"
       psk="passowrd"
       key_mgmt=WPA-PSK
}
```
After the first boot, you can connect to the Raspberry Pi via a ssh client like [Putty](http://www.putty.org/)  
`ssh pi@raspberrypi`  
Password: "raspberry"

#### 1.1.5. Update   
Start the terminal and update your system: 
```
sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get dist-upgrade -y && sudo apt-get autoremove -y && sudo reboot
```

### 1.2 Autostart Chromium on boot

#### 1.2.1 Install unclutter 
Install unclutter for hidding the cursor from the screen 
```
sudo apt-get install unclutter
```

#### 1.2.2 Update autostart file
When the GUI starts up chromium needs to boot in kiosk-mode and open the webpage. Because of that we edit the autostart file: 
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