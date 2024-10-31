import socket
import threading
import queue

import auth as au


#### old message headers ####
#
# +-------------+-----------------------------------------------------------------+-------------------------------------------------------------------------------------+
# |  command    |                    request("COMMAND_TAG:{}")                    |                           receive("USER_RECEIVE_FLAG:{}")                           |
# +-------------+-----------------------------------------------------------------+-------------------------------------------------------------------------------------+
# | 0 help      | {command_tag}                                                   | {User_Receive_Flag}                                                                 |
# | 1 register  | {command_tag},{username}                                        | {User_Receive_Flag},{usernameAvailable},{username}                                  |
# | 2 login     | {command_tag},{username}                                        | {User_Receive_Flag},{usernameUsable},{username}                                     |
# | 3 createchat| {command_tag},{chatName},{chatPass}                             | {User_Receive_Flag},{chatroomAvailable},{chatName},{chatPass}                       |
# | 4 join chat | {command_tag},{joiningUsername},{joiningChatname},{joiningPass} | {User_Receive_Flag},{chatExists},{passwordCorrect},{joiningChatname},{joiningPass}  |
# | 5 logout    | {command_tag},{username},{chat}                                 | {User_Receive_Flag},{username},{chat}                                               |
# | 6 leavechat | {command_tag},{clientUsername},{clientChat}                     | {User_Receive_Flag},{username},{chat}                                               |
# | 7 echo      | {command_tag},{message},{echoUsername}                          | {User_Receive_Flag},{echoUsername},{echoMessage}                                    |
# | 8 sendtochat| {command_tag},{message},{clientUsername},{clientChat}           | {User_Receive_Flag},{message},{clientUsername},{clientChat}                         |
# +-------------+-----------------------------------------------------------------+-------------------------------------------------------------------------------------+

#### New message headers ####
# 
# +------------------+-----------------------------------------------------------------------+--------------------------------------------------------------------------------------------+
# |     command      |                       request("COMMAND_TAG:{}")                       |                               receive("USER_RECEIVE_FLAG:{}")                              |
# +------------------+-----------------------------------------------------------------------+--------------------------------------------------------------------------------------------+
# | 0 help           | {command_tag}                                                         | {User_Receive_Flag}                                                                        |
# | 1 register       | {command_tag}:|:{username}:|:{password}                               | {User_Receive_Flag}:|:{usernameAvailable}:|:{username}:|:{password}                        |
# | 2 login          | {command_tag}:|:{username}:|:{password}                               | {User_Receive_Flag}:|:{usernameUsable}:|:{username}                                        |
# | 3 logout         | {command_tag}:|:{username}:|:{chat}                                   | {User_Receive_Flag}:|:{username}:|:{chat}                                                  |
# | 4 remove account | {command_tag}:|:{username}:|:{password}                               | {User_Receive_Flag}:|:{username}:|:{status}                                                |
# | 5 createchat     | {command_tag}:|:{chatName}:|:{chatPass}                               | {User_Receive_Flag}:|:{chatroomAvailable}:|:{chatName}:|:{chatPass}                        |
# | 6 join chat      | {command_tag}:|:{joiningUsername}:|:{joiningChatname}:|:{joiningPass} | {User_Receive_Flag}:|:{chatExists}:|:{passwordCorrect}:|:{joiningChatname}:|:{joiningPass} |
# | 7 leavechat      | {command_tag}:|:{clientUsername}:|:{clientChat}                       | {User_Receive_Flag}:|:{username}:|:{chat}                                                  |
# | 8 echo           | {command_tag}:|:{echoUsername}|:|{message}                            | {User_Receive_Flag}:|:{echoUsername}:|:{echoMessage}                                       |
# | 9 sendtochat     | {command_tag}:|:{clientUsername}:|:{clientChat}:|:{message}           | {User_Receive_Flag}:|:{clientUsername}:|:{clientChat}:|:{message}                          |
# +------------------+-----------------------------------------------------------------------+--------------------------------------------------------------------------------------------+



