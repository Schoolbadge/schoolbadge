

#import RpiSetup as rpi
#import RFIDReader 
#import FunLib
#from datetime import datetime, timedelta   

from distutils.log import Log
import Logger as Logger
import RpiMock as rpi
import RFIDReader as reader
import FunLib as funlib
from datetime import datetime, timedelta
import time

#definition of variables
LoopOn = 1
mediaDir = "/home/pi/Schoolbadge/media/" #For movies
imageDir = "/home/pi/Schoolbadge/images/" #For pictures
soundDir = "/home/pi/Schoolbadge/sound/" #For sounds
#mediaDir = '/media/pi/UDISK/Schoolbadge/media/' #from 7/10/2021 issues wih USB stick - no longer in use
logbestand = "20210913.csv"

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

def succesmovie(): # show a movie on succes
   rpi.playMovie()


def succesimage(): # show image on bading
    rpi.showPicture()

def successound(): # play succesfull sound
    rpi.playSound()

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



scannedBadgeIds = []
aantalsucces = 0

deviceConfig = rpi.start()
Logger.log("Rpi Started", deviceConfig['ref'], Logger.Level.INFO)

#program loop - this one should allways be kept running (~error handling to add)
while (LoopOn == 1):
    id, text = reader.Read();
    Logger.log("Id scanned: ", id, deviceConfig['ref'], Logger.Level.INFO) 
    if (id not in scannedBadgeIds):                
        scannedBadgeIds.append(id)
        funlib.success(rpi) #sending the text was for visual perposes, but now, text is no longer correct (numbering scheme has been changed)    
    else:
        funlib.fail(rpi)
    CheckTime() #to add time-relevant functions, like sleep, or make new log file  

rpi.stop()

