import socket
import mysql.connector
from passlib.hash import sha256_crypt
import requests

QUEUE = 5
PORT = 9350
BYTES = 1024
UNIC_FORMAT = "utf-8"
FALSE = '0'
TRUE = '1'

mydb = mysql.connector.connect(
    host="35.197.185.32",
    user="root",
    passwd="3645",
    database="car_share"
)

mycursor = mydb.cursor()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), PORT))
s.listen(QUEUE) # Amount of connections to keep in queue

# Listen forever for connections
while True: 
    # Once a connection is made, accept the request to connect and store
    #   client socket object and address of the client
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    # utf-8 denotes the type of bytes
    while True:
        username = clientsocket.recv(BYTES).decode()
        if username:
            print("Recieved username: {}".format(username))
            query = '''SELECT username 
                        FROM customer 
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
                        FROM customer 
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
            if booking and booking["customer_id"] == user["customer_id"]:
                requests.put("http://127.0.0.1:5000/api/booking/status/complete", data=booking)
                clientsocket.send(bytes("Car returned successfuly", UNIC_FORMAT))
            else:
                clientsocket.send(bytes("Return unsuccessful, please ensure you" 
                                        " have an active booking", UNIC_FORMAT))
        else:
            break
    