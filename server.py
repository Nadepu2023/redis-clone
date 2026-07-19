import asyncio
import time
from protocol import parse_command
from commands import handle_command
from commands import store, expiries
from commands import handle_command
from persistence import log_command, load_commands, WRITE_COMMANDS

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    while True:
        data = await reader.read(1024)
        if not data:
            break
        command = parse_command(data)
        reply = handle_command(command)
        # log successful writes to disk
        if command[0].upper() in WRITE_COMMANDS and not reply.startswith(b"-"):
            log_command(command)
        writer.write(reply)
        await writer.drain()
    writer.close()

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"Client connected: {addr}")
    while True:
        #pauses here until bytes arrive
        data = await reader.read(1024)      
        if not data:
            break
        command = parse_command(data)
        print(f"{addr} -> {command}")
        writer.write(handle_command(command))
        #pauses here until the reply is sent
        await writer.drain()                
    writer.close()
    print(f"Client disconnected: {addr}")

async def main():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 6379)
    print("Listening on port 6379...")
    asyncio.create_task(expiry_sweeper()) 
    async with server:
        await server.serve_forever()

async def expiry_sweeper():
    while True:
        await asyncio.sleep(1)
        now = time.time()
        expired = [k for k, deadline in expiries.items() if now > deadline]
        for key in expired:
            store.pop(key, None)
            expiries.pop(key, None)


asyncio.run(main())