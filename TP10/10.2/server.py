import socket
import threading


class ClientThread(threading.Thread):
    def __init__(self, server, client_socket: socket.socket):
        """Initialize client thread with server reference and socket."""
        super().__init__()
        self.server = server
        self.socket = client_socket

    def send(self, msg: str):
        """Send message to the client."""
        try:
            self.socket.send(msg.encode())
        except Exception as e:
            print(f"Error sending message to client: {e}")
            self.server.remove_client(self)

    def shutdown(self):
        """Shutdown the client socket."""
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print(f"Error shutting down client socket: {e}")

    def close(self):
        """Close the client socket."""
        try:
            self.socket.close()
        except Exception as e:
            print(f"Error closing client socket: {e}")

    def run(self):
        """Read messages from client continuously."""
        try:
            while True:
                msg = self.socket.recv(1024)
                if msg:
                    self.server.send_to_all(msg)
                else:
                    break
        except Exception as e:
            print(f"Error receiving message: {e}")
        finally:
            self.server.remove_client(self)
            self.close()


class Server:
    def __init__(self, port: int = 12345):
        """Initialize server with port."""
        self.port = port
        self.socket = socket.socket()
        self.clients = []

        self.socket.bind(("", self.port))
        self.socket.listen()

    def run(self):
        """Accept client connections continuously."""
        print("Server is listening for connections...")
        try:
            while True:
                client_socket, addr = self.socket.accept()
                print(f"Connection from {addr}")
                client_thread = ClientThread(self, client_socket)
                self.clients.append(client_thread)
                client_thread.start()
        except KeyboardInterrupt:
            print("\nServer stopped")
        finally:
            for client in self.clients[:]:
                client.shutdown()
                client.close()
            self.socket.close()
            print("Server closed")

    def send_to_all(self, message: bytes):
        """Send message to all connected clients."""
        disconnected_clients = []
        for client in self.clients:
            try:
                client.send(message.decode())
            except Exception:
                disconnected_clients.append(client)

        for client in disconnected_clients:
            self.remove_client(client)

    def remove_client(self, client: ClientThread):
        """Remove client from clients list."""
        if client in self.clients:
            self.clients.remove(client)


if __name__ == "__main__":
    s = Server(6060)
    s.run()
