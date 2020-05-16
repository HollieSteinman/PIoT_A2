# if sha256_crypt.verify(pwRecieved, databasePW)

import socket

QUEUE = 5
PORT = 9350
BYTES = 1024
UNIC_FORMAT = "utf-8"
FALSE = '0'
TRUE = '1'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), PORT))
s.listen(QUEUE) # Amount of connections to keep in queue

# Listen forever for connections
while True: 
    # Once a connection is made, accept the request to connect and store
    #   client socket object and address of the client
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    clientsocket.send(bytes("Connection established with server!", "utf-8"))
    # utf-8 denotes the type of bytes
    while True:
        username = clientsocket.recv(BYTES)
        if not username:
            break

        print("Recieved username: {}".format(username.decode()))
        # TODO validate the username with database
        valid = True
        if valid:
            clientsocket.send(bytes(TRUE, UNIC_FORMAT))
            break
        else:
            clientsocket.send(bytes(FALSE, UNIC_FORMAT))

    while True:
        password = clientsocket.recv(BYTES)
        if not password:
            break

        print("Recieved password: {}".format(password.decode()))
        # TODO validate password with database
        correct = True
        if correct:
            clientsocket.send(bytes(TRUE, UNIC_FORMAT))
            break
        else:
            clientsocket.send(bytes(FALSE, UNIC_FORMAT))