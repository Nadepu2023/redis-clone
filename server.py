import socket
from protocol import parse_command, encode_simple, encode_error

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

        if command[0].upper() == "PING":
            conn.send(encode_simple("PONG"))
        else:
            conn.send(encode_error(f"ERR unknown command '{command[0]}'"))

    print(f"Client disconnected: {addr}")