# Real Rpi Setup
import Logger
import RpiSetup as rpi
import RFIDReader as reader
import FunLib as funlib
import sys
import traceback

# Windows Mock Setup
# import Logger as Logger
# import RpiMock as rpi
# import RFIDReaderMock as reader
# import FunLib as funlib

# definition of variables
LoopOn = 1
scannedBadgeIds = []
aantalsucces = 0

deviceConfig = rpi.start()


def exception_handler(exception_type, value, tb):
    Logger.exception(
        exception_type, deviceConfig['ref'], traceback.extract_tb(tb))


Logger.log(Logger.Level.INFO, "Schoolbadge started",
           "",  deviceConfig['ref'], "")
sys.excepthook = exception_handler
try:
    while (LoopOn == 1):
        id, text = reader.Read()
        Logger.log(Logger.Level.INFO, "Badge scanned ", id,
                   deviceConfig['ref'], "")
        if (id not in scannedBadgeIds):
            scannedBadgeIds.append(id)
            if (len(scannedBadgeIds) >= deviceConfig['scannedBadgesCacheSize']):
                scannedBadgeIds = []
            # sending the text was for visual perposes, but now, text is no longer correct (numbering scheme has been changed)
            funlib.success(rpi)
        else:
            funlib.fail(rpi)
except KeyboardInterrupt:
    Logger.log(Logger.Level.ERROR, "Schoolbadge stopped",
               "", deviceConfig["ref"], "KeyboardInterrupt")
    rpi.stop()
