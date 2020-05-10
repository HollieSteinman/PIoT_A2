import faceRecognise
import faceData
import faceTrain

class AgentPi():

    locked = True

    def showLoginMenu(self):
        print("1. Sign in with credentials")
        print("2. Use face recognition")

        i = input()
        if i == '1':
            print("Not implemented")
        elif i == '2':
            print("Recognising...")
            if faceRecognise.run():
                print("Unlocked")
                self.unlock()
                self.showMenu()
            else:
                print("Face not recognised.")
                self.showMenu()
        else:
            print("Incorrect input")
            self.showLoginMenu()

    def unlock(self):
        self.locked = False

    def lock(self):
        self.locked = True

    def showMenu(self):
        print("Car is: " + str(self.locked))
        print("1. Lock/Unlock")
        print("2. Return")
        print("3. Set up face recognition")

        i = input()
        if i == '1':
            if self.locked:
                self.unlock()
                print("Unlocked")
                self.showMenu()
            else:
                self.lock()
                print("Locked")
                self.showMenu()
        elif i == '2':
            print("Not implemented")
        elif i == '3':
            print("Scanning face...")
            faceData.gatherData()
            print("Saving data...")
            faceTrain.train()
            print("All done!")
            self.showMenu()
        else:
            print("Incorrect input")
            self.showMenu()



aPi = AgentPi()
aPi.showLoginMenu()