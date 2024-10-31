import tkinter as tk
from tkinter import ttk # this is another part of tkinter that has more features
from tkinter.scrolledtext import ScrolledText
import threading

import server_fui as fui
#### required function
# display status
# print info
# start
# stop


def gun():
    print("pew pew")

class server_main():
    # server ui

    def __init__(self,root,server):
        self.root = root
        self.window()
        self.widgets()

        self.server = server
        
        self.is_running = False

    def window(self):
        self.root.title("server ui")# window title
        self.root.geometry("950x700")# window size
        self.root.configure(bg="#087370")# biru

        # Allow root window to resize properly
        self.root.grid_rowconfigure(0, weight=4)
        self.root.grid_columnconfigure(0, weight=4)

    def widgets(self):
        style = ttk.Style()

        #frame
        style.configure("FFrame.TFrame",background="light blue")
        self.frame = ttk.Frame(self.root,style="FFrame.TFrame")
        self.frame.grid(column=0,row=0, padx=10, pady=10,sticky="nsew")

        
        # Configure grid inside the frame for resizing
        self.frame.grid_columnconfigure(0, weight=2) # resizing for column 0
        self.frame.grid_rowconfigure(1, weight=1)  # Row with the update box
        self.frame.grid_rowconfigure(6, weight=1)  # Row with the scroll text area
        
        self.frame.grid_columnconfigure(1, weight=1)  # Column for the scroll text

        # big text
        style.configure("biglabel.Label",background="white",foreground="black",font=("arial",30))
        self.label = ttk.Label(self.frame, text="Server AnakBuElsa",style="biglabel.Label")
        self.label.grid(column=0,row=0,pady=10,padx=10,sticky="we")

        # update box
        self.update_box = tk.Text(self.frame, state='disabled')
        self.update_box.grid(row=1, column=0, padx=10, pady=5, sticky="nw")

        # refresh button
        style.configure("re.TButton", font=("Helvetica", 16), foreground="blue")
        self.button_start = ttk.Button(self.frame,text="refresh",style="re.TButton",command=self.print_status)
        self.button_start.grid(column=0,row=2,padx=20,pady=5,sticky="we")

        # info box
        self.scroll_screen = ScrolledText(self.frame, height=20,)
        self.scroll_screen.grid(row=0, column=1, rowspan=7,columnspan=2, padx=20, pady=5,sticky="nsew")


        # textbox
        #####3
        
        style.configure("configure_frame.TFrame",background="sky blue")
        self.configure_frame = ttk.Frame(self.frame,style="configure_frame.TFrame",width=30)
        self.configure_frame.grid(column=0,row=3,sticky="nsew",padx=10,pady=10)

        self.configure_frame.grid_rowconfigure(0, weight=1)
        self.configure_frame.grid_columnconfigure(0, weight=0)

        style.configure("ipslabel.Label",foreground="black",font=("arial",10))
        self.title_label = ttk.Label(self.configure_frame, text="server ip",style="ipslabel.Label")
        self.title_label.grid(column=0,row=0,pady=10,padx=10)

        style.configure("portslabel.Label",background="white",foreground="black",font=("arial",10))
        self.title_label = ttk.Label(self.configure_frame, text="server port",style="portslabel.Label")
        self.title_label.grid(column=0,row=1,pady=10,padx=10)

        self.textbox_ip = ttk.Entry(self.configure_frame, font=("arial",10))
        self.textbox_ip.grid(column=1,row=0,padx=20,pady=10,sticky="we")

        self.textbox_port = ttk.Entry(self.configure_frame, font=("arial",10))
        self.textbox_port.grid(column=1,row=1,padx=20,pady=10,sticky="we")
        #####

        # start button
        style.configure("start.TButton", font=("Helvetica", 16), foreground="blue")
        self.button_start = ttk.Button(self.frame,text="start",style="start.TButton",command=self.start_button)
        self.button_start.grid(column=0,row=4,padx=20,pady=5,sticky="we")

        # stop button
        style.configure("start.TButton", font=("Helvetica", 16), foreground="blue")
        self.button_stop = ttk.Button(self.frame,text="stop",style="start.TButton",command=self.stop_button)
        self.button_stop.grid(column=0,row=5,padx=20,pady=5,sticky="we")


        pass

    def print_info(self):
        while self.is_running:
            while not self.server.messages.empty():
                self.server.sent_back()
                text1 = self.server.current_message
                text2 = self.server.current_reply
                self.scroll_screen.config(state='normal')
                self.scroll_screen.insert(tk.END, text1+"\n"+text2+"\n")
                self.scroll_screen.config(state='disabled')

    def receive_loop(self):
        while self.is_running:
            self.server.receive()


    def print_status(self):
        arr = self.server.status()
        print(arr)
        self.update_box.config(state="normal")
        self.update_box.delete(1.0, tk.END)
        self.update_box.insert(tk.END,"server ip : "+str(arr[0])+"\n")
        self.update_box.insert(tk.END,"server port : "+str(arr[1])+"\n")
        self.update_box.insert(tk.END,"chatroom number : "+str(arr[2])+"\n")
        self.update_box.config(state="disabled")

    def start_button(self):
        try:
            ip = self.textbox_ip.get()
            port = int(self.textbox_port.get())
            if ip != "":
                self.server.start(ip,port)
                self.is_running = True
                tReceive = threading.Thread(target=self.print_info,daemon=True)
                tSendToClient = threading.Thread(target=self.receive_loop,daemon=True)
                tReceive.start()
                tSendToClient.start()
                self.server.ip = ip
                self.server.port = port
                self.print_status()
                self.scroll_screen.insert(tk.END, "server start\n")
                self.button_start.config(state="disabled")
                self.textbox_ip.config(state="disabled")
                self.textbox_port.config(state="disabled")
            else:
                self.scroll_screen.insert(tk.END, "input ip\n")  
        except:
            self.scroll_screen.insert(tk.END, "error\n")

    def stop_button(self):
        try:
            self.server.stop()
            self.is_running = False
            self.scroll_screen.insert(tk.END, "server stop\n")
            self.button_start.config(state="normal")
            self.textbox_ip.config(state="normal")
            self.textbox_port.config(state="normal")
        except:
            self.scroll_screen.insert(tk.END, "error\n")



if __name__ == "__main__":
    file = "users.txt"
    serv = fui.server_fui(file=file)
    
    root = tk.Tk()
    
    ui = server_main(root,serv)
    root.mainloop()