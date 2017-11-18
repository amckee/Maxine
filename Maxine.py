#!/usr/bin/python3

from lib import Security
from lib import Sounds
from lib import MaxOBD
from lib import FanControl
import threading, time, logging
from subprocess import call

# pip3 install obd
from obd import commands as obd_values

formatter = logging.Formatter( '[%(asctime)s] %(name)-12s %(message)s' )
logging.getLogger().addHandler(logging.StreamHandler())
#logger = logging.getLogger(__name__)
logger = logging.getLogger("maxine")
logger.setLevel(logging.INFO)
hdlr = logging.FileHandler( '/dev/shm/maxine.log' )
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.info("\n")

class Maxine(object):
    # main class for the AI 'brain'.

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

        #tSecurity.join()
        #tSounds.join()

m = Maxine()
m.start()
#logger.info("Maxine completed.")
