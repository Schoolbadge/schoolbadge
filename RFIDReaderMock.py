
class RFIDReader():
    def __init__(self):
        print("RFIDReaderMock.__init__()")
    def read_no_block(self):
        return "123456789", "RFIDReaderMock"