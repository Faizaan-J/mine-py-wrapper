import subprocess
import os
from dotenv import load_dotenv
import ConfigHandler
import threading

from ColorMap import color_map

import Logger
from Events import Event

import HandleState
import HandleSneakyBans
import HandleStateStyles
import HandleServerResourcePack

load_dotenv()

script_dir = os.path.dirname(os.path.abspath(__file__))
jar_path = os.path.join(script_dir, "..", f"{ConfigHandler.config['server']['jar_name']}.jar")

java_args = [
    "java",
    f"-Xms{ConfigHandler.config['server']['min_ram']}",
    f"-Xmx{ConfigHandler.config['server']['max_ram']}",
]

if "other_args" in ConfigHandler.config['server']:
    java_args.extend(ConfigHandler.config['server']['other_args'])

java_args.extend([
    "-jar", jar_path, "nogui"
])

server_process = subprocess.Popen(
    java_args,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    encoding="utf-8",
    errors="replace"
)

for line in server_process.stdout:
    print(line, end='')
    HandleState.update_state_from_line(line)

server_process.wait()
HandleState.set_state(HandleState.State.STOPPED)

Logger.Log(Logger.LogLevel.INFO, "Server process stopped!")
# It pauses in bat file