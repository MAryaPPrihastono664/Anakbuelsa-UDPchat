import socket
import threading
import sys

import encryptor as enc


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


### variable changes ### :|:


class client_fui:

    def __init__(self,client_ip=None,client_port=None,server_ip=None,server_port=None):
        self.client_ip = client_ip
        self.client_port = client_port
        self.server_ip = server_ip
        self.server_port = server_port

        self.serverAddress = (self.server_ip, self.server_port)
        self.clientAddress = (self.client_ip, self.client_port)


        self.clientUsername = None
        self.clientChat = None
        self.clientPass = None

        self.current_respond = ""

    # get shift
    def get_shift(self,shift)->int:
        first_l = ord(shift[0])
        intshift = (first_l%30 + len(shift))%31
        return intshift
    
    def sentToserver(self,message=None):
        if message ==None:
            message = input("ppp:\n")
        match message:
            case "!q":
                print("Bye")
                sys.exit()
                self.client.close()
            case "/help":
                self.requestHelp()
            case "/register":
                self.requestRegister()
            case "/login":
                self.requestLogin()
            case "/logout":
                self.requestLogout()
            case "/remove":
                self.requestRemove()
            case "/createChat":
                self.requestCreateChat()
            case "/joinChat":
                self.requestJoinChat()
            case "/leaveChat":
                self.requestLeaveChat()
            case "/status":
                self.status()
            case _:
                if self.clientChat == None: # user is not logged in and not in a chatroom
                    self.echo(message)
                elif self.clientUsername != None and self.clientChat != None: #user is logged in and in a chatroom
                    self.sendToChat(message)
                # failsafe if message has no/broken header
                else:
                    pass
        message = None

    ### request functions ##3
    # 0. REQUEST HELP
    def requestHelp(self):
        command_tag = 0
        self.client.sendto(f"COMMAND_TAG:{command_tag}".encode(), self.serverAddress)

        # DEBUGGING : check command info being sent
        print(f"COMMAND_TAG:{command_tag}")

    # 1. REQUEST REGISTER
    # needs input edit
    def requestRegister(self,username=None,password=None):
        if username == None or password == None:
            username = input("insert username:\n")
            password = input("insert password:\n")
        command_tag = 1

        # check if user is already logged in with the username
        # if yes it means the username is already registered
        if self.clientUsername == username:
            print(f"You are already logged in and registered as \"{username}\", Please reuse /register with a different username")
        else:
            self.client.sendto(f"COMMAND_TAG:{command_tag}:|:{username}:|:{password}".encode(), self.serverAddress)

        # DEBUGGING : check command info being sent
        print(f"COMMAND_TAG:{command_tag}:|:{username}:|:{password}")

    # 2. REQUEST LOGIN
    # need input
    def requestLogin(self,username=None,password=None):
        if username == None or password == None:
            username = input("insert username:\n")
            password = input("insert password:\n")
        command_tag = 2


        # Check if user is currently logged in
        if self.clientUsername != None and self.clientUsername != None:
            print(f"You are already logged in as \"{self.clientUsername}\", please logout before logging in")
        else:
            self.client.sendto(f"COMMAND_TAG:{command_tag}:|:{username}:|:{password}".encode(), self.serverAddress) 

        # DEBUGGING : check command info being sent
        # print(f"COMMAND_TAG:{command_tag}:|:{username}")


    # 3. REQUEST LOGOUT
    def requestLogout(self):
        command_tag = 3

        username = self.clientUsername
        chat = self.clientChat
        if username == None:
            print("You are already logged out")
        else:
            self.client.sendto(f"COMMAND_TAG:{command_tag}:|:{username}:|:{chat}".encode(), self.serverAddress)

        # DEBUGGING : check command info being sent
        # print(f"COMMAND_TAG:{command_tag}:|:{username}:|:{chat}")


    # 4. REQUEST REMOVE
    # need input also password
    def requestRemove(self,username=None,password=None):
        if username == None or password == None:
            username = input("insert username:\n")
            password = input("insert password:\n")
        command_tag = 4

        if self.clientUsername !=None:
            self.client.sendto(f"COMMAND_TAG:{command_tag}:|:{username}:|:{password}".encode(), self.serverAddress) 
        else:
            print(f"You are not logged in, please login first")




    # 5. REQUEST CREATE CHAT
    # need input
    def requestCreateChat(self,chatName=None,chatPass=None):
        if chatName == None:
            chatName = input("insert chat name:")
        command_tag = 5
  
        # Check if user is currently in a chatroom
        # if yes it means the chatroom has already been created
        if chatName == self.clientChat:
            print("This chatroom has already been created and you are in it!")
        else:
            if chatPass == None:
                chatPass = str(input("Chat password: "))
            self.client.sendto(f"COMMAND_TAG:{command_tag}:|:{chatName}:|:{chatPass}".encode(), self.serverAddress)

        # DEBUGGING : check command info being sent
        # print(f"COMMAND_TAG:{command_tag}:|:{chatName}:|:{chatPass}")

    # 6. REQUEST JOIN CHAT
    # need intputet
    def requestJoinChat(self,joiningChatname=None,joiningPass=None):
        if joiningChatname == None or joiningPass == None:
            joiningChatname = input("insert chatname")
            joiningPass = input("insert chat pass")
        command_tag = 6


        joiningUsername = self.clientUsername

        # Check if user is logged in
        # user cannot join a chatroom unless logged in
        if joiningUsername == None:
            print(f"You are not logged in! Please log in before joining a chatroom")
        # Check if clientChat is empty and if user has already joined a chatroom
        # if clienChat is empty then user can join a chatroom
        elif self.clientChat != None:
            print(f"You have already joined the chatroom \"{self.clientChat}\", please leave any chat before using /joinChat")
        else:
            self.client.sendto(f"COMMAND_TAG:{command_tag}:|:{joiningUsername}:|:{joiningChatname}:|:{joiningPass}".encode(), self.serverAddress) 

        # DEBUGGING : check command info being sent
        # print(f"COMMAND_TAG:{command_tag}:|:{joiningUsername}:|:{joiningChatname}:|:{joiningPass}")

    

    # 7. REQUEST LEAVE CHAT
    def requestLeaveChat(self):
        command_tag = 7


        if self.clientChat == None:
            print("You have already left chatroom")
        else:
            self.client.sendto(f"COMMAND_TAG:{command_tag}:|:{self.clientUsername}:|:{self.clientChat}".encode(), (self.serverAddress))

        # DEBUGGING : check command info being sent
        # print(f"COMMAND_TAG:{command_tag}:|:{clientUsername}:|:{clientChat}")

    # 8. ECHO
    # message
    def echo(self,message=str):
        command_tag = 8
        echoUsername = self.clientUsername
        self.client.sendto(f"COMMAND_TAG:{command_tag}:|:{echoUsername}:|:{message}".encode(), self.serverAddress)

        # DEBUGGING : check command info being sent
        # print(f"COMMAND_TAG:{command_tag}:|:{message}:|:{echoUsername}")

    # 9. SEND TO CHAT
    # message
    def sendToChat(self,message):
        command_tag = 9
        shift = self.get_shift(self.clientPass)
        en_message = enc.ceasar_encrypt(message,shift)

        self.client.sendto(f"COMMAND_TAG:{command_tag}:|:{self.clientUsername}:|:{self.clientChat}:|:{en_message}".encode(), self.serverAddress)

        # DEBUGGING : check command info being sent
        # print(f"COMMAND_TAG:{command_tag}:|:{message}:|:{clientUsername}:|:{clientChat}")

    # 10. STATUS
    def status(self):
        currentStatus = f'''
---------------------------------------------
    Current Clientside Status               
    clientAddress   : {self.client_ip}       
    serverAddress   : {self.server_ip}       
    clientUsername  : {self.clientUsername}      
    clientChat      : {self.clientChat}          
---------------------------------------------
'''
        print(currentStatus)


    def check_message(self,User_Respond_Info):
        User_Respond = User_Respond_Info.split(":|:")
        return User_Respond

    def receive(self):
        try:
            message, _ = self.client.recvfrom(2048)
            decodedMessage = message.decode()
            User_Receive_Flag = decodedMessage[:18]
            # DEBUGGING : check decoded message
            # print("---")
            # print(decodedMessage)
            # print("---")

            if User_Receive_Flag == "USER_RECEIVE_FLAG:":
                User_Respond_Info = self.check_message(decodedMessage[18:])
                User_Respond_Number = User_Respond_Info[0]
                match User_Respond_Number:
                    case "0":
                        self.current_respond = self.respondHelp(User_Respond_Info)
                    case "1":
                        self.current_respond = self.respondRegister(User_Respond_Info)
                    case "2":
                        self.current_respond = self.respondLogin(User_Respond_Info)
                        # print(f"user: {clientUsername}")
                    case "3":
                        self.current_respond = self.respondLogout(User_Respond_Info)
                    case "4":
                        self.current_respond = self.respondRemove(User_Respond_Info)
                    case "5":
                        self.current_respond = self.respondCreateChat(User_Respond_Info)
                    case "6":
                        self.current_respond = self.respondJoinChat(User_Respond_Info)
                        # print(f"chat: {clientChat}")
                    
                    case "7":
                        self.current_respond = self.respondLeaveChat(User_Respond_Info)
                    case "8":
                        self.current_respond = self.respondEcho(User_Respond_Info)
                    case "9":
                        self.current_respond = self.respondSendToChat(User_Respond_Info)

                # Hardcode Status Checker
                # Get current username and chatroom
                # global clientUsername, clientChat
                # print(clientUsername, clientChat)
                # print("-------------------------")

            # failsafe if received message has no/broken header
            else:
                print(decodedMessage)
        except:
            pass

    ## responds ##
    def respondHelp(self,User_Respond_Info):
        # Help Message
        helpMessage = '''
    ---------------------------------------------------------------------  
    |    LIST OF COMMANDS:                                              |
    |    1.  /help       : see list of commands                         |
    |    2.  /register   : register a new account                       |
    |    3.  /login      : log into existing accounts                   |
    |    4.  /createChat : create a new chatroom                        |
    |    5.  /joinChat   : join existing chatrooms                      |
    |    6.  /logout     : log out from current user                    |
    |    7.  /leaveChat  : leave current chatroom                       |
    |    8.  /status     : check current address, username, and chat    |
    ---------------------------------------------------------------------
        '''
        print(helpMessage)
        
        # DEBUGGING : print User_Respond_Info
        # print(User_Respond_Info)

    # 1. REGISTER
    def respondRegister(self,User_Respond_Info):
        usernameAvailable = User_Respond_Info[1]
        username = User_Respond_Info[2]
        out = ""

        if usernameAvailable == "True":
            print(f"Succesfully registered username \"{username}\"!")
            print("Please log in using the username")
            out = "Succesfully registered username \"{username}\"!\nPlease log in using the username"

        else:
            print(f"Username \"{username}\" is not available!")
            print("Please reuse /register with a different username")
            out = "Username \"{username}\" is not available!\nPlease register with a different username"
        return out

        # DEBUGGING : print User_Respond_Info
        # print(User_Respond_Info)

    # 2. LOGIN
    def respondLogin(self,User_Respond_Info):
        usernameUsable = User_Respond_Info[1]
        username = User_Respond_Info[2]
        out = ""

        if usernameUsable == "True":
            print(f"Logged in successfully using username \"{username}\"!")
            self.clientUsername = username
            out = f"Logged in successfully using username \"{username}\"!"
            
        else:
            print(f"Username or password is incorrect!")
            print("Please check input")
            out = f"Username or password is incorrect!\nPlease check input"
        print(f"Current username: {self.clientUsername}")
        return out

        

        # DEBUGGING : print User_Respond_Info
        # print(User_Respond_Info)

    # 3. LOGOUT
    def respondLogout(self,User_Respond_Info):
        username = User_Respond_Info[1]
        # unused but maybe useful
        # chat = User_Respond_Info[2]


        print(f"Successfully logged out from user \"{username}\"")
        self.clientUsername = None
        out = f"Successfully logged out from user \"{username}\""


        # DEBUGGING : print User_Respond_Info
        # print(User_Respond_Info)
        return out

    # 4. REMOVE ACCOUNT
    def respondRemove(self,User_Respond_Info):
        out = ""
        if User_Respond_Info[2] =="account removed":
            self.clientUsername = None
            self.clientChat = None
            out = f"username {User_Respond_Info[1]} successfully removed"
        else:
            out = f"removing {User_Respond_Info[1]} failed"
            
        print(out)
        return out
        

    # 5. CREATE CHATROOM
    def respondCreateChat(self,User_Respond_Info):
        chatroomAvailable = User_Respond_Info[1]
        chatName = User_Respond_Info[2]
        chatPass = User_Respond_Info[3]
        if chatroomAvailable == "True":
            out = f"Chatroom created! Please join the chatroom \"{chatName}\" using the password \"{chatPass}\""
        else:
            out = f"Chatname \"{chatName}\" is already taken! Please reuse /createChat with a different chatname"
        print(out)

        # DEBUGGING : print User_Respond_Info
        # print(User_Respond_Info)
        return out

    # 6. JOIN CHATROOM
    def respondJoinChat(self,User_Respond_Info):
        chatExists = User_Respond_Info[1]
        passwordCorrect = User_Respond_Info[2]
        joiningChatname = User_Respond_Info[3]
        joiningPass = User_Respond_Info[4]

        out = ""

        if chatExists == "True":
            if passwordCorrect == "True":
                self.clientChat = joiningChatname
                self.clientPass = joiningPass
                out = (f"Current chat: {self.clientChat}")
            else:
                self.clientChat = None
                self.clientPass = None
                out = (f"Password \"{joiningPass}\" is incorrect! Please reuse /joinchat with a correct password for chat \"{joiningChatname}\"")
        else:
            self.clientChat = None
            self.clientPass = None
            out = (f"Chat \"{joiningChatname}\" does not exist! Please reuse /joinChat with existing chatName")

        print(out)
        

        # DEBUGGING : print User_Respond_Info
        # print(User_Respond_Info)
        return out


    # 7. LEAVE CHAT
    def respondLeaveChat(self,User_Respond_Info):
        # unused but maybe useful
        # username = User_Respond_Info.split(",")[1]
        chat = User_Respond_Info[2]


        self.clientChat = None
        out = (f"Successfully left chatroom \"{chat}\"")
        
        # DEBUGGING : print User_Respond_Info
        # print(User_Respond_Info)
        print(out)
        return out

    # 8. ECHO
    def respondEcho(self,User_Respond_Info):
        echoUsername = User_Respond_Info[1]
        echoMessage = User_Respond_Info[2]

        if echoUsername != "None":
            out = (f"{echoUsername} ECHO: {echoMessage}")
        else:
            out = (f"SERVER ECHO: {echoMessage}")

        # DEBUGGING : print User_Respond_Info
        # print(User_Respond_Info)
        print(out)
        return out

    # 9. SEND TO CHAT
    # decrypt here
    def respondSendToChat(self,User_Respond_Info):
        # get message, clientUsername, clientChat
        message = User_Respond_Info[3]
        clientUsername = User_Respond_Info[1]
        clientChat = User_Respond_Info[2]

        shift = self.get_shift(self.clientPass)
        de_message = enc.ceasar_decrypt(message,shift)

        out = (f"{clientChat} | {clientUsername}: {de_message}")
        print(out)
        return out

    def status(self):
        return [self.client_ip,
                self.client_port,
                self.clientUsername,
                self.server_ip,
                self.server_port,
                self.clientChat
                ]

    def connect(self,ip=None,port=None):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind((ip,port))
        print("connecting")

        # tReceiving = threading.Thread(target=self.receive)
        # tReceiving.start()

        # tSending = threading.Thread(target=self.sentToserver)
        # tSending.start()

    def disconnect(self):
        self.client.close()
        print("disconnecting")
        pass

    def set_server(self,ip,port):
        self.server_ip = ip
        self.server_port = port
        self.serverAddress = (self.server_ip, int(self.server_port))
    
    def stop_server(self):
        self.server_ip = None
        self.server_port = None


if __name__ == "__main__":

    c_ip = "localhost"
    c_port = int(input("port c: "))
    s_ip = "localhost"
    s_port = 7000

    client = client_fui(c_ip,c_port,s_ip,s_port)
    client.start()
    pass


