import socket
import mysql.connector
from passlib.hash import sha256_crypt

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
        if not username:
            break

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

    while True:
        password = clientsocket.recv(BYTES).decode()
        if not password:
            break

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