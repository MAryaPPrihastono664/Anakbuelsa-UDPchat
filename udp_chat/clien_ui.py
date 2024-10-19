import tkinter as tk
from tkinter import ttk

import tkinter as tk
from tkinter import ttk

class client_ui:
    def __init__(self, root):
        self.root = root
        
        self.window()

        self.menu_bar()
        self.widgets()

    
    def window(self):
        self.root.title("client ui")# window title

        self.root.geometry("500x600")# window size

        self.root.configure(bg="#087370")# biru

        

    def menu_bar(self):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        #login menu
        self.login = tk.Menu(self.menubar)

        self.menubar.add_cascade(label="login",menu = self.login)
        
    def widgets(self):
        style = ttk.Style()

        


        # Frame to hold Text widget and Scrollbar
        style.configure("Framem.TFrame",background="light blue")
        self.frame = ttk.Frame(self.root,style="Framem.TFrame")
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Create a Text widget (for chat display)
        self.chat_display = tk.Text(self.frame, wrap="word", font=("Arial", 12))
        self.chat_display.grid(row=0, column=0, sticky="nsew")

        # Create a Scrollbar and attach it to the Text widget
        self.scrollbar = ttk.Scrollbar(self.frame, command=self.chat_display.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure the Text widget to work with the scrollbar
        self.chat_display.config(yscrollcommand=self.scrollbar.set,state=tk.DISABLED)

        # Configure the frame to allow resizing
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        # Entry box to send messages
        self.entry_message = ttk.Entry(self.root, font=("Arial", 12))
        self.entry_message.pack(fill="x", padx=10, pady=5)


        # Button to send the message
        self.send_button = ttk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=5)

    def send_message(self):
        """Append the message to the chat display."""
        message = self.entry_message.get()
        if message.strip():  # Only add non-empty messages
            self.display_message(f"You: {message}")
            self.entry_message.delete(0, "end")

    def display_message(self, message):
        """Display the message in the chat window."""
        # Enable the Text widget to insert new content
        self.chat_display.config(state="normal")
        self.chat_display.insert("end", message + "\n")
        self.chat_display.config(state="disabled")  # Disable editing
        self.chat_display.see("end")  # Auto-scroll to the bottom

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = client_ui(root)
    root.mainloop()