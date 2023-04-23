#!/usr/bin/python3
import obd

logfile = "sandbox.log"

print("Opening connection...")
con = obd.OBD()

def get_data(cmd):
    return con.query(cmd)

print("Connection: %s" % con.is_connected())
print("Status: %s" % con.status())
print("OBD Status: %s" % get_data(obd.commands.STATUS))
print()

print("Gathering data...")

tps = get_data(obd.commands.THROTTLE_POS)
coolant_temp = get_data(obd.commands.COOLANT_TEMP)
rpm = get_data(obd.commands.RPM)

print("\nBasic Sensors:")
print("TPS: %s" % tps)
print("Coolant Temp: %s" % coolant_temp)
print("RPM: %s" % rpm)

f = open( logfile, 'w' )
#f.write( "0,0,0,0,0,0\n" )
f.write( "%s,%s,%s,%s,%s,%s" % (tps,coolant_temp,rpm,'0','0','0') )
f.close()
