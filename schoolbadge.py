

#this version is designed for offline use, but with wifi (internet) for time

#hardware
# 1. mfrc522 RFID badge reader
# 2. raspberry Pi 3 B
# 3. one relay (turning on and off usb power to screen)
# 4. hmdi screen with usb power (7-8 inch ~) 1024*600
# 5. usb-powered cheap speakers
# 6. 5V Ip65 ~15 Watt transfo
# 7. watertight enclosure

#things learned so far:
# running from shell script changes folder it's running from - hence use of full paths :-)
# using usb stick got wonky - direct referral didn't work anymore - hence only SD (for now)

###### TO DO ##### - NOT in order of importance :-) ##################################""
# 1. add some kind of fault intercept/error handling to keep it running
# 2. add some kind of weekly/ daily mail with the data
# 3. instead of mail --> push reading to internet (but keap a log on sd card)
# 4. make raspberry pi accesible from internet (https://magpi.raspberrypi.com/articles/remote-access-your-raspberry-pi-securely)
# 5. stop making 2 log files
# 6. add some kind of error log (for fault investigations)
# 7. add more visual feedback on sound playback
# 8. activate sleep routines - maybe better to externalise those (use seperate programmable timer on the mains?)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) #board numbers
import sys
sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522 #simplified library for tag reader
import subprocess
import os, random
import time
from datetime import datetime, timedelta   
import vlc

#definition of variables
reader = SimpleMFRC522()
LoopOn = 1
mediaDir = "/home/pi/Schoolbadge/media/" #For movies
imageDir = "/home/pi/Schoolbadge/images/" #For pictures
soundDir = "/home/pi/Schoolbadge/sound/" #For sounds
#mediaDir = '/media/pi/UDISK/Schoolbadge/media/' #from 7/10/2021 issues wih USB stick - no longer in use
logbestand = "20210913.csv"
relais_gpio = 17 #pin number for screen relais
media_player = vlc.MediaPlayer()
media_player.toggle_fullscreen()
aantalsucces = int(0) # number for succesfull badge attempts

#setup logfile on reboot (= 1e day of the week)
Nu = datetime.now()
Dag = int(Nu.strftime("%u")) #maandag = 1, zondag 7
Maandag = Nu
if Dag != 1:
    Dag = Dag - 1
    Maandag = Nu - timedelta(days=Dag) 

#logbestand = "/media/pi/UDISK/Schoolbadge/Logs/" + Maandag.strftime("%Y%m%d") + ".csv"
logbestand = "/home/pi/Schoolbadge/LogUSB/" + Maandag.strftime("%Y%m%d") + ".csv"
logsbestandSD = "/home/pi/Schoolbadge/LogSD/" + Maandag.strftime("%Y%m%d") + ".csv"

#functions

def succesmovie(text): # show a movie on succes
   
    mediaFile = random.choice(os.listdir(mediaDir))
    mediaFilePath = os.path.join(mediaDir, mediaFile)
    
    media = vlc.Media(mediaFilePath)
    media_player.set_media(media)
   
    media_player.play()
    GPIO.output(relais_gpio, GPIO.LOW) #screen on
    time.sleep(1) # before reading media player for lenght, we have to wait, otherwise mediaplayer is not yet ready ;-)
    Duur = media_player.get_length() #in miliseconds
    Duur = Duur/1000-1
    time.sleep(Duur)
    GPIO.output(relais_gpio, GPIO.HIGH) #screen off

def succesimage(text): # show image on bading
    mediaFile = random.choice(os.listdir(imageDir))
    mediaFilePath = os.path.join(imageDir, mediaFile)
    media = vlc.Media(mediaFilePath)
    media_player.set_media(media)
    media_player.play()
    GPIO.output(relais_gpio, GPIO.LOW) #screen on
    time.sleep(1)
    Duur = 2
    time.sleep(Duur) #makes a total of 3 seconds for the image
    GPIO.output(relais_gpio, GPIO.HIGH) #screen off

def successound(text): # play succesfull sound
    mediaFile = random.choice(os.listdir(soundDir))
    mediaFilePath = os.path.join(soundDir, mediaFile)
    media = vlc.Media(mediaFilePath)
    media_player.set_media(media)
    media_player.play()
    #GPIO.output(relais_gpio, GPIO.LOW) #screen on (not needed for sound)
    time.sleep(3)
    #Duur = 2
    #time.sleep(Duur)
    media_player.pause()
    #GPIO.output(relais_gpio, GPIO.HIGH) #screen off

