import socket
import threading


class Client:
    def __init__(self, server_address: str, server_port: int):
        """Initialize client with server address and port."""
        self.server_address = server_address
        self.server_port = server_port
        self.socket = socket.socket()
        self.running = True
        self.callbacks = []  # List of callback functions for received messages

        try:
            self.socket.connect((self.server_address, self.server_port))
            self.listening_thread = threading.Thread(target=self.listen_messages)
            self.listening_thread.start()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to server: {e}")

    def send(self, msg: str):
        """Send a message to the server."""
        try:
            self.socket.send(msg.encode())
        except Exception as e:
            print(f"Error sending message: {e}")
            self.running = False
            raise e

    def shutdown(self):
        """Shutdown the socket communication."""
        try:
            self.running = False
            self.socket.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print(f"Error during shutdown: {e}")

    def close(self):
        """Close the connection and wait for listening thread to end."""
        if hasattr(self, "listening_thread"):
            self.listening_thread.join()
        try:
            self.socket.close()
        except Exception as e:
            print(f"Error closing socket: {e}")

    def register_callback(self, callback):
        """Register a callback function for received messages."""
        self.callbacks.append(callback)

    def listen_messages(self):
        """Listen for incoming messages from the server."""
        while self.running:
            try:
                msg = self.socket.recv(1024)
                if msg:
                    decoded_msg = msg.decode()
                    # Notify all registered callbacks
                    for callback in self.callbacks:
                        callback(f"{decoded_msg}\n")
                else:
                    break
            except Exception as e:
                if self.running:  # Only print error if not shutting down
                    print(f"Error receiving message: {e}")
                break
        self.running = False


def main():
    """Test client in console mode."""
    client = Client("localhost", 6060)

    def print_message(msg: str):
        """Simple callback to print received messages."""
        print(f"Received: {msg}", end="")

    client.register_callback(print_message)

    try:
        while client.running:
            message = input("Enter message (or Ctrl+C to quit): ")
            client.send(message)
            if message.lower() == "quit":
                break
    except KeyboardInterrupt:
        print("\nClosing connection...")
    finally:
        client.shutdown()
        client.close()


if __name__ == "__main__":
    main()
