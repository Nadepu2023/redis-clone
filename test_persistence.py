from persistence import log_command, load_commands
from commands import handle_command, store, expiries

def test_load_missing_file_returns_empty(tmp_path):
    aof = tmp_path / "none.aof"                  # a path that doesn't exist yet
    assert load_commands(filename=str(aof)) == []

def test_log_then_load_roundtrip(tmp_path):
    aof = tmp_path / "test.aof"
    log_command(["SET", "name", "niharika"], filename=str(aof))
    log_command(["INCR", "counter"], filename=str(aof))
    assert load_commands(filename=str(aof)) == [
        ["SET", "name", "niharika"],
        ["INCR", "counter"],
    ]

def test_replay_rebuilds_state(tmp_path):
    aof = tmp_path / "test.aof"
    log_command(["SET", "name", "niharika"], filename=str(aof))
    log_command(["INCR", "hits"], filename=str(aof))
    store.clear()
    for cmd in load_commands(filename=str(aof)):
        handle_command(cmd)
    assert store["name"] == "niharika"
    assert store["hits"] == "1"
    