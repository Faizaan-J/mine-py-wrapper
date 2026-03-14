import os
import json

config_json = os.path.join("minepywrapper", "config.json")
server_properties_file = "server.properties"
config = None

def get_server_property(key: str) -> str | None:
        with open(server_properties_file, 'r') as prop_file:
            for line in prop_file:
                 key_value = line.strip().split('=')
                 if (key_value[0] == key):
                     return key_value[1]

def set_server_property(key: str, value: str):
    lines = []
    with open(server_properties_file, 'r') as prop_file:
        lines = prop_file.readlines()

    with open(server_properties_file, 'w') as prop_file:
        for line in lines:
            if line.startswith(f"{key}="):
                prop_file.write(f"{key}={value}\n")
            else:
                prop_file.write(line)

with open(config_json, 'r') as config_file:
    config = json.load(config_file)

def save_config():
    with open(config_json, 'w') as config_file:
        json.dump(config, config_file, indent=4)