import obd

logfile = "/dev/shm/jeep_obd.log"

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
speed = get_data(obd.commands.SPEED)

logstring = ""

print("\nBasic Sensors:")
if not tps.is_null():
    print("TPS: %s" % tps)
    logstring = str(tps.value.magnitude)
if not coolant_temp.is_null():
    print("Coolant Temp: %s" % coolant_temp.value.to('degF'))
    logstring = logstring + "," + str(coolant_temp.value.to('degF').magnitude)
if not rpm.is_null():
    print("RPM: %s" % rpm)
    logstring = logstring + "," + str(rpm.value.magnitude)
if not speed.is_null():
    print("Speed: %s" % speed.value.to('mph'))
    logstring = logstring + "," + str(speed.value.to('mph').magnitude)

f = open( logfile, 'w' )
f.write( logstring + "\n" )
f.close()
