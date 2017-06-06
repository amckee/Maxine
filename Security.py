from gpiozero import Button
from signal import pause
import time

class Security(object):
    btn = Button(13)
    def __init__(self):
        
        print("Security imported")

    def prove_existance(self):
        print("I exist!")
