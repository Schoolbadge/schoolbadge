# schoolbadge

Start => Scan badge => Show movie / picture => Restart

## components

### hardware

1. mfrc522 RFID badge reader
2. raspberry Pi 3 B
3. one relay (turning on and off usb power to screen)
4. hmdi screen with usb power (7-8 inch ~) 1024\*600
5. usb-powered cheap speakers
6. 5V Ip65 ~15 Watt transfo
7. watertight enclosure

- schoolbadge.py => RFID Reader

# program setup

# prerequisites

## on windows

- use chocolatey to install required software: choco install python3 vlc git

## on raspberry pi

- sudo apt-get install libatlas-base-dev git

Authentication git:
=> create personal access token (PAT)

- add autostartup config
  on rpi: copy <schoolbadge-dir>/conf/schoolbadge.desktop => /etc/xdg/autostart

## general

- clone repository: `git clone https://github.com/Schoolbadge/schoolbadge.git`
- go to project directory: `cd schoolbadge`
- install required python modules: `python3 -m pip install -r requirements.txt`
- create 3 subfolders:
  - conf
  - media => images, videos
  - data => logging
- update device specific configuration in the configuration files
- run program: python3 ./schoolbadge.py
