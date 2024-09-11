import configparser
import PySimpleGUI as sg

## CONFIGURATION LOADING ##
configuration = configparser.ConfigParser()

try:
    configuration.read('config.ini')
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
    
    assets_folder = configuration.get("Assets", "main_assets_folder")
    assets_tanks = configuration.get("Assets", "tanks_big-icons_folder")
    assets_ach = configuration.get("Assets", "achievements_folder")
    
    wgApiServers = configuration.get("RequestAPI-WG", "servers")
    wgPlayerInfo = configuration.get("RequestAPI-WG", "player")
    
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