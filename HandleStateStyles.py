import ConfigHandler
import HandleState

import os
from ColorMap import color_map

def set_title(title: str):
    os.system(f"title {title}")

def set_color(color_name: str):
    color_code = color_map.get(color_name, color_map["darkgray"])
    os.system(f"color {color_code}")

def auto_generate():
    jar_name = ConfigHandler.config["server"]["jar_name"]
    template = {
        "starting": {
            "title": f"Starting {jar_name}",
            "color": "yellow"
        },
        "running": {
            "title": f"Running {jar_name}",
            "color": "green"
        },
        "stopping": {
            "title": f"Stopping {jar_name}",
            "color": "red"
        },
        "stopped": {
            "title": f"Stopped {jar_name}",
            "color": "darkgray"
        }
    }
    return template

def on_state_change(new_state: HandleState.State):
    state_styles = ConfigHandler.config["state_styles"].get("styles", auto_generate())
    title_enabled = ConfigHandler.config["state_styles"]["feature_enabled"]["title"].get("enabled", True)
    color_enabled = ConfigHandler.config["state_styles"]["feature_enabled"]["color"].get("enabled", True)

    if title_enabled:
        set_title(state_styles[new_state.value]["title"])
    if color_enabled:
        set_color(state_styles[new_state.value]["color"])

feature_enabled = ConfigHandler.config["state_styles"]["feature_enabled"].get("enabled", True)
if feature_enabled:
    HandleState.OnStateChange.subscribe(on_state_change)
    on_state_change(HandleState.state)