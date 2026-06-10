def parse_command(data: bytes) -> list[str]:
    """Turn b'*2\r\n$3\r\nGET\r\n$4\r\nname\r\n' into ["GET", "name"]."""
    lines = data.split(b"\r\n")          # chop into lines at each \r\n

    if not lines[0].startswith(b"*"):
        raise ValueError(f"expected array, got: {lines[0]!r}")

    count = int(lines[0][1:])            # b'*3' -> 3

    parts = []
    i = 1                                # start after the header line
    for _ in range(count):
        length_line = lines[i]           # e.g. b'$3'
        if not length_line.startswith(b"$"):
            raise ValueError(f"expected bulk string, got: {length_line!r}")
        expected_length = int(length_line[1:])

        content = lines[i + 1]           # e.g. b'SET'
        if len(content) != expected_length:
            raise ValueError("length mismatch")

        parts.append(content.decode())   # bytes -> str
        i += 2                           # move past the pair
    return parts

def encode_simple(text: str) -> bytes:
    """'PONG' -> b'+PONG\r\n'"""
    return f"+{text}\r\n".encode()
def encode_error(text: str) -> bytes: 
    """'Error' -> b'-ERR unknown command\r\n"""
    return f"-{text}\r\n".encode()
def encode_int(text: int) -> bytes:
    """'42' -> b':42\r\n"""
    return f":{text}\r\n".encode()
def encode_bulk(text: str) -> bytes:
    """'4' -> b'$4\r\nname\r\n"""
    if text is None:
        return b"$-1\r\n" 
    return f"${len(text)}\r\n{text}\r\n".encode()

