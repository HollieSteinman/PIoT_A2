import os, requests, json, string, bluetooth

class Notification():
     nearby_devices = bluetooth.discover_devices(lookup_names = True)

     def discoverDevices(self):
          print("found %d device(s)" % len(self.nearby_devices))

          for name, addr in self.nearby_devices:
               print (" %s - %s" % (addr, name))


     #    named raspberry pi and Matthies iPhone for testing 
     #    replace name with master pi name later

     def masterPiFound(self):
          found = False

          for addr, name in self.nearby_devices:
               if(name == 'Matthies\’s iPhone' or 'raspberrypi'):
                    found = True
                    break

          return found

     #    print unlock notification

     def carUnlockedNotification(self):
          if(self.masterPiFound()):
               print("Car Unlocked")

     #    print locked notification
     
     def carLockedNotification(self):
          if(self.masterPiFound()):
               print("Car Locked")

# TESTING AREA

notification = Notification()

notification.discoverDevices()
notification.carUnlockedNotification()
notification.carLockedNotification()