import configparser
import json
import PySimpleGUI as sg
import os

from log import addLog

## CONFING FALLBACK DEFAULTS ##
default_config = {
    "globals" : {
        "always_download_update" : False
    },
    "init" : {
        "nickname_always_searched" : None,
        "clan_always_searched": None    
    },
    "others" : {
        
    }
}

# Define the config file path
settings_file_path = "settings.json"

# Check if the config file exists
if not os.path.exists(settings_file_path):
    # Create the config file
    with open(settings_file_path, "w") as f:
        f.write(f"{default_config}")
    print(f"Config file created: {settings_file_path}")
else:
    print(f"Config file already exists: {settings_file_path}")


try:
    settings = json.loads(settings_file_path)
    always_download = settings["globals"]["always_download_update"]
    init_nick = settings["init"]["nickname_always_searched"]
    init_clan = settings["init"]["clan_always_searched"]

except Exception as e:
    print(f"Error occured: {e}")
    sg.popup(f"{e}")
    addLog("error", f"Error in config_reader caught: {e}")
    exit(0)