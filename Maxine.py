from lib import Security
from lib import Sounds
from lib import Logger
from lib import MaxOBD
import threading, time
from subprocess import call

# pip3 install obd
from obd import commands as obd_values

class Maxine(object):
    # main class for the AI 'brain'.
    # this manages all subclasses, and distributes
    # input data (mainly from obd) to subsystems
    
    def __init__(self):
        self.logger = Logger.Logger(self)
        self.security = Security.Security()
        self.sounds = Sounds.Sounds()
        self.obd = MaxOBD.MaxOBD()
        self.running = True # TODO: toggle based on gpio switch
        self.logger.log("Main init complete")

    def obd_loop(self):
        longnaps = 0
        while self.running:
            dat = self.obd.get_data(obd_values.THROTTLE_POS)
            self.logger.log("TPS: %s" % dat.value)
            if dat.value is None:
                self.logger.log("Got 'none' data. Taking extra nap...")
                longnaps = longnaps + 1
                time.sleep(9)
                if longnaps > 12:
                    # we've been offline for 2m now, time to force restart bluetooth itself...
                    self.logger.log("Restarting bluetooth (yes, it's an ugly hack)")
                    # okay, look. i've been having kernel dumps occur stemming from the
                    # bluetooth stack that cause the need for a reboot, and failing
                    # anything else, a restart of bluetooth could mean reconnecting
                    # with the obd device, so for now... why not?
                    call(["sudo", "service", "bluetooth", "restart"])
            time.sleep(1)

    def start(self):
        tSecurity = threading.Thread(target=self.security.start)
        tOBD = threading.Thread(target=self.obd_loop)
        #tSounds = threading.Thread(target=self.sounds.start_engine)
        
        tSecurity.start()
        tOBD.start()
        #time.sleep(.2) #prevent logging from mixing
        #tSounds.start()

        #tSecurity.join()
        #tSounds.join()

        self.logger.log("Main start complete")

m = Maxine()
m.start()
