from lib import Security
from lib import Sounds
from lib import Logger
from lib import MaxOBD
#from lib import Notifications
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
        self.logger.log_to_file('/dev/shm/jeep_obd.log')
        self.security = Security.Security()
        self.sounds = Sounds.Sounds()
        self.running = True # TODO: toggle based on gpio switch to ignition (radio?) wire
        self.logger.log("Main init complete")

    def _nap(self, naptime=10):
        self.logger.log("Taking %ss nap." % naptime)
        time.sleep(naptime)

    def clean_data(self, data):
        if type(data) is str:
            return data
        else:
            return str(data.value)

    def obd_loop(self):
        self.obd = MaxOBD.MaxOBD()
        longnaps = 0
        logdata = ""
        while self.running:
            try:
                # throttle position sensor for synthetic engine fx
                dat = self.obd.get_data(obd_values.THROTTLE_POS)

                # Other data values for Conky
                dat = self.obd.get_data(obd_values.COOLANT_TEMP).value.to('degF')
                logdata = self.clean_data(dat) + ","
                dat = self.obd.get_data(obd_values.RPM).value
                logdata = logdata + self.clean_data(dat) + ","
                dat = self.obd.get_data(obd_values.SPEED).value.to('mph')
                logdata = logdata + self.clean_data(dat) + ","
                dat = self.obd.get_data(obd_values.ENGINE_LOAD)
                logdata = logdata + self.clean_data(dat.value) + ","

                # TODO: warnings/engine error code notifications

                # actually write the log data to a file
                # TODO: see line above
                self.logger.log(logdata)
                time.sleep(1)
            except:
                # if getting the first data request failed, usually mains nothing will work                
                # for now i am assuming this means the engine is off.
                # as such, here we sleep, reset obd, try again
                self.logger.log("Having OBD issues, which means the vehicle is probably off.")
                # TODO: output error details
                self.obd.reset()
                self._nap(30) # TODO: use power signal as switch for vehicle 'on/off'

    def start(self):
        tOBD = threading.Thread(target=self.obd_loop)
        tSecurity = threading.Thread(target=self.security.start)
        #tSounds = threading.Thread(target=self.sounds.)
        
        tSecurity.start()
        tOBD.start()
        #time.sleep(.2) #prevent logging from mixing
        #tSounds.start()

        #tSecurity.join()
        #tSounds.join()

        #self.logger.log("Main start complete")

m = Maxine()
m.start()
