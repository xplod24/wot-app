import requests
import PySimpleGUI as sg
import threading
import os
import shutil
from asset_downloader import worker, apiWotAssetsDownloader
from log import addLog
from app import app
from layouts import layoutfirst
from config_reader import *

assets_tanks_pager = apiWotAssetsDownloader(wotApiAssetsTanks, "pl", ["images.big_icon"])
total_images = assets_tanks_pager[1]['meta']['total']

if os.path.isdir("./assets/tanks-big"):
    tanks_assets_count = len(os.listdir("./assets/tanks-big"))
else:
    os.makedirs("./assets/tanks-big")
    tanks_assets_count = len(os.listdir("./assets/tanks-big"))

def main():
    event2 = threading.Event()
    downloader = threading.Thread(target=worker, args=(event2,))
    
    window = sg.Window('WOT-app Checker app for World Of Tanks @by xplod24', layoutfirst, size=(1200,800), resizable=False, icon="game.ico")
    addLog("info", "Main window init...")
    while True:
        event, values = window.read(timeout=100)
        print(event, values)
        if window.is_closed() != True:
            if event == sg.TIMEOUT_EVENT:
                i = len(os.listdir("./assets/tanks-big"))
                if os.path.isdir("./assets/tanks-big") != True:
                    window['-tank-assets-status-'].update(value="Assets folder does not exist", font="bold", text_color="cyan2")
                elif tanks_assets_count == 0:
                    window['-tank-assets-status-'].update(value="Assets not downloaded", font="bold", text_color="cyan2")
                elif tanks_assets_count != total_images:
                    window['-tank-assets-status-'].update(value="Incorrect amount of assets", font="bold", text_color="cyan2")
                elif tanks_assets_count == total_images:
                    window['-tank-assets-status-'].update(value="Assets downloaded!", font="bold", text_color="lightgreen")
                window["-tanks-assets-pb-"].update(i, total_images)
                window["-tanks-assets-text-"].update(f"{i}/{total_images}")
        if event == sg.WIN_CLOSED or event == 'Exit':
            if downloader.is_alive():
                event2.set()
                downloader.join()
            addLog("info","Main window exited. App closed.")
            exit(0)
        if event == '-assets-tanks-down-':
            if os.path.isdir("./assets/tanks-big"):
                pass
            else:
                os.makedirs("./assets/tanks-big")
            addLog("info", "Button to download assets of tanks clicked")
            downloader.start()
            
        if event == '-proceed-to-app-':
            if downloader.is_alive():
                event2.set()
                downloader.join()
            window.close()
            app()
        if event == '-assets-tanks-del-':
            if downloader.is_alive():
                event2.set()
                downloader.join()
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