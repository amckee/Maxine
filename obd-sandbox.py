import obd

class MaxOBD(object):

    def __init__(self):
        self.con = obd.OBD() #auto connects to rfcomm0

    def get_data(self, cmd):
        return self.con.query(cmd)


o = MaxOBD()

print("Connection Details:")
print("Connection: %s" % o.con.is_connected())
print("Status: %s" % o.con.status())
print("Con Status: %s" % o.get_data(obd.commands.STATUS))
print()

print("Voltages:")
print("Module Voltage: %s" % o.get_data(obd.commands.CONTROL_MODULE_VOLTAGE))
print("ELM Voltage: %s" % o.get_data(obd.commands.ELM_VOLTAGE))

print("Basic Sensors:")
print("TPS-A: %s" % o.get_data(obd.commands.THROTTLE_POS))
print("TPS-B: %s" % o.get_data(obd.commands.THROTTLE_POS_B))
print("TPS-C: %s" % o.get_data(obd.commands.THROTTLE_POS_C))
print("Coolant Temp: %s" % o.get_data(obd.commands.COOLANT_TEMP))
