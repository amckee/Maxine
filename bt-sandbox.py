from bluetooth import *
import bluetooth

obd_name = "FIXD"
#obd_mac = "00:1D:A5:00:01:EB"
obd_addr = None

print("scanning...")
neardevs = bluetooth.discover_devices()

print("found %d devices" % len(neardevs))

for dev in neardevs:
    if obd_name == bluetooth.lookup_name(dev):
        obd_addr = dev
        break

if obd_addr is not None:
    print("found %s at %s" % (obd_name, obd_addr))
    print("checking connection status of %s" % obd_name)
    sock = BluetoothSocket( RFCOMM )
    sock.connect((obd_addr,1))
    # to disconnect, sock.close()
    print("connected")
else:
    print("could not find %s" % obd_name)
