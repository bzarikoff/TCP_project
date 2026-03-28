import socket
import threading

HOST = '127.0.0.1'
PORT = 5555

def receive_messages(client_socket):
    """Runs in background — prints messages as they arrive."""
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
    print(f"Connected to {HOST}:{PORT}. Start typing!")

    # Receive messages in the background while we wait for user input
    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True
    thread.start()

    while True:
        message = input()   # blocks waiting for you to type
        if message.lower() == 'quit':
            break
        client.send(message.encode('utf-8'))

    client.close()

start_client()