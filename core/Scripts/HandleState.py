import re
from enum import Enum

from Events import Event

# I used chatgpt for these regex statements: 
# "[HH:MM:SS] [Thread/Level]:"
LOG_PREFIX = re.compile(r"^\[\d{2}:\d{2}:\d{2}\] \[[^\]]+\]: ")
# "Playername joined the game"
PLAYER_JOINED_REGEX = r"^[^\s]+ joined the game"

class State(Enum):
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    IDLE = "idle"

def strip_prefix(line: str) -> str:
    return LOG_PREFIX.sub("", line, count=1)

state: State = State.STARTING

OnStateChange = Event("OnStateChange")

def update_state_from_line(line: str):
    msg = strip_prefix(line)

    state_table = {
        msg.startswith("Done ("): State.RUNNING,
        msg.startswith("Stopping the server"): State.STOPPING,
        msg.startswith("Server empty for 60 seconds, pausing"): State.IDLE,
        re.match(PLAYER_JOINED_REGEX, msg): State.RUNNING
    }

    new_state = None
    for condition in state_table:
        new_state_value = state_table[condition]
        if condition:
            new_state = new_state_value
            break

    set_state(new_state)

def set_state(new_state: State | None):
    global state
    if new_state != state and new_state is not None:
        state = new_state
        OnStateChange.invoke_event(state)