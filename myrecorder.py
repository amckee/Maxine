#!/usr/bin/env python2

# this codebase has working functionalities similar to what is needed
# to be implemented into Maxine, so it's here for reference

from lib import obd_io
import serial
import platform
from lib import obd_sensors
import time
import getpass
import threading
import os
from lib.obd_utils import scanSerial
from datetime import datetime

class OBD_Recorder():
    def __init__(self, path, log_items):
        self.tonevalue = 0
        self.port = None
        self.sensorlist = []
        localtime = time.localtime(time.time())
        filename = "/dev/shm/jeep_obd.log"
        self.log_file = open(filename, "w", 128)
        ## i do not want headers
        #self.log_file.write("Time,RPM,MPH,Throttle,Load,Fuel Status\n");

        for item in log_items:
            self.add_log_item(item)

        self.gear_ratios = [34/13, 39/21, 36/23, 27/20, 26/21, 25/22]
        print("done initting")


    def connect(self):
        print("connect()")
        portnames = scanSerial()
        print(portnames)
        for port in portnames:
            self.port = obd_io.OBDPort(port, None, 2, 2)
            if(self.port.State == 0):
                self.port.close()
                self.port = None
            else:
                break

        if(self.port):
            print("Connected to "+self.port.port.name)
            
    def is_connected(self):
        return self.port
        
    def add_log_item(self, item):
        for index, e in enumerate(obd_sensors.SENSORS):
            if(item == e.shortname):
                self.sensorlist.append(index)
                print("Logging item: "+e.name)
                break
            
    def playtone(self):
        print("playtone: %s" % self.tonevalue)
        while True:
          if self.tonevalue == 0:
              print("cannot play tone of zero value")
              time.sleep(1)
          else:
              if type(self.tonevalue) is str:
                  print("skipping play; string received: %s" % self.tonevalue)
                  time.sleep(0.5)
              else:
                  freq = self.tonevalue + 30
                  print("Playing tone: {0:0.2f} Hz".format(freq))
                  os.system("echo '%s 0;' | pdsend 6500" % freq)     
          #time.sleep(0.2)
   

    def record_data(self):
        print("record_data")

        tSound = threading.Thread(target=self.playtone, args=())
        tSound.daemon = True
        tSound.start()
 
        while 1:
            if( self.port is None):
                print("self.port is None")
                time.sleep(.5)
                continue
            print("main while loop")
            localtime = datetime.now()
            current_time = str(localtime.hour)+":"+str(localtime.minute)+":"+str(localtime.second)+"."+str(localtime.microsecond)
            log_string = current_time
            results = {}
            #print(self.sensorlist)
            ## [12, 13, 17, 4, 3]
            for index in self.sensorlist:
                (name, value, unit) = self.port.sensor(index)
                print("Sensor:\t[index] %d\n\t[name] %s\n\t[value] %s\n\t[unit] %s" % (index, name, value, unit))
                log_string = log_string + ","+str(value)
                results[obd_sensors.SENSORS[index].shortname] = value;
                if index == 17:
                   if type(value) is not str:
                      self.tonevalue = value * 2

            #gear = self.calculate_gear(results["rpm"], results["speed"])
            #log_string = log_string #+ "," + str(gear)
            self.log_file.write(log_string+"\n")
            print("log written")
        
username = getpass.getuser()  
logitems = ["rpm", "speed", "throttle_pos", "load", "fuel_status"]
o = OBD_Recorder('/home/'+username+'/bin/pyobd/log/', logitems)
o.connect()

if not o.is_connected():
    print("Not connected")

o.record_data()
