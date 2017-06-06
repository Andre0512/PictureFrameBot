# Digital Picture Frame with Telegram Bot
#### This Project is to controll a digital Picture Frame with a Telegram Bot

## Table of contents
1. [Setup Raspberry Pi](#1-setup-raspberry-pi)  
 1.1. [Install Raspbian Jessie](#11-install-raspbian-jessie)  
 1.2. [Update Rasperry Pi configurations](#12-update-rasperry-pi-configurations)  
 1.3. [Checkout this repository](#12-checkout-this-repository)  
 1.4. [Autostart Midori on boot](#12-autostart-midori-on-boot)  

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

### 1.2 Update Rasperry Pi configurations
Enter the following command to change the Raspberry Pi settings:
```
sudo raspi-config
```

1. Navigate to **3 Boot Options**, choose **B1 Desktop / CLI** and then choose **B2 Console Autologin**
2. If you have a black frame on your display, navigate to **7 Advanced Options**, choose **A2 Overscan** and choose **yes**

### 1.3 Checkout this repository
```
cd ~
git clone https://local.abasche.de/git/Andre/Picture-Frame-Bot
```

### 1.4 Autostart Midori on boot

#### 1.2.1 Why Midori?
With a sample slide show, I tested the startup time with different browsers on my Raspberry Pi Zero W:  
* Chromium: **22,7s**
* Epiphany: **8,1s**
* Firefox:  **30,1s**
* Midori:   **5,3s**

I choose the **Midori browser** because it was the fastest in my test scenario and was the easiest to configure for my project.

#### 1.2.2 Install Midori
Install Midori Browser, matchbox as running environment and unclutter for hidding cursor from screen:
```
sudo apt-get install midori unclutter matchbox
```

#### 1.2.3 Update browser settings
By default, Midori open pages on new tab. We need to change the following file:
```
nano ~/.config/midori/config
```
The following text must be added:

#### 1.2.4 Start at boot
Autostart Midori at boot with Cron:  
```
(crontab -l && echo "@reboot xinit /home/pi/Picture-Frame-Bot/start_midori.sh &") | sudo crontab -

```