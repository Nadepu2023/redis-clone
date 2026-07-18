import time
from commands import handle_command, store, expiries

def setup_function():
    store.clear()     
    expiries.clear()   # pytest runs this before each test: fresh store

def test_set_then_get():
    handle_command(["SET", "name", "niharika"])
    assert handle_command(["GET", "name"]) == b"$8\r\nniharika\r\n"

def test_get_missing_key_returns_nil():
    assert handle_command(["GET", "ghost"]) == b"$-1\r\n"

def test_del_counts_only_existing_keys():
    handle_command(["SET", "a", "1"])
    assert handle_command(["DEL", "a", "b"]) == b":1\r\n"

def test_incr_missing_key_starts_at_one():
    assert handle_command(["INCR", "visits"]) == b":1\r\n"

def test_incr_existing_number():
    handle_command(["SET", "visits", "5"])
    assert handle_command(["INCR", "visits"]) == b":6\r\n"

def test_incr_non_numeric_is_error():
    handle_command(["SET", "niharika", "notanumber"])
    assert handle_command(["INCR", "niharika"]) == b"-ERR value is not an integer or out of range\r\n"

def test_exists_when_key_present():
    handle_command(["SET", "name", "niharika"])
    assert handle_command(["EXISTS", "name"]) == b":1\r\n"

def test_exists_when_key_absent():
    assert handle_command(["EXISTS", "ghost"]) == b":0\r\n"

def test_ttl_missing_key_is_negative_two():
    assert handle_command(["TTL", "ghost"]) == b":-2\r\n"

def test_ttl_key_without_expiry_is_negative_one():
    handle_command(["SET", "name", "niharika"])
    assert handle_command(["TTL", "name"]) == b":-1\r\n"

def test_expire_sets_a_ttl():
    handle_command(["SET", "name", "niharika"])
    handle_command(["EXPIRE", "name", "100"])
    # TTL should now be close to 100 (99 or 100 depending on timing)
    reply = handle_command(["TTL", "name"])
    assert reply in (b":100\r\n", b":99\r\n")

def test_expired_key_reads_as_gone():
    handle_command(["SET", "name", "niharika"])
    expiries["name"] = time.time() - 1        
    assert handle_command(["GET", "name"]) == b"$-1\r\n"   

def test_expire_on_missing_key_returns_zero():
    assert handle_command(["EXPIRE", "ghost", "100"]) == b":0\r\n"

def test_expire_wrong_args_is_error():
    assert handle_command(["EXPIRE", "ghost"]) == b"-ERR wrong number of arguments for 'expire'\r\n"
