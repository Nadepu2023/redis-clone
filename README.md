# PyRedis

A Redis clone built from scratch in Python, using raw TCP sockets and the RESP protocol.

## What it does

- Accepts multiple simultaneous client connections using Python's asyncio event loop
- Parses and responds to Redis commands using the RESP (Redis Serialization Protocol)
- Stores key-value data in memory

## Supported commands

| Command | Example | Description |
|---------|---------|-------------|
| PING | `PING` | Returns PONG |
| SET | `SET name niharika` | Stores a value |
| GET | `GET name` | Retrieves a value, or nil if missing |
| DEL | `DEL name age` | Deletes one or more keys, returns count deleted |
| EXISTS | `EXISTS name` | Returns 1 if key exists, 0 if not |
| INCR | `INCR counter` | Increments a numeric value by 1 |

## How to run

Start the server:
```
python3 server.py
```

Connect with redis-cli in a second terminal:
```
redis-cli
```

## Project structure

- `server.py` — TCP server using asyncio, handles multiple clients concurrently
- `commands.py` — command dispatcher and in-memory key-value store
- `protocol.py` — RESP parser and encoders
- `client.py` — simple test client for manual protocol testing
- `test_protocol.py` — pytest suite for the RESP parser and encoders
- `test_commands.py` — pytest suite for command handling

## Running tests

```
pytest test_protocol.py
pytest test_commands.py
```

---

This is a work in progress.
