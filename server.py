import socket
import threading

HOST = '127.0.0.1'
PORT = 5555

clients = {}  # socket -> username

valid = 'valid username'
utf8_string_valid = valid.encode('utf-8')

duplicate = 'duplicate username'
utf8_string_duplicate = duplicate.encode('utf-8')

def broadcast(message, sender_socket=None):
    """Send a message to all clients, optionally skipping the sender."""
    for client_socket in list(clients):
        if client_socket != sender_socket:
            try:
                client_socket.send(message)
            except:
                client_socket.close()
                del clients[client_socket]

def handle_client(client_socket, address):
    # First message is always the username
    try:
        username = client_socket.recv(1024).decode('utf-8').strip()
    except:
        client_socket.close()
        return
    
    user_name_status = username in clients.values()
    while(user_name_status):
        client_socket.send(utf8_string_duplicate)
        username = client_socket.recv(1024).decode('utf-8').strip()
        user_name_status = username in clients.values()

    client_socket.send(utf8_string_valid)

    clients[client_socket] = username
    print(f"[+] {username} connected from {address}")
    broadcast(f"*** {username} joined the chat ***".encode('utf-8'), sender_socket=client_socket)
    client_socket.send("Welcome! You are now connected.\n".encode('utf-8'))

    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            # Prefix every message with the sender's username
            formatted = f"{username}: {message.decode('utf-8')}".encode('utf-8')
            print(formatted.decode('utf-8'))
            broadcast(formatted, sender_socket=client_socket)
        except:
            break

    # Cleanup on disconnect
    print(f"[-] {username} disconnected")
    del clients[client_socket]
    broadcast(f"*** {username} left the chat ***".encode('utf-8'))
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Server listening on {HOST}:{PORT}")

    while True:
        client_socket, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.daemon = True
        thread.start()

start_server()