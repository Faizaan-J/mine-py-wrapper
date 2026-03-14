import os
import json
from mcipc.query import Client
from mcipc.rcon.je import Client as RconClient

import ConfigHandler
import HandleState

import threading

import Logger

from time import sleep as wait                

# will be improved later
def handle_sneaky_ban():
    sneaky_banned_players = ConfigHandler.config["sneaky_bans"]["players"]
    # ip bans implemented later if needed
    QUERY_PORT = int(ConfigHandler.get_server_property("query.port"))
    RCON_PORT = int(ConfigHandler.get_server_property("rcon.port"))
    RCON_PASSWORD = ConfigHandler.get_server_property("rcon.password")

    def run():
        try: # when the server closes this errors sometimes cuz its in the middle of running before it can check Handle.state and the server
            # stopped so we just ignore it
            while HandleState.state == HandleState.State.RUNNING:
                wait(4)
                with Client("127.0.0.1", QUERY_PORT) as query:
                    players = query.stats(True).players
                    for player in sneaky_banned_players:
                        if player in players:
                            try:
                                with RconClient("127.0.0.1", RCON_PORT) as rcon:
                                    rcon.login(RCON_PASSWORD)
                                    rcon.run(f"kick {player} Connection timed out: getsockopt\n") # This is an outright fabrication. 
                                    # They think it's an error but its lowkey a ban
                            except Exception as e:
                                Logger.Log(Logger.LogLevel.ERROR, f"Sneaky ban error for {player}: {e}")
        except:
            pass
    threading.Thread(target=run, daemon=True).start()

feature_enabled = ConfigHandler.config["sneaky_bans"].get("feature_enabled", False)
if feature_enabled:
    handle_sneaky_ban()