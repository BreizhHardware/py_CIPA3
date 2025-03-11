import socket
import threading


class Client:
    def __init__(self, host, port):
        """Initialize client and connect to server."""
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.running = True
        self.callback = None

    def register_callback(self, callback):
        """Register a callback function to handle received messages.

        Args:
            callback (callable): Function to call when messages are received
        """
        self.callback = callback
        # Start a thread to listen for incoming messages
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        """Listen for incoming messages and process them."""
        while self.running:
            try:
                data = self.socket.recv(1024)
                if data:
                    message = data.decode("utf-8")
                    if self.callback:
                        self.callback(message)
                else:
                    # Empty data means server closed connection
                    if self.callback:
                        self.callback("Disconnected from server\n")
                    break
            except Exception as e:
                if self.running and self.callback:  # Only show error if still running
                    self.callback(f"Error receiving message: {e}\n")
                break

    def send(self, message):
        """Send a message to the server."""
        self.socket.send(message.encode("utf-8"))

    def shutdown(self):
        """Signal the receiving thread to stop."""
        self.running = False

    def close(self):
        """Close the socket connection."""
        self.socket.close()
