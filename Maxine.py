from lib import Security
from lib import Sounds
from lib import OBD

class Maxine(object):
    security = Security.Security()
    sounds = Sounds.Sounds()
    def __init__(self):
        self.security.start() # security is important, so start this asap
        self.sounds.play('startup')

    def start(self):
        pass

m = Maxine()
m.start()
