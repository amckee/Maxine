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

    def clean_data(self, data):
        if type(data) is str:
            return data
        else:
            return str(data.value)

    def obd_loop(self):
        longnaps = 0
        logdata = ""
        while self.running:
            try:
                # TPS for synthetic engine fx
                dat = self.obd.get_data(obd_values.THROTTLE_POS)
                print("TPS: %s" % str(dat))

                # Other data values for Conky
                dat = self.obd.get_data(obd_values.COOLANT_TEMP).value.to('degF')
                logdata = self.clean_data(dat) + ","
                dat = self.obd.get_data(obd_values.RPM).value
                logdata = logdata + self.clean_data(dat) + ","
                dat = self.obd.get_data(obd_values.SPEED).value.to('mph')
                logdata = logdata + self.clean_data(dat) + ","
                dat = self.obd.get_data(obd_values.ENGINE_LOAD)
                logdata = logdata + self.clean_data(dat.value) + ","

                # actually write the log data to a file
                # TODO: see line above
                print(logdata)
                time.sleep(1)
            except:
                # for now we are assuming this means the engine is off, so sleep, reset, try again
                self.logger.log("Having issues, OBD probably off. Taking long nap.")
                time.sleep(10)
                self.obd = MaxOBD.MaxOBD()

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
