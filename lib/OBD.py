try:
    from lib import obd_io, obd_sensors, obd_utils
except ImportError:
    import obd_io, obd_sensors, obd_utils
    
import serial, platform, time
import numpy,pyaudio,math
from datetime import datetime
from bluezero import adapter

class OBD(object):
    mainadapter = "B8:27:EB:24:E3:49" # rpi3 built in bt dev addr

    def __init__(self):
        self.btdevice = self.find_bluetooth_device(self.mainadapter)
        if self.btdevice == False:
            print("TODO: proper handling. for now, 'error: no adapter id given'")
        print("TODO: init obd")

    def find_bluetooth_device(self, adapter_id=None):
        if adapter_id is None:
            print("FAIL: OBD.py->OBD->find_bluetooth_device")
            return False
        #iterate through all located bt adapters, set main
        #bt dev when we find by matching id
        btdevs = adapter.list_adapters()
        for btd in btdevs:
            a = adapter.Adapter(btd)
            if a.address == self.mainadapter:
                self.btdev = a
                #print("DEBUG: got requested device: %s @ %s" % (self.btdev.name, self.btdev.address))
                break

    def start(self):
        print("Got OBD: %s @ %s" % (self.btdevice.name, self.btddevice.address))
        print("Status: %s" % self.btdevice.status)
        print("TODO: connect to obd device")
