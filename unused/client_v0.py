import socket
import threading
import random

# ALGORITMA
# 1. Masuk
#   a. Buat akun
#   b. Masuk ke akun
#       i. Buat chatroom
#       ii. Gabung ke chatroom
#   c. Keluar


def main():
    # Tanyakan aksi
    aksi = perintah()

    # Respon sesuai aksi
    if aksi == "keluar":
        quit()
    return


def buatAkun():
    return


def masukAkun():
    return

def perintah():
    return


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("localhost", random.randint(8000, 9000)))

name = input("Nickname: ")


def receive():
    while True:
        try:
            message, _ = client.recvfrom(2048)
            print(message.decode())
        except:
            pass


t = threading.Thread(target=receive)
t.start()

client.sendto(f"SIGNUP_TAG:{name}".encode(), ("localhost", 9999))

while True:
    message = input("")
    if message == "!q":
        # exit()
        client.close()
    else:
        client.sendto(f"{name}: {message}".encode(), ("localhost", 9999))


# CLIENT SPECIFICATION
# Available Command
# 1. Create chatroom
#   a. input room name -> chatname
#   b. input room IP Address -> chatIP
#   c. input room port number -> chatPort
#   d. input room password -> chatPass
class Chatroom:
    def __init__(self, chatname, chatIP, chatPort, chatPass):
        self.chatname = chatname
        self.chatIP = chatIP
        self.chatPort = chatPort
        self.chatPass = chatPass
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((chatIP, chatPort))


chatrooms = []


def createChatroom(chatname, chatIP, chatPort, chatPass):
    new_chatroom = Chatroom(chatname, chatIP, chatPort, chatPass)
    chatrooms.append(new_chatroom)

# 2. Create account
#   a. input username (must be unique) -> username
#   b. input user IP Address -> userIP
#   c. input user port - -> userPort


class Client:
    def __init__(self, username, userIP, userPort):
        self.username = username
        self.userIP = userIP
        self.userPort = userPort
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((userIP, userPort))


clients = []


def createAccount(username, userIP, userPort):
    clients.append(Client(username, userIP, userPort))


# 3. Join chatroom
#   a. asked for username -> joiningUsername
#   b. asked for room password -> joiningPass
def joinChatroom(joiningUsername, joiningPass):
    return
