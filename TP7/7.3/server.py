import socket
import threading

clients = []

def send_to_all(clients, message):
    for client in clients:
        try:
            client.send(message)
        except Exception as e:
            print(f'Error sending message to a client: {e}')
            clients.remove(client)

def client_thread(client_socket, clients):
    try:
        while True:
            msg = client_socket.recv(1024)
            if msg:
                print(f'Message received: {msg.decode()}')
                send_to_all(clients, msg)
            else:
                break
    except Exception as e:
        print(f'Error: {e}')
    finally:
        client_socket.close()
        clients.remove(client_socket)

server_socket = socket.socket()
server_socket.bind(('', 12345))
server_socket.listen()

print('Server is listening for connections...')

try:
    while True:
        client_socket, addr = server_socket.accept()
        print(f'Connection from {addr}')
        clients.append(client_socket)
        thread = threading.Thread(target=client_thread, args=(client_socket, clients))
        thread.start()
except KeyboardInterrupt:
    print('Server stopped')
finally:
    for client in clients:
        try:
            client.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print(f'Error shutting down client socket: {e}')
        client.close()
    server_socket.close()
    print('Server closed')