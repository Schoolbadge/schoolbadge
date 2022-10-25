import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522  # simplified library for tag reader

reader = SimpleMFRC522()


def Read():
    print('Toon mij maar jouw badge.')
    id, text = reader.read()
    return id, text
