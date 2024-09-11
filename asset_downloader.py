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
from layouts import layout_download
from config_reader import *

def apiWotServerCaller(lang = None, game = None, fields = None):
    """Method to call WG API to get server statuses

    Args:
        lang (string, optional): Language of response. Defaults to None.
        game (string, optional): Game servers. Defaults to None. If None then shows all servers. Else put \"wot\".
        fields (List[string], optional): List of field for api to return. Defaults to None.

    Returns:
        tuple(apiToCall, json_parse, callTIme): Set of apiToCall -  url to call, json_parse - response from api, callTime - time of call in ms

    """
    try:
        apiToCall = main_api_url + wgApiServers + app_id
        if lang is not None:
            apiToCall = apiToCall + "&language="  + lang
        if game is not None:
            apiToCall = apiToCall + "&game=" + game
        if fields is not None and isinstance(fields, list):
            apiToCall = apiToCall + "&fields="
            if  len(fields) > 1:
                for f in fields:
                    apiToCall = apiToCall  + f + "%2C"
            else:
                apiToCall = apiToCall  + fields[0]
        elif fields is None:
            pass
        else:
            print(f"Fields must be a list of strings not {type(fields)}")
        print(apiToCall)
        responseApi = requests.get(apiToCall)
        responseApi.raise_for_status()
        callTime = responseApi.elapsed.total_seconds()*100
        print(str(callTime) + " - Response time")
        data = responseApi.text
        json_parse = json.loads(data)
        return apiToCall, json_parse, callTime


    except Exception as e:
        print(f"Error: {e}")
        sg.Popup(f"Fatal error: {e}")
        exit(1)
        
def worker(event):

    if os.path.isdir("./assets"):
        i = len(os.listdir("./assets"))
    else:
        i = 0

    assets_tanks_pager = "" ## TO DO API call to get tank assets pages
    total_pages = assets_tanks_pager[0]['meta']['page_total']
    total_images = assets_tanks_pager[0]['meta']['total']
    print(f"Total pages: {total_pages} Total images: {total_images} Current image count: {i}")
    
    if i < total_images:
        assets_page = "" ##  TO DO API call to get tank assets page

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
                        total_size = int(response.headers.get('content-lenght', 0))
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
    download_window = sg.Window("File Downloader", layout_download, modal=True)
    addLog("info", "Download window init...")
    assets_tanks_pager = "" ## TO DO : implement pager
    total_images = assets_tanks_pager[0]['meta']['total']

    # event2 = threading.Event()
    # downloader = threading.Thread(target=worker, args=(event2,))
    # downloader.start()
    
    while True:
        event, values = download_window.read(timeout=100)
        print(event, values)
        i = len(os.listdir("./assets/tanks-big"))
        print(f"Total files in assets folder: {i}")
        if download_window.is_closed() != True:
            download_window["-PROGRESS_BAR-"].update(i, total_images)
            download_window["-STATUS_TEXT-"].update(f"Files downloaded: {i}/{total_images}")
        if event == sg.WINDOW_CLOSED:
            # event2.set()
            # downloader.join()
            create_filetree("./assets/tanks-big", "assets-tanks-tree.txt")
            break

    download_window.close()

apiWotServerCaller("pl", "wot")