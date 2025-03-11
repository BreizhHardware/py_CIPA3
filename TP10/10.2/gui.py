import tkinter as tk
from tkinter import ttk
from client import Client
import datetime


class ClientWindow:
    def __init__(self, root: tk.Tk):
        """Initialize the chat window."""
        self.root = root
        self.root.title("Chat Client")
        self.root.geometry("600x400")

        self.client = None

        # Server connection fields
        self.address = tk.StringVar(value="localhost")
        self.port = tk.StringVar(value="6060")

        # Address field
        address_label = ttk.Label(root, text="Address:")
        address_label.grid(column=0, row=0, padx=5, pady=5)
        address_entry = ttk.Entry(root, textvariable=self.address)
        address_entry.grid(column=1, row=0, padx=5, pady=5)

        # Port field
        port_label = ttk.Label(root, text="Port:")
        port_label.grid(column=2, row=0, padx=5, pady=5)
        port_entry = ttk.Entry(root, textvariable=self.port)
        port_entry.grid(column=3, row=0, padx=5, pady=5)

        # Connect button
        self.connect_button = ttk.Button(root, text="Connect", command=self.connect)
        self.connect_button.grid(column=4, row=0, padx=5, pady=5)

        # Messages display
        self.text_area = tk.Text(root, wrap=tk.WORD, width=50, height=20)
        self.text_area.grid(column=0, row=1, columnspan=5, padx=5, pady=5)
        self.text_area.config(state="disabled")

        # Message input
        self.message = tk.StringVar()
        self.msg_entry = ttk.Entry(root, textvariable=self.message)
        self.msg_entry.grid(column=0, row=2, columnspan=5, padx=5, pady=5, sticky="ew")
        self.msg_entry.bind("<Return>", self.send)

        # Configure grid weights
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

    def connect(self):
        """Connect to the server."""
        try:
            self.client = Client(self.address.get(), int(self.port.get()))
            if self.client:  # Only register callback if client is created successfully
                self.client.register_callback(self.append_text)
                self.connect_button["text"] = "Disconnect"
                self.connect_button["command"] = self.disconnect
                self.append_text("Connected to server\n")
        except Exception as e:
            self.append_text(f"Connection error: {e}\n")
            self.client = None  # Reset client on failed connection

    def disconnect(self):
        """Disconnect from the server."""
        if self.client:
            self.client.shutdown()
            self.client.close()
            self.client = None
            self.connect_button["text"] = "Connect"
            self.connect_button["command"] = self.connect
            self.append_text("Disconnected from server\n")

    def send(self, event=None):
        """Send message to server."""
        if self.client and self.message.get():
            try:
                self.client.send(self.message.get())
                self.message.set("")  # Clear input field
            except Exception as e:
                self.append_text(f"Error sending message: {e}\n")

    def append_text(self, message: str):
        """Append text to message display area with timestamp."""
        self.text_area.config(state="normal")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Ensure the message ends with a newline
        if not message.endswith("\n"):
            message += "\n"

        # Add timestamp and ensure double line break between messages
        formatted_message = f"[{timestamp}] {message}\n"

        self.text_area.insert("end", formatted_message)
        self.text_area.see("end")
        self.text_area.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    ClientWindow(root)
    root.mainloop()
