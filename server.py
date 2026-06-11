import socket
from protocol import parse_command
from commands import handle_command

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", 6379)) 

server.listen()
print("Listening on port 6379...")

while True:
    conn, addr = server.accept()
    print(f"Client connected: {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        command = parse_command(data)
        print(f"Parsed command: {command}")
        conn.send(handle_command(command))

    print(f"Client disconnected: {addr}")