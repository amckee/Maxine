from lib import Security
from lib import Sounds
from lib import OBD
from lib import Logger

class Maxine(object):
    # main class for the AI 'brain'.
    # this manages all subclasses, and distributes
    # input data (mainly from obd) to subsystems
    
    def logger(self, obj, msg=""):
        #TODO: log to external file
        if msg == "":
            return
        dt = datetime.datetime.now()
        print("[%s] %s : %s" % (dt.strftime("%Y.%m.%d %H:%M:%S"), str(obj), msg))
    
    def __init__(self):
        self.security = Security.Security()
        self.sounds = Sounds.Sounds()
        self.obd = OBD.OBD()

    def start(self):
        self.security.start()
        self.sounds.start_engine()
        self.obd.start()

m = Maxine()
m.start()
