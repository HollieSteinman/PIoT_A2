import faceRecognise
import faceData
import faceTrain
import socket
from passlib.hash import sha256_crypt

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 9350
UNIC_FORMAT = "utf-8"
BYTES = 1024
FALSE = '0'
TRUE = '1'

class AgentPi():

    locked = True

    def showLoginMenu(self):
        print("1. Sign in with credentials")
        print("2. Use face recognition")

        i = input()
        if i == '1':
            s.connect((socket.gethostname(), PORT))
            # Get a username, keep trying until a valid username is entered
            valid_username = FALSE
            while valid_username == FALSE:
                username = input("Username: ")
                # Send the username entered to the server
                s.send(bytes(username, UNIC_FORMAT))
                valid_username = s.recv(BYTES).decode()
                if valid_username == FALSE:
                    print("Username \'{}\' does not exist in system, please try" 
                            " again".format(username))

            correct_password = FALSE
            while correct_password == FALSE:
                password = input("Password: ")
                # Send the password entered to the server
                s.send(bytes(password, UNIC_FORMAT))
                correct_password = s.recv(BYTES).decode()
                if correct_password == TRUE:
                    print("Login successful!")
                    self.unlock()
                    self.showMenu()

                else:
                    print("Password incorrect, please try again")

        elif i == '2':
            print("Recognising...")
            if faceRecognise.run():
                print("Unlocked")
                self.unlock()
                self.showMenu()
            else:
                print("Face not recognised.")
                self.showLoginMenu()
        else:
            print("Incorrect input")
            self.showLoginMenu()

    def unlock(self):
        self.locked = False

    def lock(self):
        self.locked = True

    def showMenu(self):
        lock_status = ""
        if self.locked:
            lock_status = "locked"
        else:
            lock_status = "unlocked"
        print("Car is: " + lock_status)
        print("1. Lock/Unlock")
        print("2. Return")
        print("3. Set up face recognition")

        i = input()
        if i == '1':
            if self.locked:
                self.unlock()
                print("Car unlocked")
                self.showMenu()
            else:
                self.lock()
                print("Car locked")
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