import random
import os

moviesDir = "/home/pi/schoolbadge/media/movies"  # For movies
picturesDir = "/home/pi/schoolbadge/media/pictures"  # For pictures
soundsDir = "/home/pi/schoolbadge/media/sounds"  # For sounds


def getPicture():
    return


def getMovie():
    movieFile = random.choice(os.listdir(moviesDir))
    movieFilePath = os.path.join(moviesDir, movieFile)
    return movieFilePath


def getSound():
    return

 # this function decides wheter a movie, sound or image is played, based on school lady preferences (1/5 is movie, 2/5 is audio, 2/5 is image)


def success(rpi):
    movieFilePath = getMovie()
    rpi.playMovie(movieFilePath)


def fail(rpi):
    rpi.playMovie("media/nee.mp4")
