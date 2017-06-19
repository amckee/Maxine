import obd

con = obd.OBD() #auto connects to rfcomm0

#res = con.query(obd.commands.ACCELERATOR_POS_D) # get details of specified sensor
#print(res.value)

print(con.query(obd.commands.COOLANT_TEMP).value.to('degF'))
print(con.query(obd.commands.ENGINE_LOAD).value)
print(con.query(obd.commands.RPM).value)
print(con.query(obd.commands.SPEED).value.to('mph'))
print(con.query(obd.commands.THROTTLE_POS).value)

