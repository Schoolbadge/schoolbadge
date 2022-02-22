

import RPi.GPIO as GPIO
import os, random, time
import vlc


relais_gpio = 17 #pin number for screen relais
mediaDir = "/home/pi/Schoolbadge/media/" #For movies
imageDir = "/home/pi/Schoolbadge/images/" #For pictures
soundDir = "/home/pi/Schoolbadge/sound/" #For sounds
media_player = vlc.MediaPlayer()

def start():
    media_player.toggle_fullscreen()
    GPIO.setmode(GPIO.BCM) #board numbers
    #setup phase (klaarzetten voor loop)
    GPIO.setup(relais_gpio, GPIO.OUT) #GPIO assign mode
    GPIO.output(relais_gpio, GPIO.HIGH) #screen off

def stop():
    GPIO.output(relais_gpio, GPIO.LOW) #screen on
    GPIO.cleanup() 

def playMovie():
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

def showPicture():
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

def playSound():
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
    