import requests
import PySimpleGUI as sg
import json
import os
import shutil
from asset_downloader import randaa
from log import addLog
from asset_downloader import apiCaller
from app import app

            
callForTanksImages = apiCaller("https://api.worldoftanks.eu/wot/encyclopedia/vehicles/?application_id=9ec1b1d893318612477ebc6807902c3c&fields=images.big_icon")
total_images = callForTanksImages[0]['meta']['total']
if os.path.isdir("./assets/tanks-big"):
    tanks_assets_count = len(os.listdir("./assets/tanks-big"))
else:
    os.makedirs("./assets/tanks-big")
    tanks_assets_count = len(os.listdir("./assets/tanks-big"))
    
layoutfirst = [
    [sg.Push(), sg.Text("Hello!"),sg.Push()],
    [sg.Push(), sg.Text("Thanks for downloading my app!"), sg.Push()],
    [sg.Push(), sg.Text("This app needs assets in order to function properly"), sg.Push()],
    [sg.Push(), sg.Text("Buttons below will tell you if you need to update folders with assets"), sg.Push()],
    [sg.Push(),sg.Column([[sg.Text("Tanks assets")],[sg.Text("Modules assets")],[sg.Text("Player stats assets")]]), 
            sg.Column([[sg.Text("Refresh to update status", k='-tank-assets-status-')], [sg.Text("Refresh to update status", k='-modules-assets-status-')], [sg.Text("Refresh to update status", k='-player-assets-status-')]]),
            sg.Column([[sg.Button("Download", k='-assets-tanks-down-'), sg.Button("Delete", k='-assets-tanks-del-'), sg.Button("Check", k='-assets-tanks-ref-')], 
                       [sg.Button("Download", k='-modules-assets-down-'), sg.Button("Delete", k='-modules-assets-del-'), sg.Button("Check", k='-modules-assets-ref-')], 
                       [sg.Button("Download", k='-player-assets-down-'), sg.Button("Delete", k='-player-assets-del-'), sg.Button("Check", k='-player-assets-ref-')]]),sg.Push(),],
    [sg.VPush()],
    [sg.Text("Current news:", font="bold")],
    [sg.Text("Login will be available soon, this will only add ability to see private info.")],
    [sg.Push(),sg.Button("Login", k='-login-button-', disabled=True), sg.Button("Proceed to app", k='-proceed-to-app-'),sg.Push()]
]

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