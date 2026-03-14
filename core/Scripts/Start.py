import subprocess
import os
import sys

from ColorMap import color_map
from Events import Event
import Logger

import argparse
parser = argparse.ArgumentParser(description="Start the Minecraft server.")
parser.add_argument("--server-dir", required=True, help="Path to the server directory.", default=os.getcwd())

args = parser.parse_args()
server_dir = os.path.abspath(args.server_dir)
if not os.path.isdir(server_dir):
    Logger.Log(Logger.LogLevel.ERROR, f"Provided server directory does not exist: {server_dir}")
    sys.exit(1)

os.chdir(server_dir)

# IMPORT MODULES
import subprocess
from dotenv import load_dotenv
load_dotenv()
import ConfigHandler
import threading

import HandleState
import HandleSneakyBans
import HandleStateStyles
import HandleServerResourcePack

def main():
    jar_path = f"{ConfigHandler.config['server']['jar_name']}.jar"

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

if __name__ == "__main__":
    main()