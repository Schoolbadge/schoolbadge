import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522 #simplified library for tag reader

# def RFIDReader():
#     sys.path.append('/home/pi/MFRC522-python')
#     return SimpleMFRC522()

reader = SimpleMFRC522()
    
try:
    while True:
        print("Hold a tag near the reader")
        id, text = reader.read()
        print("ID: %s\nText: %s" % (id,text))
except KeyboardInterrupt:
    GPIO.cleanup()
    raise