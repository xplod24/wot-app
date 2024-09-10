import requests
import PySimpleGUI as sg
import json
import os
import shutil
from asset_downloader import randaa
from log import addLog
from asset_downloader import apiCaller
from app import app
from layouts import layoutfirst
import configparser

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
    assets_folder = configuration.get("Assets", "main_assets_folder")
    assets_tanks = configuration.get("Assets", "tanks_big-icons_folder")
    assets_ach = configuration.get("Assets", "achievements_folder")
    print(f"{main_api_url}, {assets_folder}, {assets_tanks}, {app_id}, {assets_ach}")
except Exception as e:
    print(f"Error occured: {e}")
    sg.popup(f"{e}")
    exit(0)



callForTanksImages = apiCaller("https://api.worldoftanks.eu/wot/encyclopedia/vehicles/?application_id=9ec1b1d893318612477ebc6807902c3c&fields=images.big_icon")
total_images = callForTanksImages[0]['meta']['total']
if os.path.isdir("./assets/tanks-big"):
    tanks_assets_count = len(os.listdir("./assets/tanks-big"))
else:
    os.makedirs("./assets/tanks-big")
    tanks_assets_count = len(os.listdir("./assets/tanks-big"))

def main():
    window = sg.Window('WOT-app Checker app for World Of Tanks @by xplod24', layoutfirst, size=(800,600), resizable=False, icon="game.ico")
    addLog("info", "Main window init...")
    while True:
        event, values = window.read(timeout=100)
        print(event, values)
        if window.is_closed() != True:
            if os.path.isdir("./assets") != True:
                window['-tank-assets-status-'].update(value="Assets folder does not exist", font="bold", text_color="cyan2")
            elif tanks_assets_count == 0:
                window['-tank-assets-status-'].update(value="Assets not downloaded", font="bold", text_color="cyan2")
            elif tanks_assets_count != total_images:
                window['-tank-assets-status-'].update(value="Incorrect amount of assets", font="bold", text_color="cyan2")
            elif tanks_assets_count == total_images:
                window['-tank-assets-status-'].update(value="Assets downloaded!", font="bold", text_color="lightgreen")
        if event == sg.WIN_CLOSED or event == 'Exit':
            addLog("info","Main window exited. App closed.")
            exit(0)
        if event == '-assets-tanks-down-':
            if os.path.isdir("./assets/tanks-big"):
                pass
            else:
                os.makedirs("./assets/tanks-big")
            addLog("info", "Button to download assets of tanks clicked")
            randaa()
        if event == '-proceed-to-app-':
            window.close()
            app()
        if event == '-assets-tanks-del-':
            addLog("info", "Button to remove folder with tanks assets clicked")
            try:
                shutil.rmtree("./assets/tanks-big")
                addLog("info", "Folder for tank assets created")
            except OSError as e:
                print(f"Error removing folder: {e}")
                addLog("error", f"{e}")
            window.refresh()

            
if __name__ == "__main__":
    addLog("info", "App init...")
    main()