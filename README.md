# PyRedis

A Redis clone built from scratch in Python. Implements the RESP protocol over raw TCP sockets, handles concurrent clients with asyncio, and persists data to disk using an append-only log.

## Features

- Concurrent client connections via Python's asyncio event loop
- RESP protocol parser and encoder written from scratch
- In-memory key-value store
- Key expiry with both lazy deletion and a background sweeper
- Append-only file (AOF) persistence — write commands are logged to disk and replayed on startup

## Supported commands

| Command | Example | Description |
|---------|---------|-------------|
| PING | `PING` | Returns PONG |
| SET | `SET name niharika` | Stores a value |
| GET | `GET name` | Retrieves a value, or nil if the key is missing or expired |
| DEL | `DEL key1 key2` | Deletes one or more keys, returns count removed |
| EXISTS | `EXISTS name` | Returns 1 if the key exists, 0 if not |
| INCR | `INCR counter` | Increments a numeric value by 1, starts from 0 if missing |
| EXPIRE | `EXPIRE name 60` | Sets a TTL in seconds on a key |
| TTL | `TTL name` | Returns seconds remaining, -1 if no expiry, -2 if key missing |

## Getting started

Start the server:
```
python3 server.py
```

Connect with redis-cli in a second terminal:
```
redis-cli
```

## Project structure

```
server.py          — asyncio TCP server, AOF logging
commands.py        — command dispatcher, in-memory store, expiry logic
protocol.py        — RESP parser and encoders
persistence.py     — append-only file logging and replay
client.py          — minimal test client for manual testing
test_protocol.py   — tests for the RESP parser and encoders
test_commands.py   — tests for command handling and expiry
test_persistence.py — tests for AOF logging and replay
```

## Running tests

```
pytest
```

