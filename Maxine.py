#!/usr/bin/python3

from lib import Security
from lib import Sounds
from lib import MaxOBD
import threading, time, logging
from subprocess import call

# pip3 install obd
from obd import commands as obd_values

formatter = logging.Formatter('[%(asctime)s] %(name)-12s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
hdlr = logging.FileHandler('/dev/shm/maxine.log')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 

class Maxine(object):
    # main class for the AI 'brain'.

    def __init__(self):
        logger.info("Maxine::init()")
        #self.security = Security.Security()
        #self.sounds = Sounds.Sounds()
        self.obd = MaxOBD.MaxOBD()
        #self.running = True # TODO: toggle based on gpio switch

    def clean_data(self, data):
        if type(data) is str:
            return data
        else:
            return str(data.value)

    def start(self):
        logger.info("Maxine::start()")
        #tSecurity = threading.Thread(target=self.security.start)
        tOBD = threading.Thread(target=self.obd.start)
        #tSounds = threading.Thread(target=self.sounds.start_engine)
        
        #tSecurity.start()
        tOBD.start()
        #time.sleep(.2) #prevent logging from mixing
        #tSounds.start()

        #tSecurity.join()
        #tSounds.join()

m = Maxine()
m.start()
