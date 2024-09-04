import requests
import PySimpleGUI as sg
import json
import os
import shutil
from asset_downloader import randaa
from log import addLog
from asset_downloader import apiCaller
from app import app

def tank_assets(whatToDo):
    
    """This method allows to control assets of tanks (icons, etc.)

    Args:
        whatToDo (string): Only exact strings are allowed:
        Delete - Deletes whole assets folder
        Refresh - FIrst deletes whole folder, then redownloads all assets
    """
    
    if whatToDo == "Delete":
        try:
            shutil.rmtree("./assets")
            addLog("info", "Folder for tank assets created")
        except OSError as e:
            print(f"Error removing folder: {e}")
            addLog("error", f"{e}")
            

callForImages = apiCaller("https://api.worldoftanks.eu/wot/encyclopedia/vehicles/?application_id=9ec1b1d893318612477ebc6807902c3c&fields=images.big_icon&page_no=1")
total_images = callForImages[0]['meta']['total']

layoutfirst = [
    [sg.Push(), sg.Text("Hello!"),sg.Push()],
    [sg.Push(), sg.Text("Thanks for downloading my app!"), sg.Push()],
    [sg.Push(), sg.Text("This app needs assets in order to function properly"), sg.Push()],
    [sg.Push(), sg.Text("Buttons below will tell you if you need to update folders with assets"), sg.Push()],
    [sg.Push(), sg.Text("Tanks assets"), sg.Push(), sg.Text("Refresh to update status", k='-tank-assets-status-') ,sg.Push(), sg.Button("Download", k='-assets-tanks-down-'), sg.Button("Delete", k='-assets-tanks-del-'), sg.Button("Check", k='-assets-tanks-ref-'), sg.Push()],
    [sg.VPush()],
    [sg.Push(),sg.Button("Proceed"),sg.Push()]
]

def main():
    window = sg.Window('WOT-app Checker app for World Of Tanks @by xplod24', layoutfirst, size=(800,600), resizable=False, icon="game.ico")
    addLog("info", "Main window init...")
    while True:
        event, values = window.read(timeout=500)
        print(event, values)
        if window.is_closed() != True:
            if os.path.isdir("./assets") != True:
                window['-tank-assets-status-'].update(value="Folder does not exist", font="bold", text_color="cyan2")
            elif len(os.listdir("./assets")) == 0:
                window['-tank-assets-status-'].update(value="Assets not downloaded", font="bold", text_color="cyan2")
            elif len(os.listdir("./assets")) != total_images:
                window['-tank-assets-status-'].update(value="Incorrect amount of assets", font="bold", text_color="cyan2")
            elif len(os.listdir("./assets")) == total_images:
                window['-tank-assets-status-'].update(value="Assets downloaded!", font="bold", text_color="lightgreen")
        if event == sg.WIN_CLOSED or event == 'Exit':
            addLog("info","Main window exited. App closed.")
            exit(0)
        if event == '-assets-tanks-down-':
            addLog("info", "Button to download assets of tanks clicked")
            randaa()
        if event == '-assets-tanks-del-':
            addLog("info", "Button to remove folder with tanks assets clicked")
            tank_assets("Delete")
            window.refresh()

            
if __name__ == "__main__":
    addLog("info", "App init...")
    main()