# Real Rpi Setup
# import Logger
# import RpiSetup as rpi
# import RFIDReader as reader
# import FunLib as funlib

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
Logger.log("Schoolbadge started", "",  deviceConfig['ref'], Logger.Level.INFO)

try:
    while (LoopOn == 1):
        id, text = reader.Read()
        Logger.log("Badge scanned ", id,
                   deviceConfig['ref'], Logger.Level.INFO)
        if (id not in scannedBadgeIds):
            scannedBadgeIds.append(id)
            # sending the text was for visual perposes, but now, text is no longer correct (numbering scheme has been changed)
            funlib.success(rpi)
        else:
            funlib.fail(rpi)
except KeyboardInterrupt:
    Logger.log("Schoolbadge stopped", "",
               deviceConfig["ref"], Logger.Level.ERROR)
    rpi.stop()
