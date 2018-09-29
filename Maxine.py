#!/usr/bin/python3

from lib import Security
from lib import Sounds
from lib import MaxOBD
from lib import FanControl
import threading, time, logging
from subprocess import call

# pip3 install obd
from obd import commands as obd_values
#from logging_tree import printout

class Maxine(object):
    # main class for the AI 'brain'.

    def __init__( self ):
        logger = logging.getLogger( "maxine" )
        formatter = logging.Formatter( '[%(asctime)s] %(name)-12s %(message)s' )
        fhandler = logging.FileHandler( '/dev/shm/maxine.log', mode='w' )
        fhandler.setFormatter( formatter )
        shandler = logging.StreamHandler()
        shandler.setFormatter( formatter )

        logger.setLevel(logging.INFO)
        logger.addHandler( fhandler )
        logger.addHandler( shandler )

    def start(self):
        # create objects
        self.obd = MaxOBD.MaxOBD()
        self.fan = FanControl.FanControl()
        #self.sounds = Sounds.Sounds()
        #self.security = Security.Security()

        # create threads
        tFan = threading.Thread( target=self.fan.start )
        tOBD = threading.Thread( target=self.obd.start )
        #tSounds = threading.Thread(target=self.sounds.start_engine)
        #tSecurity = threading.Thread(target=self.security.start)

        # start threads
        tFan.start()
        tOBD.start()
        #tSecurity.start()
        #tSounds.start()

        # join threads to single pool
        #tFan.join()
        #tOBD.join()
        #tSecurity.join()
        #tSounds.join()
        #printout() ## show logger tree


m = Maxine()
m.start()
print("Maxine exited")
