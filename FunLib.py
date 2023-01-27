import random
import os


def success(rpi, deviceConfig):
    movieFilePath = getRandomFile(deviceConfig["mediaDirPath"])
    rpi.playMovie(movieFilePath)


def fail(rpi):
    rpi.playMovie("media/nee.mp4")


def getRandomFile(mediaDirPath):
    movieFilePath = random.choice([x for x in os.listdir(
        mediaDirPath) if os.path.isfile(os.path.join(mediaDirPath, x))])
    return movieFilePath
