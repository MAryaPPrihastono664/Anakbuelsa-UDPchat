import socket
import threading
import queue

messages = queue.Queue()
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 9999))

def receive():
    while True:
        try:
            message, addr = server.recvfrom(2048)
            messages.put((message, addr))
        except:
            pass

def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            print(message.decode())
            if addr not in clients:
                clients.append(addr)
            for client in clients:
                try:
                    if message.decode().startswith("SIGNUP_TAG"):
                        name = message.decode()[message.decode().index(":")+1:]
                        server.sendto(f"{name} joined!".encode(), client)
                    else:
                        server.sendto(message, client)
                except:
                    clients.remove(client)
        
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()

# SERVER SPECIFICATION
# Flow
# 1. Read message

# 2. If create chatroom (chatname, chatIP, chatPort, chatPass)
#   a. put chatname
#   b. put IP
#   c. put chatPort
#   d. put chatPass -> maybe do hashing

# 3. if create account (username, userIP, userPort)
#   a. put username
#   b. put userIP
#   c. put userPort

# 4. if join chatroom (joiningUsername, joiningPass)
#   a. put joiningUsername
#   b. put joiningPass -> check if match
