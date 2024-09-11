import requests
import PySimpleGUI as sg
import json
import os
import shutil
from asset_downloader import randaa
from log import addLog
from app import app
from layouts import layoutfirst
from config_reader import *

callForTanksImages = "" ## TO DO api call to get tanks images
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