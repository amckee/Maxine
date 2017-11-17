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

    def __init__(self):
        logger.info( "init()" )
        #self.running = True # TODO: toggle based on gpio switch

    def threadtest(self):
        logger.info("threadtest()")

    def new_rpm(self, rpm):
        logger.info("New RPM: %s" % rpm.value.magnitude)

    def clean_data(self, data):
        if type(data) is str:
            return data
        else:
            return str( data.value )

    def start(self):
        logger.info("start()")
	## for debugging through prototype, run it unthreaded
        #self.obd = MaxOBD.MaxOBD()
        #self.obd.start()

        # below here is kind of what i had in mind when i wrote it.
        # it's been awhile, so things change. keeping it all
        # here for future reference for now.
        
        # create objects
        self.obd = MaxOBD.MaxOBD()
        self.fan = FanControl.FanControl()
        #self.security = Security.Security()
        #self.sounds = Sounds.Sounds()

        # create threads
        tFan = threading.Thread( target=self.fan.start )
        tOBD = threading.Thread( target=self.obd.start )
        #tSecurity = threading.Thread(target=self.security.start)
        #tSounds = threading.Thread(target=self.sounds.start_engine)

        # start threads
        tFan.start()
        tOBD.start()
        #tSecurity.start()
        #tSounds.start()

        #tSecurity.join()
        #tSounds.join()

m = Maxine()
m.start()
logger.info("Maxine completed.")
