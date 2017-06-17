import bluetooth

print("scanning...")
nd = bluetooth.discover_devices()
print("found %d devices" % len(nd))
aand = bluetooth.lookup_name("00:1D:A5:00:01:EB")

for dev in nd:
    print( dev )

print( aand )
