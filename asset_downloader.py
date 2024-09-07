import requests
import os
from alive_progress import alive_bar
from log import addLog
from asset_checker import get_checksum_from_filetree, create_filetree
import json
import PySimpleGUI as sg
import threading
import time
import hashlib

def apiCaller(stringToCall):
    """This method allows to call an api for a response.
    Returns tuple of json and response time in ms.

    Args:
        stringToCall (string): Specify url to call

    Returns:
        (json_parse, ms) : json_parse - Response from api parsed to json, ms - Response time measured in miliseconds
    """
    try:
        responseAPI = requests.get(stringToCall)
        responseAPI.raise_for_status()
    except requests.RequestException as e:
        print(f"Request Failed: {e}") 
    
    ms = responseAPI.elapsed.total_seconds()*100
    print(str(ms) + " - Response time")
    data = responseAPI.text
    json_parse = json.loads(data)
    return json_parse, ms
        
def worker(event):

    if os.path.isdir("./assets"):
        i = len(os.listdir("./assets"))
    else:
        i = 0

    assets_tanks_pager = apiCaller("https://api.worldoftanks.eu/wot/encyclopedia/vehicles/?application_id=9ec1b1d893318612477ebc6807902c3c&fields=images.big_icon")
    total_pages = assets_tanks_pager[0]['meta']['page_total']
    total_images = assets_tanks_pager[0]['meta']['total']
    print(f"Total pages: {total_pages} Total images: {total_images} Current image count: {i}")
    
    if i < total_images:
        assets_page = apiCaller("https://api.worldoftanks.eu/wot/encyclopedia/vehicles/?application_id=9ec1b1d893318612477ebc6807902c3c&fields=images.big_icon")

        for tank_id, inner_dict in assets_page[0]['data'].items():
            if event.is_set():
                addLog("debug",f"{threading.get_ident()} Thread will be terminated")
                print("Thread is terminating...")
                break
            
            for big_image in inner_dict:
                
                if event.is_set():
                    addLog("debug",f"{threading.get_ident()} Thread will be terminated")
                    print("Thread is terminating...")
                    break
                
                file_to_download = inner_dict[big_image]['big_icon']
                file_itself = os.path.basename(file_to_download)
                check_for_file = os.path.isfile(os.path.join("./assets", file_itself))
                
                print(f"Tank_id: {tank_id}, Big_iamge: {file_to_download}")
                print(f"Filename: {file_itself} Is in folder?: {check_for_file}")
                
                if check_for_file:
                    print(f"{file_itself} File is found, ommiting...")
                    addLog("info",f"{file_itself} File is found, ommiting...")
                    i = i + 1
                    break
                
                else:
                    print(f"{file_itself} File is missing! Downloading...")
                    addLog("info",f"{file_itself} File is missing! Downloading...")
                    
                    try:
                        # response = requests.get(file_to_download, stream=True)

                        # if response.status_code != 200:
                        #     print (f"Failed to download file: {response.status_code}")
                        
                        # filename = file_itself
                        
                        total_size = int(response.headers.get('content-lenght', 0))

                        # file_path = os.path.join(f"./assets/tanks-big/{filename}")
                        # if os.path.exists(file_path):
                        #     print(f"File already exists! File: {filename}")
                        #     break
                        
                        filepath = os.path.join("./assets/tanks-big", file_itself)
                        if os.path.exists(filepath):
                            print(f"File {file_itself} already exists, checking checksum...")
                            with open(filepath, 'rb') as f:
                                file_checksum = hashlib.md5(f.read()).hexdigest()
                            if file_checksum != get_checksum_from_filetree(file_itself):
                                print(f"Checksum mismatch, redownloading {file_itself}...")
                                os.remove(filepath)
                                response = requests.get(file_to_download, stream=True)
                                with open(filepath, 'wb') as f:
                                    for chunk in response.iter_content(1024):
                                        f.write(chunk)
                                print(f"Downloaded {file_itself}")
                            else:
                                print(f"Checksum matches, skipping {file_itself}")
                        else:
                            print(f"Downloading {file_itself}...")
                            response = requests.get(file_to_download, stream=True)
                            with open(filepath, 'wb') as f:
                                for chunk in response.iter_content(1024):
                                    f.write(chunk)
                            print(f"Downloaded {file_itself}")
                        
                        with alive_bar(total_size, force_tty=None) as bar:
                            with open(filepath, 'wb') as f:
                                for chunk in response.iter_content(1024):
                                    f.write(chunk)
                                    bar(len(chunk))
                        
                        print("File finished downloading.")
                    except Exception as e:
                        print(f"Error occured! {e}")

                    time.sleep(0.2)
                    break

def randaa():
    
    layout_download = [
        [sg.Text("Downloading files...")],
        [sg.ProgressBar(10, size=(20, 20), key="-PROGRESS_BAR-")],
        [sg.Text("", key="-STATUS_TEXT-")]
    ]
    
    download_window = sg.Window("File Downloader", layout_download, modal=True)
    addLog("info", "Download window init...")
    assets_tanks_pager = apiCaller("https://api.worldoftanks.eu/wot/encyclopedia/vehicles/?application_id=9ec1b1d893318612477ebc6807902c3c&fields=images.big_icon")
    total_images = assets_tanks_pager[0]['meta']['total']

    event2 = threading.Event()
    downloader = threading.Thread(target=worker, args=(event2,))
    downloader.start()
    
    while True:
        event, values = download_window.read(timeout=100)
        print(event, values)
        i = len(os.listdir("./assets/tanks-big"))
        print(f"Total files in assets folder: {i}")
        if download_window.is_closed() != True:
            download_window["-PROGRESS_BAR-"].update(i, total_images)
            download_window["-STATUS_TEXT-"].update(f"Files downloaded: {i}/{total_images}")
        if event == sg.WINDOW_CLOSED:
            event2.set()
            downloader.join()
            create_filetree("./assets/tanks-big", "assets-tanks-tree.txt")
            break

    download_window.close()