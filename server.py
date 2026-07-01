import asyncio
from protocol import parse_command
from commands import handle_command

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"Client connected: {addr}")
    while True:
        data = await reader.read(1024)      # PAUSE here until bytes arrive
        if not data:
            break
        command = parse_command(data)
        print(f"{addr} -> {command}")
        writer.write(handle_command(command))
        await writer.drain()                # PAUSE until the reply is sent
    writer.close()
    print(f"Client disconnected: {addr}")

async def main():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 6379)
    print("Listening on port 6379...")
    async with server:
        await server.serve_forever()

asyncio.run(main())