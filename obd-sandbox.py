import obd

logfile = "/dev/shm/jeep_obd.log"
con = obd.OBD()

def get_data(cmd):
    return con.query(cmd)

print("Connection Details:")
print("Connection: %s" % con.is_connected())
print("Status: %s" % con.status())
print("Connection Status: %s" % get_data(obd.commands.STATUS))
print()

print("Basic Sensors:")
print("TPS-A: %s" % get_data(obd.commands.THROTTLE_POS))
print("TPS-B: %s" % get_data(obd.commands.THROTTLE_POS_B))
print("TPS-C: %s" % get_data(obd.commands.THROTTLE_POS_C))
print("Coolant Temp: %s" % get_data(obd.commands.COOLANT_TEMP))
print("RPM: %s" % get_data(obd.commands.RPM))

print("Load: %s" % con.query(obd.commands.ABSOLUTE_LOAD))

f = open( logfile, 'w' )
f.write( "0,0,0,0,0,0\n" )
f.close()
