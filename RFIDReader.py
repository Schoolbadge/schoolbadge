import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522 #simplified library for tag reader

def RFIDReader():
    return SimpleMFRC522()
    
