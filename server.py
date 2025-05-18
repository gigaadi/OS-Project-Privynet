import socket
import threading
import os
import json

HOST = '192.168.16.147'
PORT = 5001

# Load users and roles
with open('users.json', 'r') as f:
    USERS = json.load(f)

def handle_client(client_socket, address):
    print(f"[CONNECTED] Client {address} connected.")
    try:
        # Receive authentication
        data = client_socket.recv(1024).decode()
        print("Received:", data)
        parts = data.strip().split("::")

        if len(parts) != 2:
            client_socket.send("Invalid authentication format.".encode())
            client_socket.close()
            return

        username, password = parts
        user_info = USERS.get(username)

        if user_info and user_info["password"] == password:
            role = user_info["role"]
            client_socket.send(f"Authentication successful::{role}".encode())
        else:
            client_socket.send("Authentication failed".encode())
            client_socket.close()
            return

        # Handle commands
        while True:
            data = client_socket.recv(2048).decode()
            if not data:
                break

            print(f"[COMMAND FROM {address}] {data}")
            parts = data.split("::")
            command = parts[0]

            if command == "LIST":
                files = os.listdir('.')
                client_socket.send(', '.join(files).encode())

            elif command == "CREATE":
                if role != "admin":
                    client_socket.send("Permission denied: only admin can create files.".encode())
                    continue
                if len(parts) >= 3:
                    filename = parts[1]
                    content = "::".join(parts[2:])
                    with open(filename, 'w') as f:
                        f.write(content)
                    client_socket.send(f"File '{filename}' created.".encode())
                else:
                    client_socket.send("Invalid CREATE command.".encode())

            elif command == "READ":
                if len(parts) == 2:
                    filename = parts[1]
                    if os.path.exists(filename):
                        with open(filename, 'r') as f:
                            content = f.read()
                        client_socket.send(content.encode())
                    else:
                        client_socket.send("File not found.".encode())
                else:
                    client_socket.send("Invalid READ command.".encode())

            elif command == "DELETE":
                if role != "admin":
                    client_socket.send("Permission denied: only admin can delete files.".encode())
                    continue
                if len(parts) == 2:
                    filename = parts[1]
                    if os.path.exists(filename):
                        os.remove(filename)
                        client_socket.send(f"File '{filename}' deleted.".encode())
                    else:
                        client_socket.send("File not found.".encode())
                else:
                    client_socket.send("Invalid DELETE command.".encode())

            else:
                client_socket.send("Unknown command.".encode())

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        print(f"[DISCONNECTED] Client {address} disconnected.")
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[SERVER STARTED] Listening on {HOST}:{PORT}")

    while True:
        client_socket, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()

if __name__ == "__main__":
    start_server()
