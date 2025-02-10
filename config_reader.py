import configparser
import PySimpleGUI as sg
import os

from log import addLog

## CONFING FALLBACK DEFAULTS ##
default_config = """
[Connection]
main_api_wg = https://api.worldoftanks.eu
app_id_wg = ?application_id=9ec1b1d893318612477ebc6807902c3c
main_api_tomato = https://api.tomato.gg/dev/api-v2
wot_eu1_server = https://login.p1.worldoftanks.eu
wot_eu2_server = https://login.p2.worldoftanks.eu
wot_eu3_server = https://login.p3.worldoftanks.eu
wot_eu4_server = https://login.p4.worldoftanks.eu

[RequestAPI-Tomato]
player-sessions = /player/sessions/eu/
player-recents = /player/recents/eu/
player-clan-history = /player/clan-history-unofficial/EU/
player-overall-tracker = /player/overall-tracker/eu/

[RequestAPI-Hemero]

[RequestAPI-WG]
servers = /wgn/servers/info/

[RequestAPI-WOT]
player-list = /wot/account/list/
player-data = /wot/account/info/
player-tanks-data = /wot/account/tanks/
player-ach-data = /wot/account/achievements/
player-tanks-stats = /wot/tanks/stats/
player-tanks-ach = /wot/tanks/achievements/
player-clan-history = /wot/clans/memberhistory/
clans-list = /wot/clans/list/
clans-data = /wot/clans/info/
clans-members = /wot/clans/accountinfo/
tankopedia-tanks-list = /wot/encyclopedia/vehicles/
tankopedia-tank-info = /wot/encyclopedia/vehicleprofile/
tankopedia-ach = /wot/encyclopedia/achievements/
tankopedia-game-info = /wot/encyclopedia/info/
tankopedia-maps-info = /wot/encyclopedia/arenas/
tankopedia-consum-modules = /wot/encyclopedia/provisions/
tankopedia-operations = /wot/encyclopedia/personalmissions/
tankopedia-boosters = /wot/encyclopedia/boosters/
tankopedia-tanks-modules = /wot/encyclopedia/modules/
tankopedia-badges = /wot/encyclopedia/badges/
tankopedia-crewroles = /wot/encyclopedia/crewroles/
tankopedia-crewskills = /wot/encyclopedia/crewskills/
globalmap-status = /wot/globalmap/info/
globalmap-seasons = /wot/globalmap/seasons/
globalmap-season-data = /wot/globalmap/seasonclaninfo/
globalmap-season-accinfo = /wot/globalmap/seasonaccountinfo/
globalmap-events = /wot/globalmap/events/
globalmap-events-claninfo = /wot/globalmap/eventclaninfo/
globalmap-events-accinfo = /wot/globalmap/eventaccountinfo/
"""

# Define the config file path
config_file_path = "config.ini"

# Check if the config file exists
if not os.path.exists(config_file_path):
    # Create the config file
    with open(config_file_path, "w") as f:
        f.write(f"{default_config}")
    print(f"Config file created: {config_file_path}")
else:
    print(f"Config file already exists: {config_file_path}")


## CONFIGURATION LOADING ##
configuration = configparser.ConfigParser()

try:
    configuration.read('config.ini')
    print("Loading config file...")
    sections = configuration.sections()
    for section in sections:
        options = configuration.options(section)
        for option in options:
            value = configuration.get(section, option)
            print(f"{option} - {value}")
            
    wot_eu1 = configuration.get("Connection", "wot_eu1_server")
    wot_eu2 = configuration.get("Connection", "wot_eu2_server")
    wot_eu3 = configuration.get("Connection", "wot_eu3_server")
    wot_eu4 = configuration.get("Connection", "wot_eu4_server")
            
    main_api_url = configuration.get("Connection", "main_api_wg")
    app_id = configuration.get("Connection", "app_id_wg")
    main_api_tomato = configuration.get("Connection", "main_api_tomato")
    
    wgApiServers = configuration.get("RequestAPI-WG", "servers")
    
    wotApiAssetsTanks = configuration.get("RequestAPI-WOT", "tankopedia-tanks-list")
    wotApiAssetsModules = configuration.get("RequestAPI-WOT", "tankopedia-consum-modules")
    
    wotApiPlayerList = configuration.get("RequestAPI-WOT", "player-list")
    wotApiPlayerInfo = configuration.get("RequestAPI-WOT", "player-data")
    wotApiPlayerTanksData = configuration.get("RequestAPI-WOT", "player-tanks-data")
    wotApiPlayerTanksStats = configuration.get("RequestAPI-WOT", "player-tanks-stats")
    wotApiPlayerAchData = configuration.get("RequestAPI-WOT", "player-ach-data")
    wotApiPlayerClanHistory = configuration.get("RequestAPI-WOT", "player-clan-history")
    
    wotApiClanList = configuration.get("RequestAPI-WOT", "clans-list")
    wotApiClanData = configuration.get("RequestAPI-WOT", "clans-data")
    wotApiClanMembers = configuration.get("RequestAPI-WOT", "clans-members")
    
    tomatoSessions = configuration.get("RequestAPI-Tomato", "player-sessions")

except Exception as e:
    print(f"Error occured: {e}")
    sg.popup(f"{e}")
    addLog("error", f"Error in config_reader caught: {e}")
    exit(0)