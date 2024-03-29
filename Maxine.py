#!/usr/bin/python3

#from lib import Security
from lib import MaxOBD
#from lib import Sounds
from lib import FanControl
import threading, time, logging
from subprocess import call

# pip3 install obd
from obd import commands as obd_values
#from logging_tree import printout

class Maxine(object):
    # main class for the AI 'brain', mainly a thread handler
    logger = logging.getLogger( "maxine" )

    def __init__( self ):
        formatter = logging.Formatter( '[%(asctime)s] %(name)-12s %(message)s' )
        fhandler = logging.FileHandler( '/dev/shm/maxine.log', mode='a' )
        fhandler.setFormatter( formatter )
        shandler = logging.StreamHandler()
        shandler.setFormatter( formatter )

        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler( fhandler )
        self.logger.addHandler( shandler )

    def start(self):
        self.obd = MaxOBD.MaxOBD()
        #self.fan = FanControl.FanControl()
        #self.sounds = Sounds.Sounds()
        #self.security = Security.Security()

        # create threads
        tOBD = threading.Thread( target=self.obd.start )
        #tFan = threading.Thread( target=self.fan.start )
        #tSounds = threading.Thread(target=self.sounds.start_engine)
        #tSecurity = threading.Thread(target=self.security.start)

        # start threads
        tOBD.start()
        #tFan.start()
        #tSecurity.start()
        #tSounds.start()

        # join threads to single pool
        tOBD.join()
        #tFan.join()
        #tSecurity.join()
        #tSounds.join()
        #printout() ## show logger tree

m = Maxine()
m.start()

print("Maxine stopped!")
