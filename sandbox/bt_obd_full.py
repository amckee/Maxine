#!/usr/bin/python3

from obd import OBDStatus
from bluetooth import *
import obd, subprocess, bluetooth

obdaddr = "00:1D:A5:00:01:EB"

def newinfo( dat ):
    print( dat )

#bt = BluetoothSocket( RFCOMM )
#bt.connect( (obdaddr, 1) )

## hcitool notes
## 	con 	Display active connections
## 

subprocess.call(['sudo', 'hcitool', 'cc', obdaddr])
subprocess.call(['sudo', 'rfcomm', 'bind', '0', obdaddr])

myobd = obd.Async()
myobd.watch(obd.commands.COOLANT_TEMP, callback=newinfo)
myobd.start()
