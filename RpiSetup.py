import RPi.GPIO as GPIO
import time
import vlc
import json


relais_gpio = 17  # pin number for screen relais
media_player = vlc.MediaPlayer()
media_player.retain()


def start():
    GPIO.cleanup()
    media_player.toggle_fullscreen()
    GPIO.setmode(GPIO.BCM)  # board numbers
    # setup phase (klaarzetten voor loop)
    GPIO.setup(relais_gpio, GPIO.OUT)  # GPIO assign mode
    GPIO.output(relais_gpio, GPIO.HIGH)  # screen off

    with open('conf/device-conf.json', 'r') as configFile:
        conf = json.load(configFile)
    return conf


def stop():
    media_player.release()
    GPIO.output(relais_gpio, GPIO.LOW)  # screen on
    GPIO.cleanup()


def playMovie(path):
    media_player.set_media(vlc.Media(path))
    media_player.play()

    GPIO.output(relais_gpio, GPIO.LOW)  # screen on

    time.sleep(1.5)
    duration = media_player.get_length() / 1000
    time.sleep(duration)

    GPIO.output(relais_gpio, GPIO.HIGH)  # screen off


def showPicture(path):
    media = vlc.Media(path)
    media_player.set_media(media)
    media_player.play()
    GPIO.output(relais_gpio, GPIO.LOW)  # screen on
    time.sleep(1)
    Duur = 2
    time.sleep(Duur)  # makes a total of 3 seconds for the image
    GPIO.output(relais_gpio, GPIO.HIGH)  # screen off


def playSound(path):
    media = vlc.Media(path)
    media_player.set_media(media)
    media_player.play()
    # GPIO.output(relais_gpio, GPIO.LOW) #screen on (not needed for sound)
    time.sleep(3)
    #Duur = 2
    # time.sleep(Duur)
    media_player.pause()
    # GPIO.output(relais_gpio, GPIO.HIGH) #screen off