class server_fui:
    def __init__(self,ip=None,port=None,file=None):
        self.ip =  ip
        self.port = port
        self.messages = queue.Queue()
        
        self.chatrooms = []
        self.file = file

        self.is_running = True

        self.current_message = None
        self.current_reply = None

    class Chatroom:
        def __init__(self, chatName, chatPass, chatParticipants):
            self.chatName = chatName
            self.chatPass = chatPass
            self.chatParticipants = chatParticipants

    def receive(self):
        try:
            message, addr = self.server.recvfrom(2048)
            self.messages.put((message, addr))
        except:
            pass
             
    
    def check_message(self,texts=str):
        com_check = texts[:12]
        if com_check == "COMMAND_TAG:":
            content = texts[12:].split(":|:")
        else:
            content = ["!",None]
        print(content)
        return content


    def sent_back(self):
        message, addr = self.messages.get()
        decodedMessage = message.decode()
        print(decodedMessage)
        
        self.current_message = decodedMessage
        try:
            content = self.check_message(decodedMessage)
        except:
            content = "!"
        match content[0]:
            case "!":
                self.current_reply = self.send_error(addr,message)
            case "0":
                self.current_reply = self.commandHelp(addr)
            case "1":
                self.current_reply = self.commandRegister(addr,content)
            case "2":
                self.current_reply = self.commandLogin(addr,content)
            case "3":
                self.current_reply = self.commandLogout(addr,content)
            case "4":
                self.current_reply = self.commandRemoveAcc(addr,content)
            case "5":
                self.current_reply = self.commandCreateChat(addr,content)
            case "6":
                self.current_reply = self.commandJoinChat(addr,content)
            case "7":
                self.current_reply = self.commandLeaveChat(addr,content)
            case "8":
                self.current_reply = self.commandEcho(addr,content)
            case "9":
                self.current_reply = self.commandSendToChat(addr,content)


    # Error message:
    def send_error(self,client,message):
        self.server.sendto(message, client)
        return f"{message} error"

    # Command 0: HELP
    def commandHelp(self,client):

        # set User_Receive_Flag
        User_Receive_Flag = 0
        self.server.sendto(f"USER_RECEIVE_FLAG:{User_Receive_Flag}".encode(), client)

        # DEBUGGING : print User_Receive_Info being sent
        # print(f"USER_RECEIVE_FLAG:{User_Receive_Flag}")
        return f"USER_RECEIVE_FLAG:{User_Receive_Flag}"
    
    # Command 1: CREATE NEW ACCOUNT
    def commandRegister(self,client, command_info):

        # set User_Receive_Flag
        User_Receive_Flag = 1

        # Get username in client
        username = command_info[1]
        password = command_info[2]

        if not au.check_existing_user(username):
            au.signup(username,password,self.file)
            # print(f"SERVER_ALERT:USERS_UPDATED,users={username}")
            usernameAvailable = True
        else:
            usernameAvailable = False
        
        self.server.sendto(f"USER_RECEIVE_FLAG:{User_Receive_Flag}:|:{usernameAvailable}:|:{username}:|:{password}".encode(), client)
        out = f"USER_RECEIVE_FLAG:{User_Receive_Flag}:|:{usernameAvailable}:|:{username}:|:{password}"
        print(out)
        return out

    # Command 2: LOG INTO ACCOUNT
    def commandLogin(self,client, command_info):
  
        # set User_Receive_Flag
        User_Receive_Flag = 2

        # Get username in client
        username = command_info[1]
        password = command_info[2]


        if au.check_credensial(username,password,self.file):# check username and password
            usernameUsable = True
            # print(f"SERVER_ALERT:USER_LOGIN,client{client} logged in using username \"{username}\"")
        # idk
        else:
            usernameUsable = False
        self.server.sendto(f"USER_RECEIVE_FLAG:{User_Receive_Flag}:|:{usernameUsable}:|:{username}".encode(), client)
        
        out = f"USER_RECEIVE_FLAG:{User_Receive_Flag}:|:{usernameUsable}:|:{username}"
        print(out)
        return out
    
    # Command 3: LOGOUT
    def commandLogout(self,client, command_info):
        # TESTING MESSAGE
        # server.sendto("LOGOUT".encode(), client)

        # set User_Receive_Flag
        User_Receive_Flag = 3

        username = command_info[1]
        chat = command_info[2]

        # If user is in a chatroom user will be removed from chatroom
        if chat != None:
            self.commandLeaveChat(client, command_info)
        
        self.server.sendto(f"USER_RECEIVE_FLAG:{User_Receive_Flag}:|:{username}:|:{chat}".encode(),client)

        # DEBUGGING : print User_Receive_Info being sent
        out = f"USER_RECEIVE_FLAG:{User_Receive_Flag}:|:{username}:|:{chat}"
        print(out)
        return out

    # Command 4: REMOVE ACCOUNT
    def commandRemoveAcc(self,client,command_info):
 
         # set User_Receive_Flag
        User_Receive_Flag = 4 

        #credential
        username = command_info[1]
        password = command_info[2]
        
        status = ""
        if au.check_credensial(username,password,self.file):
            status = au.remove_user(username,password,self.file)
            pass
        else:
            status = "wrong credential"
        self.server.sendto(f"USER_RECEIVE_FLAG:{User_Receive_Flag}:|:{username}:|:{status}".encode(),client)


        out = f"USER_RECEIVE_FLAG:{User_Receive_Flag}:|:{username}:|:{status}"
        print(out)
        return out
    
    # Command 5: CREATE NEW CHATROOM
    def commandCreateChat(self,client, command_info):
        # TESTING MESSAGE
        # server.sendto("CREATE CHAT".encode(), client)
        
        # set User_Receive_Flag
        User_Receive_Flag = 5 

        # Get chatname and pass from client
        chatName = command_info[1]
        chatPass = command_info[2]

        # check if chatroom is unique
        self.chatrooms
        chatUnique = True
        for chatroom in self.chatrooms:
            if chatName in chatroom.chatName:
                chatUnique = False

        # if chatName is unique, append the chatroom to chatrooms
        if chatUnique:
            # append the new chatroom to chatrooms
            self.chatrooms.append(self.Chatroom(chatName, chatPass, []))
            chatroomAvailable = True
            print(f"SERVER_ALERT:NEW_CHATROOM,chatrooms={self.chatrooms}")
        # if chatName is not unique, send notification to client requesting different chatName
        else:
            chatroomAvailable = False

        self.server.sendto(f"USER_RECEIVE_FLAG:{User_Receive_Flag}:|:{chatroomAvailable}:|:{chatName}:|:{chatPass}".encode(),client)

        # DEBUGGING : print User_Receive_Info being sent
        out = f"USER_RECEIVE_FLAG:{User_Receive_Flag}:|:{chatroomAvailable}:|:{chatName}:|:{chatPass}"
        print(out)
        return out
    
    
    # Command 6: JOIN CHATROOM
    def commandJoinChat(self,client, command_info):
        # TESTING MESSAGE
        # server.sendto("JOIN CHAT".encode(), client)

        # set User_Receive_Flag
        User_Receive_Flag = 6
        joiningUsername = command_info[1]
        joiningChatname = command_info[2]
        joiningPass = command_info[3]

        # check if chatname exists
        chatExists = False
        passwordCorrect = False
        for chatroom in self.chatrooms:
            if chatroom.chatName == joiningChatname:
            # if chatname exists check if password is correct
                chatExists = True
                if chatroom.chatPass == joiningPass:
                    # if password is correct client will be added as a chat participant
                    passwordCorrect = True
                    chatroom.chatParticipants.append(client)

        # put user into said chat
        
        self.server.sendto(f"USER_RECEIVE_FLAG:{User_Receive_Flag}:|:{chatExists}:|:{passwordCorrect}:|:{joiningChatname}:|:{joiningPass}".encode(), client)

        # DEBUGGING : print User_Receive_Info being sent
        out = f"USER_RECEIVE_FLAG:{User_Receive_Flag}:|:{chatExists}:|:{passwordCorrect}:|:{joiningChatname}:|:{joiningPass}"
        print(out)
        return out
    
    

    # Command 7: LEAVE CHATROOM
    def commandLeaveChat(self,client, command_info):
        # TESTING MESSAGE
        # server.sendto("LEAVE CHAT".encode(), client)

        # set User_Receive_Flag
        User_Receive_Flag = 7

        username = command_info[1]
        chat = command_info[2]

        for chatroom in self.chatrooms:
            # Remove client from chatroom
            if chatroom.chatName == chat:
                chatroom.chatParticipants.remove(client)
                # Alert server that client was removed from chatroom
                print(f"SERVER_ALERT:REMOVE_CLIENT_FROM_CHAT,user:{username} from client:{client} was removed from chatroom:{chat}")
                # Alert the chat that client was removed from chatroom
                # use SEND TO CHAT function

        # Alert client that it has been removed from chatroom
        self.server.sendto(f"USER_RECEIVE_FLAG:{User_Receive_Flag}:|:{username}:|:{chat}".encode(),client)

        # DEBUGGING : print User_Receive_Info being sent
        out = f"USER_RECEIVE_FLAG:{User_Receive_Flag}:|:{username}:|:{chat}"
        print(out)
        return out
    

    # Command 8: ECHO
    def commandEcho(self,client, command_info):
        # TESTING MESSAGE
        # server.sendto("ECHO".encode(), client)

        # set User_Receive_Flag
        User_Receive_Flag = 8

        echoMessage = command_info[2]
        echoUsername = command_info[1]
        print(f"SERVER_ALERT:ECHO,user:{echoUsername},message:{echoMessage}")
        print(f"USER_RECEIVE_FLAG:{User_Receive_Flag}:|:{echoUsername}:|:{echoMessage}")

        self.server.sendto(f"USER_RECEIVE_FLAG:{User_Receive_Flag}:|:{echoUsername}:|:{echoMessage}".encode(), client)

        # DEBUGGING : print User_Receive_Info being sent
        out = f"USER_RECEIVE_FLAG:{User_Receive_Flag}:|:{echoUsername}:|:{echoMessage}"
        print(out)
        return out
    

    # Command 9: SEND TO CHAT
    def commandSendToChat(self,client, command_info):
        # TESTING MESSAGE
        # server.sendto("SEND TO CHAT".encode(), client)

        # set User_Receive_Flag
        User_Receive_Flag = 9

        # get message, clientUsername, clientChat
        message = command_info[3]
        clientUsername = command_info[1]
        clientChat = command_info[2]

        # get corresponding chatroom and send message to all participants in the chatroom
        for chatroom in self.chatrooms:
            if chatroom.chatName == clientChat:
                for participant in chatroom.chatParticipants:
                    self.server.sendto(f"USER_RECEIVE_FLAG:{User_Receive_Flag}:|:{clientUsername}:|:{clientChat}:|:{message}".encode(), participant)
                    print(f"{clientChat} | {clientUsername}: {message}")

        # DEBUGGING : print User_Receive_Info being sent
        out = f"USER_RECEIVE_FLAG:{User_Receive_Flag}:|:{clientUsername}:|:{clientChat}:|:{message}"
        print(out)
        return out
    
    def start(self,ip=None,port=None):
        if ip== None or port == None:
            ip = self.ip
            port = self.port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((ip, port))
        # THREADING
        # tReceive = threading.Thread(target=self.receive)
        # tSendToClient = threading.Thread(target=self.sent_back)

        # tReceive.start()
        # tSendToClient.start()
        print("server started")
        
    def stop(self):
        # Stop the server and shut down the threads
        self.is_running = False
        self.server.close()  # Close the socket to release the port
        print("Server stopped.")

    def status(self):
        arr = [
            self.ip,
            self.port,
            len(self.chatrooms)
        ]
        return arr


if __name__ == "__main__":
    serip = input("localhost maybe")
    serport = int(input("port num"))
    user_database = "users.txt"

    alpha = server_fui(serip,serport,user_database)

    try:
        alpha.start()
        input("Press Enter to stop the server...\n")  # Keep the server running
    except KeyboardInterrupt:
        print("Stopping server...")
    finally:
        alpha.stop()

if __name__== "server_fui":
    print("banana")