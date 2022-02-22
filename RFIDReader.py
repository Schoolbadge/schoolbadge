import sys
from mfrc522 import SimpleMFRC522 #simplified library for tag reader

def RFIDReader():
    sys.path.append('/home/pi/MFRC522-python')
    return SimpleMFRC522()
    
