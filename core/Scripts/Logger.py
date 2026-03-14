import datetime
from enum import Enum

import inspect

prefix = "MinePyWrapper"

class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

def Log(level: LogLevel, *args):
    stack = inspect.stack()
    caller = stack[1]
    filename = caller.filename.split("/")[-1].split("\\")[-1]
    line_number = caller.lineno

    now = datetime.datetime.now()
    timestamp = now.strftime("%H:%M:%S").zfill(8)
    print(f"[{timestamp}] [{prefix}/{level.value}] [{filename}:{line_number}] {' '.join(str(arg) for arg in args)}")

Log(LogLevel.INFO, "Logger initialized", "Combined message test", 6, 7)