import tkinter as tk
from tkinter import ttk
import threading

import client_fui as fui



class client_ui:
    def __init__(self, root,client):
        self.root = root
        self.window()

        self.widgets()

        
        self.client = client
        self.is_running = True

    
    def window(self):
        self.root.title("client ui")# window title
        self.root.geometry("1100x750")# window size
        self.root.configure(bg="#087370")# biru

        self.root.grid_rowconfigure(0, weight=4)
        self.root.grid_columnconfigure(0, weight=4)

    def menu_bar(self):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        #login menu
        self.help = tk.Menu(self.menubar)
        self.menubar.add_cascade(label="help",menu = self.login)
        
    def widgets(self):
        style = ttk.Style()

        # Frame to hold Text widget and Scrollbar
        style.configure("FFrame.TFrame",background="light blue")
        self.frame = ttk.Frame(self.root,style="FFrame.TFrame")
        self.frame.grid(column=0,row=0, padx=10, pady=10,sticky="nsew")

        ### column 0 ###
        # big label
        self.frame.grid_rowconfigure(0, weight=1)

        style.configure("biglabel.Label",background="white",foreground="black",font=("arial",20))
        self.title_label = ttk.Label(self.frame, text="Client AnakBuElsa",style="biglabel.Label")
        self.title_label.grid(column=0,row=0,pady=10,padx=10)

        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # status text box
        self.status_text = tk.Text(self.frame, state='disabled',width=35,height=8)
        self.status_text.grid(column=0,row=1,padx=10, pady=5,rowspan=1)

        # refresh button
        style.configure("re.TButton", font=("Helvetica", 16), foreground="blue")
        self.button_start = ttk.Button(self.frame,text="refresh",style="re.TButton",command=self.print_status)
        self.button_start.grid(column=0,row=2,padx=20,pady=5,sticky="we")

        
        # login account ui
        #################
        style.configure("log.TFrame",background="sky blue")
        self.user_frame = ttk.Frame(self.frame,style="log.TFrame",width=30)
        self.user_frame.grid(column=0,row=3,padx=10, pady=10,sticky="nsew")

        style.configure("ipu.Label",background="white",foreground="black",font=("arial",10))
        self.ipu_label = ttk.Label(self.user_frame, text="ip use",style="ipu.Label")
        self.ipu_label.grid(column=0,row=0,pady=10,padx=10)

        self.ipu_message = ttk.Entry(self.user_frame, font=("Arial", 12))
        self.ipu_message.grid(column=1,row=0, padx=10, pady=5,sticky="w",columnspan=1)

        style.configure("poru.Label",background="white",foreground="black",font=("arial",10))
        self.poru_label = ttk.Label(self.user_frame, text="port use",style="poru.Label")
        self.poru_label.grid(column=0,row=1,pady=10,padx=10)

        self.poru_message = ttk.Entry(self.user_frame, font=("Arial", 12))
        self.poru_message.grid(column=1,row=1, padx=10, pady=5,sticky="w",columnspan=1)

        self.u_connect = ttk.Button(self.user_frame, text="connect",command=self.connect_button)
        self.u_connect.grid(column=0,row=2,padx=10, pady=5,sticky="w")

        self.u_disconnect = ttk.Button(self.user_frame, text="disconnect",command=self.disconnect_button)
        self.u_disconnect.grid(column=1,row=2,padx=10, pady=5,sticky="w")

        style.configure("logu.Label",background="white",foreground="black",font=("arial",10))
        self.title_label = ttk.Label(self.user_frame, text="username",style="logu.Label")
        self.title_label.grid(column=0,row=3,pady=10,padx=10)

        self.ulogin_message = ttk.Entry(self.user_frame, font=("Arial", 12))
        self.ulogin_message.grid(column=1,row=3, padx=10, pady=5,sticky="w",columnspan=1)

        style.configure("logp.Label",background="white",foreground="black",font=("arial",10))
        self.title_label = ttk.Label(self.user_frame, text="password",style="logp.Label")
        self.title_label.grid(column=0,row=4,pady=10,padx=10)

        self.upass_message = ttk.Entry(self.user_frame, font=("Arial", 12))
        self.upass_message.grid(column=1,row=4, padx=10, pady=5,sticky="w",columnspan=1)

        self.login_button = ttk.Button(self.user_frame, text="login",command=self.login)
        self.login_button.grid(column=0,row=5,padx=10, pady=5,sticky="w")

        self.logout_button = ttk.Button(self.user_frame, text="logout",command=self.logout)
        self.logout_button.grid(column=1,row=5,padx=10, pady=5,sticky="w")

        self.remove_button = ttk.Button(self.user_frame, text="remove account",command=self.remove)
        self.remove_button.grid(column=0,row=6,padx=10, pady=5,sticky="w")

        self.regis_button = ttk.Button(self.user_frame, text="register account",command=self.register)
        self.regis_button.grid(column=1,row=6,padx=10, pady=5,sticky="w")
        ###################


        # join chat room button
        ###############
        style.configure("log.TFrame",background="sky blue")
        self.join_frame = ttk.Frame(self.frame,style="log.TFrame",width=30)
        self.join_frame.grid(column=0,row=4,padx=10, pady=10,sticky="nsew")

        style.configure("juser.Label",background="white",foreground="black",font=("arial",10))
        self.title_label = ttk.Label(self.join_frame, text="chatname",style="juser.Label")
        self.title_label.grid(column=0,row=0,pady=10,padx=10)

        self.join_message = ttk.Entry(self.join_frame, font=("Arial", 12))
        self.join_message.grid(column=1,row=0, padx=10, pady=5,sticky="w",columnspan=2)

        style.configure("puser.Label",background="white",foreground="black",font=("arial",10))
        self.title_label = ttk.Label(self.join_frame, text="chat pass",style="puser.Label")
        self.title_label.grid(column=0,row=1,pady=10,padx=10)

        self.chpass_message = ttk.Entry(self.join_frame, font=("Arial", 12))
        self.chpass_message.grid(column=1,row=1, padx=10, pady=5,sticky="w",columnspan=2)

        self.join_button = ttk.Button(self.join_frame, text="join chat",command=self.joinchat)
        self.join_button.grid(column=0,row=2,padx=10, pady=5,sticky="w")

        self.exit_button = ttk.Button(self.join_frame, text="exit chat",command=self.exitchat)
        self.exit_button.grid(column=1,row=2,padx=10, pady=5,sticky="w")

        self.create_chat = ttk.Button(self.join_frame, text="create chat",command=self.createchat)
        self.create_chat.grid(column=2,row=2,padx=10, pady=5,sticky="w")
        ######################

        ### column 1 ###

        # connect server
        ####################
        style.configure("configure_frame.TFrame",background="sky blue")
        self.configure_frame = ttk.Frame(self.frame,style="configure_frame.TFrame",width=30)
        self.configure_frame.grid(column=1,row=0,sticky="nsew",padx=20,pady=20)
        self.configure_frame.grid_rowconfigure(0, weight=1)
        self.configure_frame.grid_rowconfigure(1, weight=1)
        self.configure_frame.grid_rowconfigure(2, weight=1)
        self.configure_frame.grid_columnconfigure(0, weight=0)
        self.configure_frame.grid_columnconfigure(1, weight=1)
        self.configure_frame.grid_columnconfigure(2, weight=1)
        self.configure_frame.grid_columnconfigure(3, weight=8)

        style.configure("ipslabel.Label",foreground="black",font=("arial",10))
        self.ip_label = ttk.Label(self.configure_frame, text="server ip",style="ipslabel.Label")
        self.ip_label.grid(column=0,row=0,pady=10,padx=10)

        style.configure("portslabel.Label",background="white",foreground="black",font=("arial",10))
        self.port_label = ttk.Label(self.configure_frame, text="server port",style="portslabel.Label")
        self.port_label.grid(column=0,row=1,pady=10,padx=10)

        self.server_ip = ttk.Entry(self.configure_frame, font=("Arial", 12))
        self.server_ip.grid(column=1,row=0, padx=10, pady=5,sticky="we",columnspan=3)

        self.server_port = ttk.Entry(self.configure_frame, font=("Arial", 12))
        self.server_port.grid(column=1,row=1, padx=10, pady=5,sticky="we",columnspan=3)

        self.connect = ttk.Button(self.configure_frame, text="connect",command=self.con_server)
        self.connect.grid(column=1,row=2,padx=10, pady=5,sticky="w")

        self.disconnect = ttk.Button(self.configure_frame, text="disconnect",command=self.discon_server)
        self.disconnect.grid(column=2,row=2,padx=10, pady=5,sticky="w")
        ####################

        # Create a Text widget (for chat display)
        self.chatbox = tk.Text(self.frame, state='disabled')
        self.chatbox.grid(column=1,row=1, padx=10, pady=10,rowspan=3)

        # Configure the frame to allow resizing
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        # senders frame 

        style.configure("schat.TFrame",background="gray")
        self.send_frame = ttk.Frame(self.frame,style="schat.TFrame")
        self.send_frame.grid(column=1,row=4,sticky="nsew",padx=10,pady=10)
        # Entry box to send messages
        self.send_frame.grid_columnconfigure(0, weight=1)
        self.entry_message = ttk.Entry(self.send_frame, font=("Arial", 12))
        self.entry_message.grid(column=0,row=0, padx=10, pady=5,sticky="we")
        self.entry_message.bind('<Return>', self.send_message)

        # Button to send the message
        self.send_button = ttk.Button(self.send_frame, text="Send", command=self.send_message)
        self.send_button.grid(column=0,row=1,padx=10, pady=5,sticky="we")

        # Button help
        self.help_button = ttk.Button(self.send_frame, text="Help", command=self.help)
        self.help_button.grid(column=0,row=2,padx=10, pady=5,sticky="we")


    def print_status(self):
        arr = self.client.status()
        self.status_text.config(state="normal")
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert("end",f"ip using : {str(arr[0])}\n")
        self.status_text.insert("end",f"port using : {str(arr[1])}\n")
        self.status_text.insert("end",f"username : {str(arr[2])}\n")
        self.status_text.insert("end",f"ip server: {str(arr[3])}\n")
        self.status_text.insert("end",f"port server : {str(arr[4])}\n")
        self.status_text.insert("end",f"chatname : {str(arr[5])}\n")
        self.status_text.config(state="disabled")
        pass

    def receive(self):
        while self.is_running:
            self.client.receive()
            if self.client.current_respond != "":
                self.display_message(self.client.current_respond)
                self.client.current_respond = ""

    def register(self):
        username = self.ulogin_message.get()
        password = self.upass_message.get()
        self.client.requestRegister(username,password)    
    
    def login(self):
        try:
            username = self.ulogin_message.get()
            password = self.upass_message.get()
            self.client.requestLogin(username,password)
            self.upass_message.delete(0, "end")
        except:
            self.display_message("error")

    def logout(self):
        self.client.requestLogout()
    
    def remove(self):
        username = self.ulogin_message.get()
        password = self.upass_message.get()
        self.client.requestRemove(username,password)
        self.upass_message.delete(0, "end")
             
    def createchat(self):
        chatname = self.join_message.get()
        chatpass = self.chpass_message.get()
        self.client.requestCreateChat(chatname,chatpass)

    def joinchat(self):
        chatname = self.join_message.get()
        chatpass = self.chpass_message.get()
        self.client.requestJoinChat(chatname,chatpass)

    def exitchat(self):
        if self.client.clientChat == None:
            self.display_message("You have already left chatroom")
        else:
            self.client.requestLeaveChat()

    def createchat(self):
        chatname = self.join_message.get()
        chatpass = self.chpass_message.get()
        self.client.requestCreateChat(chatname,chatpass)

    def send_message(self,event=None):
        message = self.entry_message.get()
        try:
            if message.strip():  # Only add non-empty messages
                if self.client.clientUsername == None or self.client.clientChat == None:
                    self.client.echo(message)
                    self.display_message(f"echo | {self.client.clientUsername}: {message}")
                    self.entry_message.delete(0, "end")
                else:
                    self.client.sendToChat(message)
                    # self.display_message(f"{self.client.clientchat} | {self.client.clientUsername}: {message}")
                    self.entry_message.delete(0, "end")
        except:
            self.display_message("error")

    def display_message(self, message):
        """Display the message in the chat window."""
        # Enable the Text widget to insert new content
        self.chatbox.config(state="normal")
        self.chatbox.insert("end", message + "\n")
        self.chatbox.config(state="disabled")  # Disable editing
        self.chatbox.see("end")  # Auto-scroll to the bottom

    def con_server(self):
        ip = self.server_ip.get()
        port = self.server_port.get()
        self.client.set_server(ip,port)
        self.server_ip.config(state="disabled")
        self.server_port.config(state="disabled")

    def discon_server(self):
        self.client.set_server(None,None)
        self.server_ip.config(state="normal")
        self.server_port.config(state="normal")

    def help(self):
        self.display_message('''
    ---------------------------------------------------------------------  
    |    LIST OF COMMANDS:                                              |
    |    1.  help       : see list of commands                          |
    |    2.  register   : register a new account                        |
    |    3.  login      : log into existing accounts                    |
    |    4.  createChat : create a new chatroom                         |
    |    5.  joinChat   : join existing chatrooms                       |
    |    6.  logout     : log out from current user                     |
    |    7.  leaveChat  : leave current chatroom                        |
    |    8.  status     : check current address, username, and chat     |
    ---------------------------------------------------------------------
        ''')

    def connect_button(self):
        try:
            ip = self.ipu_message.get()
            port = int(self.poru_message.get())
            self.client.connect(ip,port)
            self.is_running = True
            self.client.client_ip = ip
            self.client.client_port = port
            tReceiving = threading.Thread(target=self.receive,daemon=True)
            tReceiving.start()
            self.display_message("connected")
        except:
            self.display_message("error")


    def disconnect_button(self):
        self.is_running = False
        self.client.disconnect()
        self.display_message("disconnected")

# Run the application
if __name__ == "__main__":
    client = fui.client_fui()
    root = tk.Tk()
    app = client_ui(root,client)
    root.mainloop()