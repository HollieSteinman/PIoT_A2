import socket
import mysql.connector
from passlib.hash import sha256_crypt
import requests
import time

QUEUE = 5
PORT = 9350
BYTES = 1024
UNIC_FORMAT = "utf-8"
FALSE = '0'
TRUE = '1'
QUERY_IDENTIFIER = ["LOGIN", "MAC", "ENGDETAILS"]


class CredCheck:

    def login(self, clientsocket, mycursor):
        while True:
            username = clientsocket.recv(BYTES).decode()
            if username:
                print("Recieved username: {}".format(username))
                query = '''SELECT username 
                            FROM user 
                            WHERE username = \"{}\"'''.format(username)
                mycursor.execute(query)
                result = mycursor.fetchall()
                if result:
                    clientsocket.send(bytes(TRUE, UNIC_FORMAT))
                    break
                else:
                    clientsocket.send(bytes(FALSE, UNIC_FORMAT))
            else:
                break

        while True:
            password = clientsocket.recv(BYTES).decode()
            if password:
                print("Recieved password: {}".format(password))
                query = '''SELECT password 
                            FROM user 
                            WHERE username = \"{}\"'''.format(username)
                mycursor.execute(query)
                result = mycursor.fetchall()
                if sha256_crypt.verify(password, result[0][0]):
                    clientsocket.send(bytes(TRUE, UNIC_FORMAT))
                    break
                else:
                    clientsocket.send(bytes(FALSE, UNIC_FORMAT))
            else:
                break

        while True:
            car_id = clientsocket.recv(BYTES).decode()
            if car_id:
                print("Recieved return message: car id to return is {} for the user {}".format(car_id, username))
                # TODO Michael to use API endpoint to set car for user's current
                # booking to available and booking to complete
                user = requests.get("http://127.0.0.1:5000/api/customer/username/{}".format(username)).json()
                booking = requests.get("http://127.0.0.1:5000/api/booking/car/{}/status/active".format(car_id)).json()
                if booking and booking["user_id"] == user["user_id"]:
                    requests.put("http://127.0.0.1:5000/api/booking/status/complete", data=booking)
                    clientsocket.send(bytes("Car returned successfuly", UNIC_FORMAT))
                else:
                    clientsocket.send(bytes("Return unsuccessful, please ensure you"
                                            " have an active booking", UNIC_FORMAT))
            else:
                break

    def mac(self, clientsocket, mycursor):
        while True:
            mac = clientsocket.recv(BYTES).decode()
            if mac:
                if mac == FALSE:
                    print("no more MAC")
                    break
                print("Recieved MAC: {}".format(mac))
                query = '''SELECT mac_address
                                FROM engineer_mac 
                                WHERE mac_address = \"{}\"'''.format(mac)
                mycursor.execute(query)
                result = mycursor.fetchall()
                if result:
                    clientsocket.send(bytes(TRUE, UNIC_FORMAT))
                    break
                else:
                    clientsocket.send(bytes(FALSE, UNIC_FORMAT))
            else:
                break

    def engDetails(self, clientsocket, mycursor):
        while True:
            username = clientsocket.recv(BYTES).decode()
            if username:
                print("Recieved username: {}".format(username))
                query = '''SELECT first_name, last_name, email
                                    FROM user 
                                    WHERE username = \"{}\"
                                    AND type = \"engineer\"'''.format(username)
                mycursor.execute(query)
                result = mycursor.fetchall()
                if result:
                    clientsocket.send(bytes(TRUE, UNIC_FORMAT))
                    time.sleep(0.4)
                    clientsocket.send(bytes(result[0][0], UNIC_FORMAT))
                    time.sleep(0.4)
                    clientsocket.send(bytes(result[0][1], UNIC_FORMAT))
                    time.sleep(0.4)
                    clientsocket.send(bytes(result[0][2], UNIC_FORMAT))
                    break
                else:
                    clientsocket.send(bytes(FALSE, UNIC_FORMAT))
                    break
            else:
                break

    def handleType(self, clientsocket, mycursor):
        while True:
            print("called handle")
            type = clientsocket.recv(BYTES).decode()

            if type:
                print("Received type: {}".format(type))
                if type == QUERY_IDENTIFIER[0]:
                    self.login(clientsocket, mycursor)
                    self.handleType(clientsocket, mycursor)
                elif type == QUERY_IDENTIFIER[1]:
                    self.mac(clientsocket, mycursor)
                    self.handleType(clientsocket, mycursor)
                elif type == QUERY_IDENTIFIER[2]:
                    self.engDetails(clientsocket, mycursor)
                    self.handleType(clientsocket, mycursor)

    def run(self):
        mydb = mysql.connector.connect(
            host="35.197.185.32",
            user="root",
            passwd="3645",
            database="car_share"
        )

        mycursor = mydb.cursor()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), PORT))
        s.listen(QUEUE)  # Amount of connections to keep in queue

        # Listen forever for connections
        while True:
            # Once a connection is made, accept the request to connect and store
            #   client socket object and address of the client
            clientsocket, address = s.accept()
            print(f"Connection from {address} has been established!")

            # utf-8 denotes the type of bytes
            self.handleType(clientsocket, mycursor)

            # TODO clean up connection


CredCheck().run()
