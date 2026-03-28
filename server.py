import socket
import threading

HOST = '127.0.0.1'  # localhost — only your machine can connect
PORT = 5555         # any unused port above 1024 works

# Keep track of every connected client
clients = []

def broadcast(message, sender_socket):
    """Send a message to every client except the one who sent it."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                # Client disconnected — remove them
                clients.remove(client)

def handle_client(client_socket, address):
    """Runs in its own thread for each connected client."""
    print(f"[+] New connection from {address}")
    
    while True:
        try:
            message = client_socket.recv(1024)  # receive up to 1024 bytes
            if not message:
                break  # client disconnected cleanly
            print(f"[{address}] {message.decode('utf-8')}")
            broadcast(message, client_socket)
        except:
            break  # client disconnected unexpectedly

    print(f"[-] {address} disconnected")
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    # AF_INET = IPv4, SOCK_STREAM = TCP (vs SOCK_DGRAM for UDP)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allows reusing the port immediately after restart
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server.bind((HOST, PORT))   # claim the address + port
    server.listen(5)            # queue up to 5 pending connections
    print(f"[*] Server listening on {HOST}:{PORT}")

    while True:
        client_socket, address = server.accept()  # blocks until someone connects
        clients.append(client_socket)
        
        # Each client gets its own thread so they don't block each other
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.daemon = True
        thread.start()

start_server()