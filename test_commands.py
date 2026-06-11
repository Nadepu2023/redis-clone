from commands import handle_command, store

def setup_function():
    store.clear()        # pytest runs this before each test: fresh store

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
