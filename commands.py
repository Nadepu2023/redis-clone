from protocol import encode_simple, encode_error, encode_int, encode_bulk
import threading
import time

store = {}
expiries = {} 
store_lock = threading.Lock()

def handle_command(cmd: list[str]) -> bytes:
    name = cmd[0].upper()

    if name == "PING":
        return encode_simple("PONG")

    elif name == "SET":
        if len(cmd) != 3:
            return encode_error("ERR wrong number of arguments for 'set'")
        store[cmd[1]] = cmd[2]
        return encode_simple("OK")

    elif name == "GET":
        if len(cmd) != 2:
            return encode_error("ERR wrong number of arguments for 'get'")
        check_expired(cmd[1])
        return encode_bulk(store.get(cmd[1]))   # None -> $-1 nil, handled by your encoder

    elif name == "DEL":
        deleted = 0
        for key in cmd[1:]:
            if store.pop(key, None) is not None:
                deleted += 1
        return encode_int(deleted)
    
    elif name == "EXISTS":
        if len(cmd) != 2:
            return encode_error("ERR wrong number of arguments for 'exists'")
        return encode_int(1 if cmd[1] in store else 0)

    elif name == "INCR":
        if len(cmd) != 2:
            return encode_error("ERR wrong number of arguments for 'incr'")
        key = cmd[1]
        current = store.get(key, "0")        
        try:
            new_value = int(current) + 1     
        except ValueError:                   
            return encode_error("ERR value is not an integer or out of range")
        store[key] = str(new_value)          
        return encode_int(new_value)
    
    elif name == "EXPIRE":
        if len(cmd) != 3:
            return encode_error("ERR wrong number of arguments for 'expire'")
        key = cmd[1]
        if key not in store:
            return encode_int(0)
        seconds = int(cmd[2])
        expiries[key] = time.time() + seconds
        return encode_int(1)
    
    elif name == "TTL":
        if len(cmd) != 2:
            return encode_error("ERR wrong number of arguments for 'ttl'")
        key = cmd[1]
        if key not in store:
            return encode_int(-2)               
        if key not in expiries:
            return encode_int(-1)                 
        remaining = expiries[key] - time.time()
        return encode_int(int(remaining))

    else:
        return encode_error(f"ERR unknown command '{cmd[0]}'")
    
def check_expired(key):
    """If the key has a deadline and it's passed, delete it. Return True if it was expired."""
    if key in expiries and time.time() > expiries[key]:
        store.pop(key, None)
        expiries.pop(key, None)
        return True
    return False