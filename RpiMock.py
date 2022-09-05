import vlc
import time
import json

media_player = vlc.MediaPlayer()

def start():
    print('rpi started')
    media_player.toggle_fullscreen()
    with open('data/device-conf.json', 'r') as configFile:
        conf = json.load(configFile)    
    return conf

def stop(event):
    print('rpi stop')

def playMovie(path):
    media_player.set_media(vlc.Media(path))
    media_player.play()
    time.sleep(1.5)
    duration = media_player.get_length() / 1000
    time.sleep(duration)    

def showPicture(path):
    pictureMedia = vlc.Media(path)
    media_player.set_media(pictureMedia)
    media_player.play()
    

def playSound():
    print('rpi play sound')

