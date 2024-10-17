# SERVERSIDE for AnakBuElsa UDP Chat

# *** Set Up Server Socket ***
# Import library
import socket
import threading
import queue

# Input serverIP and serverPort
serverIP, serverPort = str, int
serverIP = input("Input server IP address: ")
serverPort = int(input("Input server Port: "))

# uncomment to use localhost
clientIP = "localhost"
serverIP = "localhost"

# Initialize server's socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((serverIP, serverPort))

# *** Receive Message for Server ***
messages = queue.Queue()

def receive():
    while True:
        try:
            message, addr = server.recvfrom(2048)
            messages.put((message, addr))
        except:
            pass

def sendToClient():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            # Print the incoming message on the serverside
            print(message.decode())
            client = addr
            
            # send the message back to sender (return to sender)
            server.sendto(message, client)

tReceive = threading.Thread(target=receive)
tSendToClient = threading.Thread(target=sendToClient)

tReceive.start()
tSendToClient.start()

# *** Respond to Client Command ***
# Command 1: CREATE NEW ACCOUNT

# Command 2: LOG INTO ACCOUNT

# Command 3: CREATE NEW CHATROOM

# Command 4: JOIN CHATROOM