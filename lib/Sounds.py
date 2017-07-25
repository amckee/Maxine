#import getpass
#import serial, platform
#from datetime import datetime
#import numpy, pyaudio, math
from lib import ToneGenerator
import logging, time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Sounds(object):
    def __init__(self):
        logger.info("Sounds::init()")
        #TODO: reimplement mysounds.py/obdrecorder.py
        #TODO: import a library of available sounds

        # these could be subdirs containing available sounds
        # (i'm thinking pick one randomly from the given group
        # to keep things interesting, and/or it'll make
        # organizing sound themes easier)
        self.sounds = ['startup','stuck','crash','flip','bump']
        logger.info("TODO: init sounds")

    def play(self, event_name=''):
        # lots to do here, but let's just
        # start by playing a sample wav directly.
        # then we get fancy with it.
        logger.info("play %s" % event_name)
        
    def start_engine(self):
        #time.sleep(10) # give radio time to be 'on'
        self.play(event_name='startup')
        logger.info("TODO: start pd")
