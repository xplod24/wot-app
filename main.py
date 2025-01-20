
import shutil
import threading
import requests
from app import app
from asset_downloader import apiCaller
from config_reader import *
import PySimpleGUI as sg

repo_url = 'https://api.github.com/repos/xplod24/wot-app/releases/latest'

current_version_tag = "0.0.1"

##############################################################################################################################

# TODO: Add update file extraction and update process
# -----
# TODO: Make a settings.py and allow user to manage settings of an app <- !!IMPORTANT!!
# -----
# TODO: Add functionality to allow user to change rate of downloading refreshed data (min 10 min, max 1 hour)
# TODO: Add ability for user to write player names to get stats of, and do it every set amount of time (minimum 10 min)
# TODO: Add background checking for internet connection <- !!IMPORTANT!!

# PLAN FOR APP
# TODO: Add collection of data to a .csv file - this will be basically a database for single user we want to track data for.
# TODO: Filename should be: 'user-userid' for easier and faster searching
# TODO: Add ability to create charts shown in app in first tab
# TODO: Add ability to track data for single user

##############################################################################################################################

# Check if update is available
def check_for_update(url):
    addLog("info", "Checking for update...")
    response = requests.get(url)
    if response.status_code == 200:
        latest_release = response.json()
        latest_tag = latest_release['tag_name']
        print(f'The latest release tag is: {latest_tag}')
        return latest_tag
    else:
        print('Failed to fetch the latest release.')
        return False
    
# Downloading update
def download_update(url):
    addLog("info", "Update package download init...")
    response = requests.get(url)
    if response.status_code == 200:
        latest_release = response.json()
        asset = latest_release['assets'][0]  # Get the first asset
        download_url = asset['url']
        download_response = requests.get(download_url)
        if download_response.status_code == 200:
            with open(os.path.join("update", asset['name']), 'wb') as f:
                f.write(download_response.content)
            addLog("info", "Downloaded update package")
            return os.path.join("update", asset['name'])
            
        else:
            print('Failed to download the asset.')
            addLog("warning", "Failed to download update package")
            return None
    else:
        addLog("warning", "Failed to fetch update package")
        print('Failed to fetch the latest release.')
        return None



if __name__ == "__main__":
    addLog("info", "App init: main()")
    
    check = check_for_update(repo_url)

    # CHECKING FOR UPDATE ON GITHUB REPO
    if check == current_version_tag:
        addLog("info", "No new updates found.")
        pass
    elif not check:
        addLog("warning", "Can't fetch update.")
    else:
        result = sg.popup_yes_no(f"New update found: {check}. Do you want to download it?")
        if (result == "Yes"):
            download_update(repo_url)
        elif (result == "No"):
            pass
        else:
            sg.popup("Invalid input!")
        pass

    # BELOW IS JUST A PROPOSED PROCESS OF UPDATING THE APP
    #       run_script_end_program()
    #       do_update()
    #       finish_update_run_program()

    app()