import random
import os
import vlc
import time

mediaFilePath = 'C:\Me\Projects\schoolbadge\media\dansendekat.mp4'
media_player = vlc.MediaPlayer()
_finishedCallback = None

def start():
    print('rpi started')

def stop(event):
    print('rpi stop')

def playMovie():
   # mediaFile = random.choice(os.listdir(mediaDir))
    #mediaFilePath = os.path.join(mediaDir, mediaFile)
    media = media_player.set_media(vlc.Media(mediaFilePath))
    media_player.play()
    time.sleep(1.5)
    duration = media_player.get_length() / 1000
    time.sleep(duration)

def showPicture():
    print('rpi show picture')

def playSound():
    print('rpi play sound')

