from bluezero import adapter

btdevs = adapter.list_adapters()
btdev = adapter.Adapter(btdevs[0]) # generally this is the built-in bluetooth device
print( type(btdevs) )
print( type(adapter.Adapter(btdevs[0]).address) )

for btd in btdevs:
    ad = adapter.Adapter(btd)
    print("Adapter:")
    print(ad.address)
    print(ad.name)
