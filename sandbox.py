#!/usr/bin/python3

from bluetooth import *
import bluetooth

obd_name = "FIXD"
#obd_mac = "88:1B:99:1D:1F:5E"
obd_addr = None

print( "Scanning..." )
neardevs = bluetooth.discover_devices()

print( "Found %d devices" % len(neardevs) )

for dev in neardevs:
    if obd_name == bluetooth.lookup_name( dev ):
        obd_addr = dev
        break

if obd_addr is not None:
    print( "Found %s at %s" % (obd_name, obd_addr) )
    print( "Checking connection status of %s" % obd_name )
    sock = BluetoothSocket( RFCOMM )
    sock.connect( (obd_addr,1) )
    # to disconnect, sock.close()
    print( "Connected" )

    #sock.close()
else:
    print( "Could not find %s" % obd_name )