def success(text): #this function decides wheter a movie, sound or image is played, based on school lady preferences (1/5 is movie, 2/5 is audio, 2/5 is image)
    global aantalsucces #global declaration needed for use in function
    aantalsucces = aantalsucces + 1
    # show images
    if aantalsucces == 1 or aantalsucces == 3:
        succesimage(text)
    # show movies
    if aantalsucces == 5:
        aantalsucces = 0
        succesmovie(text)
    # play sound
    if aantalsucces == 2 or aantalsucces == 4:
        successound(text)

def CheckRFID5min():
    #tis is a loop that checks the rfid reader for 5 minutes 
    starttijd = datetime.now()
    text = "leeg"
    while ((datetime.now()-starttijd) <timedelta(seconds=300) ):
        id, text = reader.read_no_block()  #read reader once
        if id != None:
            print(id,"-",text)
            return id, text
        time.sleep(0.2) #to sleep x seconds --> we don't want to overdo it :-) - 0.2 was arbitrary chosen
    return 0, "leeg"

# writing the data
def WriteToLog(id, text):
    with open(logbestand,"a") as log, open(logsbestandSD, "a") as logSD: #you can open 2 files at once (faster)
        logstring = str(id)+','+ text
        log.write("{0},{1}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),str(logstring)))
        logSD.write("{0},{1}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),str(logstring)))

def CheckTime(): #this one is to do certain things at certain moments (like, sleep longer in the weekends, for now, it's only to change log file in the weekend)
    Nu = datetime.now()
    Dag = Nu.strftime("%u") #maandag = 1, zondag 7
    Uur = int(Nu.strftime("%H"))
    Datum = Nu.strftime("%Y%m%d")
    # Min = int(Nu.strftime("%M")) #minuten nodig?
    
    # if (Uur >= 21):
        #time.sleep(1) # 9 uur in seconden 32400 --> van 21u tot 6u
        #copy van log maken naar usb stick? of liever per uur? --> veranderd in gewoon dubbel loggen
        #sleep functie voorlopig bypassed - latere versie
    if (Dag == 7):
        # time.sleep(2) # 24 uur (zondag 6u 86400 --> maandag 6u)
        # in deze versie zal 'm dat dus de ganse dag opnieuw doen, maar voorlopig is dat ok
        logbestand = "/media/pi/UDISK/Schoolbadge/Logs/" + Datum + ".csv" #dus 1x per week een nieuwe bestandsnaam
        logsbestandSD = "/home/pi/Schoolbadge/LogSD/" + ".csv" + Datum + ".csv"

#setup phase (klaarzetten voor loop)
GPIO.setup(relais_gpio, GPIO.OUT) #GPIO assign mode
GPIO.output(relais_gpio, GPIO.HIGH) #screen off

#these are for remembering the last 5 badge attempts
id5 = 0 
id4 = 0
id3 = 0
id2 = 0
id1 = 0

#program loop - this one should allways be kept running (~error handling to add)
while (LoopOn == 1):
    id, text = CheckRFID5min() 
    #checks RFID for 5 minutes - when managed to scan one, everything is returned (id and text are 2 string variables, id is factory unique)
    #er wordt gedurende 5 min naar RFID gezocht. Indien vroeger geregistreerd, wordt alles gereturned
    #if (id != 0) and (id != id5) and (id != id4) and (id != id3) and (id != id2) and (id != id1): #current id may not be equal to last 5 
    # this line above was changed in the one under - for testing perposes remembering the last 5 id's was ... not handy
    if (id != 0) and (id != id1): #current id may not be equal to last 1 
        success(text) #sending the text was for visual perposes, but now, text is no longer correct (numbering scheme has been changed)
        WriteToLog(id, text) # writing the result to log - internet says this could take 0.3 seconds
        #move up last 5 id's
        id5 = id4 
        id4 = id3
        id3 = id2
        id2 = id1
        id1 = id
    CheckTime() #to add time-relevant functions, like sleep, or make new log file  


#ending

GPIO.output(relais_gpio, GPIO.LOW) #screen on
GPIO.cleanup() 
# these are funny, because this program actually never ends except for RUD