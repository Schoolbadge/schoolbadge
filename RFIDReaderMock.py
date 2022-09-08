import random
import Logger as Logger


def Read():
    r = random.randint(0, 1)
    if (r == 1):
        value = random.choice(
            [("id123", "text123"), ("id456", "text456"), ("id789", "text789")])
        return value
    else:
        Logger.log(
            'RFIDReaderMock.read_no_block() failed: id: None text: leeg', "", "", Logger.Level.WARN)
        return None, "leeg"
