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
def success(rpi, text):    
    print(text)
    #global aantalsucces #global declaration needed for use in function
    # aantalsucces = aantalsucces + 1
    # # show images
    # if aantalsucces == 1 or aantalsucces == 3:
    #     rpi.succesimage()
    # # show movies
    # if aantalsucces == 5:
    #     aantalsucces = 0
    #     rpi.succesmovie()
    # # play sound
    # if aantalsucces == 2 or aantalsucces == 4:
    #     rpi.successound()
    await rpi.playMovie()
