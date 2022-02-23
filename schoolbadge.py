

#import RpiSetup as rpi
#import RFIDReader 
#import FunLib
#from datetime import datetime, timedelta   

import Logger as Logger
import RpiMock as rpi
import RFIDReaderMock as RFIDReader
import FunLib as funlib
from datetime import datetime, timedelta

#definition of variables
reader = RFIDReader.RFIDReader()
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


def CheckRFID5min():
    #tis is a loop that checks the rfid reader for 5 minutes 
    starttijd = datetime.now()
    text = "leeg"
    while ((datetime.now()-starttijd) <timedelta(seconds=300) ):
        id, text = reader.read_no_block()  #read reader once
        if id != None:
            print(id,"-",text)
            return id, text
        time.sleep(0.2) #to sleep x seconds --> we don't want to overdo it :-) - 0.2 was arbitrary chosen
    return 0, "leeg"

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



#these are for remembering the last 5 badge attempts
id5 = 0 
id4 = 0
id3 = 0
id2 = 0
id1 = 0

aantalsucces = 0

rpi.start();
Logger.log('Started', 'debug')

#program loop - this one should allways be kept running (~error handling to add)
while (LoopOn == 1):
    id, text = CheckRFID5min() 
    #checks RFID for 5 minutes - when managed to scan one, everything is returned (id and text are 2 string variables, id is factory unique)
    #er wordt gedurende 5 min naar RFID gezocht. Indien vroeger geregistreerd, wordt alles gereturned
    #if (id != 0) and (id != id5) and (id != id4) and (id != id3) and (id != id2) and (id != id1): #current id may not be equal to last 5 
    # this line above was changed in the one under - for testing perposes remembering the last 5 id's was ... not handy
    if (id != 0) and (id != id1): #current id may not be equal to last 1 
        funlib.success(rpi, text) #sending the text was for visual perposes, but now, text is no longer correct (numbering scheme has been changed)
        
        #WriteToLog(id, text) # writing the result to log - internet says this could take 0.3 seconds
        #move up last 5 id's
        id5 = id4 
        id4 = id3
        id3 = id2
        id2 = id1
        id1 = id
    CheckTime() #to add time-relevant functions, like sleep, or make new log file  

rpi.stop();

