import socket
import threading
from protocol import parse_command
from commands import handle_command, store_lock

def handle_client(conn, addr):
    print(f"Client connected: {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        command = parse_command(data)
        print(f"{addr} -> {command}")
        with store_lock:
            reply = handle_command(command)
        conn.send(reply)
    conn.close()
    print(f"Client disconnected: {addr}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 6379))
    server.listen()
    print("Listening on port 6379...")

    while True:                                  # forever:
        conn, addr = server.accept()             #   wait for the next client
        thread = threading.Thread(
            target=handle_client,                #   give them a personal waiter
            args=(conn, addr),
            daemon=True,                         #   don't block shutdown
        )
        thread.start()                           #   and immediately go wait again

main()