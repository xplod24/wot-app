import configparser
import PySimpleGUI as sg
import os

## CONFING FALLBACK DEFAULTS ##
default_config = """
[Connection]
main_api_uri = https://api.worldoftanks.eu
app_id = 9ec1b1d893318612477ebc6807902c3c

[RequestAPI-WG]
servers = /wgn/servers/info/
player = /wgn/account/list/

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
            
    main_api_url = configuration.get("Connection", "main_api_uri")
    app_id = configuration.get("Connection", "app_id")
    app_id = f"?application_id="+str(app_id)
    print(app_id)
    
    wgApiServers = configuration.get("RequestAPI-WG", "servers")
    wgPlayerInfo = configuration.get("RequestAPI-WG", "player")
    
    wotApiAssetsTanks = configuration.get("RequestAPI-WOT", "tankopedia-tanks-list")
    wotApiAssetsModules = configuration.get("RequestAPI-WOT", "tankopedia-consum-modules")
    
    wotApiPlayerList = configuration.get("RequestAPI-WOT", "player-list")
    wotApiPlayerInfo = configuration.get("RequestAPI-WOT", "player-data")
    wotApiPlayerTanksData = configuration.get("RequestAPI-WOT", "player-tanks-data")
    wotApiPlayerAchData = configuration.get("RequestAPI-WOT", "player-ach-data")
    wotApiPlayerClanHistory = configuration.get("RequestAPI-WOT", "player-clan-history")
    
    wotApiClanList = configuration.get("RequestAPI-WOT", "clans-list")
    wotApiClanData = configuration.get("RequestAPI-WOT", "clans-data")
    wotApiClanMembers = configuration.get("RequestAPI-WOT", "clans-members")

except Exception as e:
    print(f"Error occured: {e}")
    sg.popup(f"{e}")
    exit(0)