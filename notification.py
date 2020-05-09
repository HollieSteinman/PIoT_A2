import os, requests, json, string, bluetooth

nearby_devices = bluetooth.discover_devices(lookup_names = True)

def discoverDevices():
     print("found %d device(s)" % len(nearby_devices))

     for name, addr in nearby_devices:
          print (" %s - %s" % (addr, name))


# named raspberry pi for testing 
# replace name with master pi

def masterPiFound():
     found = False

     for addr, name in nearby_devices:
          if(name == 'Matthies\’s iPhone' or 'raspberrypi'):
               found = True

     return found

def sendNotification():
     if(masterPiFound()):
          print("Car Unlocked")


sendNotification()