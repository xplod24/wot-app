import requests
import PySimpleGUI as sg
import threading
import os
import shutil
from asset_downloader import downloader_tanks_icons, apiWotAssetsDownloader, downloader_consumables_and_modules
from log import addLog
from app import app
from layouts import layoutfirst
from config_reader import *
import os
from git import Repo
import sys

try:
    assets_tanks_pager = apiWotAssetsDownloader(wotApiAssetsTanks, "pl", ["images.big_icon"])
    assets_modules_pager = apiWotAssetsDownloader(wotApiAssetsModules, "pl", ["image"])
except  Exception as e:
    sg.popup(f"ERROR WHILE OPENING APP: {e}")
    addLog("error", f"While opening app, error has been catched: {e}")
    raise Exception(f"Error catched: {e}")

total_images = assets_tanks_pager[1]['meta']['total']
total_images_modules = assets_modules_pager[1]['meta']['total']

if os.path.isdir("./assets/tanks-big"):
    tanks_assets_count = len(os.listdir("./assets/tanks-big"))
else:
    os.makedirs("./assets/tanks-big")
    tanks_assets_count = len(os.listdir("./assets/tanks-big"))

if os.path.isdir("./assets/modules"):
    modules_assets_count = len(os.listdir("./assets/modules"))
else:
    os.makedirs("./assets/modules")
    modules_assets_count = len(os.listdir("./assets/modules"))
    
if os.path.isdir("./assets/player"):
    player_assets_count = len(os.listdir("./assets/player"))
else:
    os.makedirs("./assets/player")
    player_assets_count = len(os.listdir("./assets/player"))
    
if os.path.isdir("./update"):
    pass
else:
    os.makedirs("./update")

def main():
    event2 = threading.Event()
    downloader = threading.Thread(target=downloader_tanks_icons, args=(event2,))
    modules_downloader = threading.Thread(target=downloader_consumables_and_modules, args=(event2,))
    
    window = sg.Window('WOT-app Checker app for World Of Tanks @by xplod24', layoutfirst, size=(1200,800), resizable=False, icon="game.ico")
    addLog("info", "Main window init...")
    while True:
        event, values = window.read(timeout=500)
        print(event, values)
        if window.is_closed() != True:
            if event == sg.TIMEOUT_EVENT:
                i = len(os.listdir("./assets/tanks-big"))
                l = len(os.listdir("./assets/modules"))
                if os.path.isdir("./assets/tanks-big") != True:
                    window['-tank-assets-status-'].update(value="Assets folder does not exist", font="bold", text_color="cyan2")
                elif tanks_assets_count == 0:
                    window['-tank-assets-status-'].update(value="Assets not downloaded", font="bold", text_color="cyan2")
                elif tanks_assets_count != total_images:
                    window['-tank-assets-status-'].update(value="Incorrect amount of assets", font="bold", text_color="cyan2")
                elif tanks_assets_count == total_images:
                    window['-tank-assets-status-'].update(value="Assets downloaded!", font="bold", text_color="lightgreen")
                if os.path.isdir("./assets/modules") != True:
                    window['-modules-assets-status-'].update(value="Assets folder does not exist", font="bold", text_color="cyan2")
                elif modules_assets_count == 0:
                    window['-modules-assets-status-'].update(value="Assets not downloaded", font="bold", text_color="cyan2")
                elif modules_assets_count != total_images_modules:
                    window['-modules-assets-status-'].update(value="Incorrect amount of assets", font="bold", text_color="cyan2")
                elif modules_assets_count == total_images_modules:
                    window['-modules-assets-status-'].update(value="Assets downloaded!", font="bold", text_color="lightgreen")
                window["-tanks-assets-pb-"].update(i, total_images)
                window["-tanks-assets-text-"].update(f"{i}/{total_images}")
                window["-modules-assets-pb-"].update(l, total_images_modules)
                window["-modules-assets-text-"].update(f"{l}/{total_images_modules}")
                
        ## WHEN WINDOW IS CLOSED TERMINATE ALL THREADS ##
        if event == sg.WIN_CLOSED or event == 'Exit':
            if downloader.is_alive():
                event2.set()
                downloader.join()
            if modules_downloader.is_alive():
                event2.set()
                modules_downloader.join()
            addLog("info","Main window exited. App closed.")
            exit(0)
            
        ## DOWNLOAD BUTTONS ##
        if event == '-assets-tanks-down-':
            if os.path.isdir("./assets/tanks-big"):
                pass
            else:
                os.makedirs("./assets/tanks-big")
            addLog("info", "Button to download assets of tanks clicked")
            downloader.start()
        if event == '-modules-assets-down-':
            if os.path.isdir("./assets/modules"):
                pass
            else:
                os.makedirs("./assets/modules")
            addLog("info", "Button to download assets of modules and consumables was clicked")
            modules_downloader.start()
 
        ## DELETE BUTTONS ##
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
            
        ## PROCEED TO MAIN APP ##
        if event == '-proceed-to-app-':
            if downloader.is_alive():
                event2.set()
                downloader.join()
            if modules_downloader.is_alive():
                event2.set()
                modules_downloader.join()
            window.close()
            app()

if __name__ == "__main__":
    addLog("info", "App init...")
    # try:
    #     init_repo()
    #     update_local_repo()
    # except Exception as e:
    #     raise Exception(f"{e}")
    main()