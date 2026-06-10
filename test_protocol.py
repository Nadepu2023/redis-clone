from protocol import parse_command, encode_simple, encode_bulk

def test_parse_ping():
    assert parse_command(b"*1\r\n$4\r\nPING\r\n") == ["PING"]

def test_parse_set_command():
    data = b"*3\r\n$3\r\nSET\r\n$4\r\nname\r\n$8\r\nniharika\r\n"
    assert parse_command(data) == ["SET", "name", "niharika"]

def test_encode_simple():
    assert encode_simple("PONG") == b"+PONG\r\n"

def test_encode_bulk_none_is_nil():
    assert encode_bulk(None) == b"$-1\r\n"