# CLIENTSIDE for AnakBuElsa UDP Chat

# *** Set Up Client Socket ***
# Import library
import socket
import threading

# Input clientIP and clientPort
clientIP, clientPort = str, int
# clientIP = input("Input client IP: ")
clientPort = int(input("Input client Port: "))

# Input serverIP and serverPort
serverIP, serverPort = str, int
# serverIP = input("Input server IP: ")
# serverPort = int(input("Input server Port: "))


# Testing IP and Port
clientIP = "localhost"
# clientPort = 9000
serverIP = "localhost"
serverPort = 8000


# Initialize client's socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind((clientIP, clientPort))

# *** Receive Message ***
def receive():
    while True:
        try:
            message, _ = client.recvfrom(2048)
            print(message.decode())
        except:
            pass

t = threading.Thread(target=receive)
t.start()


# *** Send Message ***
# This is the function that will be given TCP later on
def sendingToServer():
    while True:
        message = input("")
        if message == "!q":
            # exit()
            print("Bye")
            client.close()
        else:
            # We might want to put header here
            client.sendto(f"{message}".encode(), (serverIP, serverPort))

sendingToServer()