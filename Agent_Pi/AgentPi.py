import faceRecognise
import faceData
import faceTrain
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 9350
UNIC_FORMAT = "utf-8"
BYTES = 1024
FALSE = '0'
TRUE = '1'


class AgentPi():
    """AgentPi class allows for user interaction with the car: unlocking with face or login details, locking and returning as well as adding a new face to recognise.

    :param use(str): The username for the user successfully logged in.
    :param locked(bool): The locked/unlocked status of the car the Agent Pi is currently attached to.
    """

    user = ""
    locked = True

    def showLoginMenu(self):
        """Display the menu to the user so that they may choose a login option and enter their details or provide a face to recognise
        """

        print("1. Unlock with credentials")
        print("2. Use face recognition")

        i = input()
        # Log in with username and password
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
                    print("Username \'{}\' does not exist in system, please"
                          " try again".format(username))

            correct_password = FALSE
            while correct_password == FALSE:
                password = input("Password: ")
                # Send the password entered to the server
                s.send(bytes(password, UNIC_FORMAT))
                correct_password = s.recv(BYTES).decode()
                if correct_password == TRUE:
                    self.user = username
                    print("Login successful! Welcome {}".format(self.user))
                    self.showMenu()

                else:
                    print("Password incorrect, please try again")
        # Log in using facial recognition
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
        """Unlock the car the Agent Pi is currently attached to
        """
        self.locked = False

    def lock(self):
        """Lock the car the the Agent Pu is currently attached to
        """
        self.locked = True

    def returnCar(self):
        """ Return the car, send a message to the Master Pi notifying it that the
        """
        print("Returned")
        s.send(bytes("{} returning car".format(self.user), UNIC_FORMAT))
        msg = s.recv(BYTES).decode()
        print(msg)
        self.showMenu()

    def showMenu(self):
        """The menu displayed to the user following a successful login
        """
        
        lock_status = ""
        if self.locked:
            lock_status = "locked"
        else:
            lock_status = "unlocked"
        print("Car is: " + lock_status)
        print("1. Unlock")
        print("2. Return")
        print("3. Set up face recognition")

        i = input()
        if i == '1':
            if self.locked:
                self.unlock()
                print("Car unlocked")
                self.showMenu()
            else:
                print("Car already unlocked")
                self.showMenu()
        elif i == '2':
            if self.locked == False:
                self.lock()
                self.returnCar()
            else:
                print("Car already locked")
                self.showMenu()
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
