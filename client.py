import socket
import threading

HOST = '127.0.0.1'
PORT = 5555

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Disconnected from server.")
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Ask for username before anything else
    valid_username = False

    while(valid_username != True):
        username = input("Enter your username: ").strip()
        client.send(username.encode('utf-8'))

        message = client.recv(1024).decode('utf-8')
        print(message)

        if(message == 'valid username'):
            valid_username = True

    # Now start listening for incoming messages in the background
    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True
    thread.start()

    while True:
        message = input()
        if message.lower() == 'quit':
            break
        client.send(message.encode('utf-8'))

    client.close()

start_client()