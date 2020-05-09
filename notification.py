import os, requests, json, string, bluetooth

print ("Searching for devices...")

nearby_devices = bluetooth.discover_devices(lookup_names = True)

print ("found %d devices" % len(nearby_devices))

for name, addr in nearby_devices:
     print (" %s - %s" % (addr, name))