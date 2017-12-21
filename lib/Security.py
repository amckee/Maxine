from gpiozero import Button
from signal import pause
import logging, time, datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Security(object):
    ## Track door open/close activity
    ## Manage cameras on/off (storage?)
    ## Skimmer Scanner thread / alerts:
    ##  - https://github.com/sparkfunX/Skimmer_Scanner
    btnPassenger = Button(13) #passenger door
    btnDriver = Button(14)    #driver door

    def door_open(self, btn):
        if btn == self.btnPassenger:
            logger.info("Passenger door opened")
        elif btn == self.btnDriver:
            logger.info("Driver door opened")

    def door_closed(self, btn):
        if btn == self.btnPassenger:
            logger.info("Passenger door closed")
        elif btn == self.btnDriver:
            logger.info("Driver door closed")

    def setup_door_events(self):
        self.btnPassenger.when_released = self.door_open
        self.btnDriver.when_released = self.door_open
        self.btnPassenger.when_pressed = self.door_closed
        self.btnDriver.when_pressed = self.door_closed

    def __init__(self):
        logger.info("Security::init()")
        #self.setup_door_events() # doors have reverse polarity switches. this drains the battery. going to have to find another way to do this
        
    def start(self):
        logger.info("Listening for door events...")
        pause()
