import random
import os
import glob


def success(rpi, deviceConfig):
    successLib = os.path.join(deviceConfig['mediaDirPath'], 'success/**/*')
    print(successLib)
    mediaFilePath = getRandomFile(successLib)    
    rpi.playMovie(mediaFilePath)


def fail(rpi):
    rpi.playMovie("media/fail/nee.mp4")


def getRandomFile(mediaDirPath):
    movieFilePath = random.choice(glob.glob(mediaDirPath, recursive=True))
    return movieFilePath
