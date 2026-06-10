import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 6379))

# This is exactly what redis-cli sends for the command: PING
client.send(b"*1\r\n$4\r\nPING\r\n")

reply = client.recv(1024)
print(f"Server replied: {reply!r}")
client.close()