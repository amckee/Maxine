from lib import Security
from lib import Sounds
from lib import MaxOBD
import threading, time, logging
from subprocess import call

# pip3 install obd
from obd import commands as obd_values

logging.basicConfig( format='[%(asctime)s] %(message)s' )
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
#logging.basicConfig( filename='/dev/shm/jeepobd.log' )

class Maxine(object):
    # main class for the AI 'brain'.

    def __init__(self):
        logger.info("Maxine::init()")
        self.security = Security.Security()
        self.sounds = Sounds.Sounds()
        self.obd = MaxOBD.MaxOBD()
        self.running = True # TODO: toggle based on gpio switch

    def clean_data(self, data):
        if type(data) is str:
            return data
        else:
            return str(data.value)

    def obd_loop(self):
        logger.info("Maxine::obd_loop()")
        naptime = 10
        longnaps = 0
        logdata = ""
        while self.running:
            self.obd = MaxOBD.MaxOBD()
                        
            if self.obd.con.is_connected():
                self.obd.start()
            else:
                logger.warning("Connection to OBD failed. Sleeping, and trying again.")
                self.obd.stop()
                time.sleep(naptime)

    def start(self):
        logger.info("Maxine::start()")
        tSecurity = threading.Thread(target=self.security.start)
        tOBD = threading.Thread(target=self.obd.start)
        #tSounds = threading.Thread(target=self.sounds.start_engine)
        
        tSecurity.start()
        tOBD.start()
        #time.sleep(.2) #prevent logging from mixing
        #tSounds.start()

        #tSecurity.join()
        #tSounds.join()

m = Maxine()
m.start()
