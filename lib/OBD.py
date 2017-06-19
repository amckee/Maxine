try:
    from lib import obd_io, obd_sensors, obd_utils
except ImportError:
    import obd_io, obd_sensors, obd_utils
    
import serial, platform, time
import numpy,pyaudio,math
from datetime import datetime
from bluezero import adapter
from lib import Logger

class OBD(object):
    # TODO: setup a scanner/list of devs for dynamic setup
    ## these IDs are for me; adjust yours accordingly
    bt_devices = {}
    bt_devices['rpi'] = "B8:27:EB:24:E3:49" # rpi3 built in bt dev addr
    bt_devices['usb'] = "5C:F3:70:69:EF:9F" # usb bluetooth adapter addr
    bt_devices['obd'] = "00:1D:A5:00:01:EB" # obd device

    def __init__(self):
        self.logger = Logger.Logger(self)
        self.btdevice = self.find_bluetooth_device(self.bt_devices['rpi'])
        if self.btdevice == False:
            self.logger.log("TODO: proper handling. for now, 'error: no adapter id given'")
        self.logger.log("TODO: init obd")

    def find_bluetooth_device(self, adapter_id=None):
        if adapter_id is None:
            self.logger.log("FAIL: find_bluetooth_device")
            return False
        #iterate through all located bt adapters, set main
        #bt dev when we find by matching id
        btdevs = adapter.list_adapters()
        for btd in btdevs:
            a = adapter.Adapter(btd)
            if a.address == self.bt_devices['rpi']:
                self.btdev = a
                #print("DEBUG: got requested device: %s @ %s" % (self.btdev.name, self.btdev.address))
                break

    def start(self):
        if self.btdevice is None:
            self.logger.log("Do not have OBD")
            return
        self.logger.log("Got OBD: %s @ %s" % (self.btdevice.name, self.btddevice.address))
        self.logger.log("Status: %s" % self.btdevice.status)
        self.logger.log("TODO: connect to obd device")
