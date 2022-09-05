# schoolbadge

## components

- schoolbadge.py => RFID Reader

# test setup

## on windows

- use chocolatey to required software: choco install python3 vlc git
- clone the repository
- install dependency for pandas: sudo apt-get install libatlas-base-dev
- perform python install in project directory: python3 -m pip install -r requirements.txt
- run program: python3 ./schoolbadge.py

# hardware

1. mfrc522 RFID badge reader
2. raspberry Pi 3 B
3. one relay (turning on and off usb power to screen)
4. hmdi screen with usb power (7-8 inch ~) 1024\*600
5. usb-powered cheap speakers
6. 5V Ip65 ~15 Watt transfo
7. watertight enclosure

# things learned so far:

- running from shell script changes folder it's running from - hence use of full paths :-)
- using usb stick got wonky - direct referral didn't work anymore - hence only SD (for now)

# TO DO

- add some kind of fault intercept/error handling to keep it running
- add some kind of weekly/ daily mail with the data
- instead of mail --> push reading to internet (but keap a log on sd card)
- make raspberry pi accesible from internet (https://magpi.raspberrypi.com/articles/remote-access-your-raspberry-pi-securely)
- stop making 2 log files
- add some kind of error log (for fault investigations)
- add more visual feedback on sound playback
- activate sleep routines - maybe better to externalise those (use seperate programmable timer on the mains?)
