import serial, time
from lib import obd_io

obdev = obd_io.OBDPort("/dev/rfcomm0",None,2,2)

