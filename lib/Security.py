from gpiozero import Button
from signal import pause
import time, datetime
from lib import Logger

class Security(object):
    btnPassenger = Button(13) #passenger door
    btnDriver = Button(14) #driver door

    def door_open(self, btn):
        if btn == self.btnPassenger:
            self.logger.log("Passenger door opened")
        elif btn == self.btnDriver:
            self.logger.log("Driver door opened")

    def door_closed(self, btn):
        if btn == self.btnPassenger:
            self.logger.log("Passenger door closed")
        elif btn == self.btnDriver:
            self.logger.log("Driver door closed")

    def __init__(self):
        self.logger = Logger.Logger(self)
        self.btnPassenger.when_released = self.door_open
        self.btnDriver.when_released = self.door_open
        self.btnPassenger.when_pressed = self.door_closed
        self.btnDriver.when_pressed = self.door_closed

    def start(self):
        self.logger.log("Listening for door events...")
        pause()
