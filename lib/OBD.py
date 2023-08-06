from lib import obd_io, obd_sensors, obd_utils
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
    bt_devices['obd'] = "00:1D:A5:00:01:EB" # obd devicegi

    def __init__(self):
        self.tonevalue = 0
        self.port = None
        self.sensorlist = []
        self.logger = Logger.Logger(self)
        self.btdevice = self.find_bluetooth_device()
        if self.btdevice == None:
            self.logger.log("TODO: %s not found" % self.bt_devices['usb'])
        else:
            self.logger.log("btdevice: %s " % self.btdevice)

    def connect(self):
        self.port = obd_io.OBDPort(self.btdevice, None, 2, 2)
        if(self.port.State == 0):
            self.port.close()
            self.port = None

    def find_bluetooth_device(self, adapter_id=None):
        """scan for available ports. return a list of serial names"""
        available = []
        # Enable Bluetooh connection
        for i in range(5):
          try:
            s = serial.Serial("/dev/rfcomm"+str(i))
            available.append( (str(s.port)))
            s.close()   # explicit close 'cause of delayed GC in java
          except serial.SerialException:
            pass
        return available

    def start(self):
        if self.btdevice is None:
            self.logger.log("Do not have OBD")
            return
        self.logger.log("Got OBD serial device at: %s" % self.btdevice)
