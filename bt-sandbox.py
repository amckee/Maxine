import bluetooth

obd_mac = "00:1D:A5:00:01:EB"

print("scanning...")
nd = bluetooth.discover_devices()
print("found %d devices" % len(nd))

aand = bluetooth.lookup_name(obd_mac)

for dev in nd:
    print( dev )

print( aand )
