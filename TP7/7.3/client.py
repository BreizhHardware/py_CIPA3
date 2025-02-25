import socket
import threading

def receive_messages(client_socket):
    try:
        while True:
            msg = client_socket.recv(1024)
            if msg.decode() == 'stop':
                print('Received stop signal. Closing connection.')
                break
            else:
                print(f'Message received: {msg.decode()}')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        client_socket.close()

client_socket = socket.socket()
client_socket.connect(('localhost', 12345))
client_socket.send('Coucou'.encode())

# Ask the user for messages to send
try:
    while True:
        msg = input('Message: ')
        client_socket.send(msg.encode())
        if msg == 'stop':
            break
except KeyboardInterrupt:
    print('Connection closed')
finally:
    client_socket.close()

receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()
receive_thread.join()