mediaDir = "/home/pi/Schoolbadge/media/" #For movies
imageDir = "/home/pi/Schoolbadge/images/" #For pictures
soundDir = "/home/pi/Schoolbadge/sound/" #For sounds

def getPicture():
    return

def getMovie():
    return

def getSound():
    return

 #this function decides wheter a movie, sound or image is played, based on school lady preferences (1/5 is movie, 2/5 is audio, 2/5 is image)
def success(rpi):    
    rpi.playMovie("media/sample-5s.mp4")
    

def fail(rpi):
    rpi.playMovie("media/nee.mp4")
