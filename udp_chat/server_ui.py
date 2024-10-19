import tkinter as tk
from tkinter import ttk # this is another part of tkinter that has more features

def gun():
    print("pew pew")

class server_main():
    # server ui

    def __init__(self,root):
        self.root = root
        
        self.window()

        self.widgets()

        pass
    

    def window(self):
        self.root.title("server ui")# window title

        self.root.geometry("500x300")# window size

        self.root.configure(bg="#087370")# biru

        

    def widgets(self):
        style = ttk.Style()

        #frame
        style.configure("FFrame.TFrame",background="light blue")
        self.frame = ttk.Frame(self.root,style="FFrame.TFrame")
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)

        # big text
        style.configure("biglabel.Label",background="white",foreground="green",font=("arial",30))
        self.label = ttk.Label(self.frame, text="server ui idk",style="biglabel.Label")
        self.label.pack(pady=10)

        # textbox
        self.textbox_ip = ttk.Entry(self.frame, font=("arial",10))
        self.textbox_ip.pack(padx=20,pady=20)

        self.textbox_port = ttk.Entry(self.frame, font=("arial",10))
        self.textbox_port.pack(padx=20,pady=20)

        # button
        style.configure("start.TButton", font=("Helvetica", 16), foreground="blue")
        self.button_start = ttk.Button(self.frame,text="start",style="start.TButton",command=self.outall)
        self.button_start.pack(padx=20,pady=20)


        pass
    def outall(self):
        gun()
        ip = self.textbox_ip.get()
        port = self.textbox_port.get()
        print(ip)
        print(port)
        pass


if __name__ == "__main__":
    root = tk.Tk()
    ui = server_main(root)
    root.mainloop()