from lib import Security
from lib import Sounds
from lib import OBD

class Maxine(object):
    security = Security.Security()
    sounds = Sounds.Sounds()
    obd = OBD.OBD() #TODO: fix hardcoded bluetooth adapter address
    
    def __init__(self):
        self.security.start()
        self.sounds.play('startup')

    def start(self):
        self.sounds.start_engine()
        self.obd.start()

m = Maxine()
m.start()
