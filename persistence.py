import json

AOF_FILENAME = "pyredis.aof"
WRITE_COMMANDS = {"SET", "DEL", "EXPIRE", "INCR"}

def log_command(cmd, filename=AOF_FILENAME):
    """Append one write command to the append-only file."""
    with open(filename, "a") as f:                 # "a" = append mode
        f.write(json.dumps(cmd) + "\n")            # one command per line

def load_commands(filename=AOF_FILENAME):
    """Read every logged command back, in order. Empty list if no file yet."""
    commands = []
    try:
        with open(filename) as f:
            for line in f:
                line = line.strip()
                if line:
                    commands.append(json.loads(line))
    except FileNotFoundError:
        pass                                        # no file yet = fresh start
    return commands