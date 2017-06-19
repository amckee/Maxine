from lib import Security
from lib import Sounds
from lib import OBD
from lib import Logger
import threading
import time

class Maxine(object):
    # main class for the AI 'brain'.
    # this manages all subclasses, and distributes
    # input data (mainly from obd) to subsystems
    
    def __init__(self):
        self.logger = Logger.Logger(self)
        self.security = Security.Security()
        self.sounds = Sounds.Sounds()
        self.obd = OBD.OBD()
        self.logger.log("Main init complete")

    def start(self):
        tSecurity = threading.Thread(target=self.security.start)
        tSounds = threading.Thread(target=self.sounds.start_engine)
        
        tSecurity.start()
        time.sleep(.2) #prevent logging from mixing
        tSounds.start()

        tSecurity.join()
        tSounds.join()
        self.obd.start()

        self.logger.log("Main start complete")

m = Maxine()
m.start()
