import random
import Logger as Logger
class RFIDReader():
    

    def __init__(self):
        print("RFIDReaderMock.__init__()")
    
    def read_no_block(self):
        r = random.randint(0, 1)        
        if (r == 1):
            id = "123456789"
            text = "RFIDReaderMock"
            return id, text
        else:
            Logger.log('RFIDReaderMock.read_no_block() failed: id: None text: leeg', Logger.Level.WARN)
            return None, "leeg"