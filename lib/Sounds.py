#import time, getpass
#import serial, platform
#from datetime import datetime
#import numpy, pyaudio, math
from lib import ToneGenerator

class Sounds(object):
    def __init__(self):
        #TODO: reimplement mysounds.py/obdrecorder.py
        #TODO: import a library of available sounds
        self.sounds = ['startup','stuck','crash','flip'] # these could be subdirs containing available sounds (i'm thinking pick one randomly to keep things interesting, and/or it'll make organizing sound themes easier)
        print("TODO: init sounds")

    def play(self, event_name='start'):
        # lots to do here, but let's just
        # start by playing a sample wav directly.
        # then we get fancy with it.
        print("TODO: play a sound")
        
    def start_engine(self):
        print("TODO: start pd")
