# Real Rpi Setup
#import RpiSetup as rpi
#import RFIDReader as reader
#import FunLib as funlib

# Windows Mock Setup
import Logger as Logger
import RpiMock as rpi
import RFIDReaderMock as reader
import FunLib as funlib

# definition of variables
LoopOn = 1
scannedBadgeIds = []
aantalsucces = 0

deviceConfig = rpi.start()
Logger.log("Rpi Started", "",  deviceConfig['ref'], Logger.Level.INFO)

while (LoopOn == 1):
    result = reader.Read()
    Logger.log("Id scanned: ", id, deviceConfig['ref'], Logger.Level.INFO)
    if (id not in scannedBadgeIds):
        scannedBadgeIds.append(id)
        # sending the text was for visual perposes, but now, text is no longer correct (numbering scheme has been changed)
        funlib.success(rpi)
    else:
        funlib.fail(rpi)

rpi.stop()
