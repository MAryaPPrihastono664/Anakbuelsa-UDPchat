# SERVERSIDE for AnakBuElsa UDP Chat

# *** Set Up Server Socket ***
# Import library
import socket
import threading
import queue

# Input serverIP and serverPort
serverIP, serverPort = str, int

# Comment the code for testing purposes
# serverIP = input("Input server IP address: ")
# serverPort = int(input("Input server Port: "))

# Testing IP and Port
clientIP = "localhost"
serverIP = "localhost"
serverPort = 8000

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

#  *** Send Message Back To Client***
def sendToClient():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            # Print the incoming message on the serverside
            print(message.decode())
            client = addr
            
            match message.decode():
                case "/help":
                    commandHelp(client)
                case "/register":
                    commandRegister(client)
                case "/login":
                    commandLogin(client)
                case "/createChat":
                    commandCreateChat(client)
                case "/joinChat":
                    commandJoinChat(client)
                case _:
                    # send the message back to sender (return to sender)
                    server.sendto(message, client)


tReceive = threading.Thread(target=receive)
tSendToClient = threading.Thread(target=sendToClient)

tReceive.start()
tSendToClient.start()

# *** Respond to Client Command ***
# Command 1: HELP
def commandHelp(client):
    # Testing Message
    helpMessage = '''
-----------------------------------------------------  
|    LIST OF COMMANDS:                              |
|    1.  /help       : see list of commands         |
|    2.  /register   : register a new account       |
|    3.  /login      : log into existing accounts   |
|    4.  /createChat : create a new chatroom        |
|    5.  /joinChat   : join existing chatrooms      |
-----------------------------------------------------
    '''
    server.sendto(f"{helpMessage}".encode(), client)
    return

# Command 2: CREATE NEW ACCOUNT
def commandRegister(client):
    # Testing Message
    server.sendto("REGISTER".encode(), client)
    return

# Command 3: LOG INTO ACCOUNT
def commandLogin(client):
    # Testing Message
    server.sendto("LOGIN".encode(), client)
    return

# Command 4: CREATE NEW CHATROOM
def commandCreateChat(client):
    # Testing Message
    server.sendto("CREATE CHAT".encode(), client)
    return

# Command 5: JOIN CHATROOM
def commandJoinChat(client):
    # Testing Message
    server.sendto("JOIN CHAT".encode(), client)
    return

# DATA STRUCTURE & STORAGE
# 1. Username
usernames = []
def isUsernameUnique(username, usernames):
    return username in usernames

# 2. Chatroom
chatrooms = []
class Chatroom:
    def __init__(self, chatName, chatPass):
        self.chatName = chatName
        self.chatPass = chatPass