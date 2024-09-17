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
    except Exception as e:
        print(f"Error: {e}")
        sg.Popup(f"Fatal error: {e}")
        exit(1)
    print(f"Function called this url: {apiToCall}")
    print(f"And received:\n {json_parse}")
    print(f"Response time was:  {callTime} ms")
    return apiToCall, json_parse, callTime

def apiWotAssetsDownloader(whatApiToCall, lang, fields):
    try:
        apiToCall = main_api_url + whatApiToCall + app_id
        if lang is not None:
            apiToCall = apiToCall + "&language="  + lang
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
    except Exception as e:
        print(f"Error: {e}")
        sg.Popup(f"Fatal error: {e}")
        exit(1)
    print(f"Function called this url: {apiToCall}")
    print(f"And received:\n {json_parse}")
    print(f"Response time was:  {callTime} ms")
    return apiToCall, json_parse, callTime

def worker(event):
    if os.path.isdir("./assets"):
        i = len(os.listdir("./assets"))
    else:
        i = 0

    assets_tanks_pager = apiWotAssetsDownloader(wotApiAssetsTanks, "pl", ["images.big_icon"])
    total_pages = assets_tanks_pager[1]['meta']['page_total']
    total_images = assets_tanks_pager[1]['meta']['total']
    print(f"Total pages: {total_pages} Total images: {total_images} Current image count: {i}")

    filetree_file = "assets-tanks-tree.txt"
    filetree_data = {}

    if i < total_images:
        while True:
            if event.is_set():
                addLog("debug", f"{threading.get_ident()} Thread will be terminated")
                print("Thread is terminating...")
                break

            assets_page = apiWotAssetsDownloader(wotApiAssetsTanks, "pl", ["images.big_icon"])

            for tank_id, inner_dict in assets_page[1]['data'].items():
                if event.is_set():
                    addLog("debug", f"{threading.get_ident()} Thread will be terminated")
                    print("Thread is terminating...")
                    break

                for big_image in inner_dict:
                    if event.is_set():
                        addLog("debug", f"{threading.get_ident()} Thread will be terminated")
                        print("Thread is terminating...")
                        break

                    file_to_download = inner_dict[big_image]['big_icon']
                    file_itself = os.path.basename(file_to_download)
                    check_for_file = os.path.isfile(os.path.join("./assets", file_itself))

                    print(f"Tank_id: {tank_id}, Big_image: {file_to_download}")
                    print(f"Filename: {file_itself} Is in folder?: {check_for_file}")

                    if check_for_file:
                        print(f"{file_itself} File is found, omitting...")
                        addLog("info", f"{file_itself} File is found, omitting...")
                        i = i + 1
                        continue

                    else:
                        print(f"{file_itself} File is missing! Downloading...")
                        addLog("info", f"{file_itself} File is missing! Downloading...")

                        try:
                            response = requests.get(file_to_download)
                            filepath = os.path.join("./assets/tanks-big", file_itself)
                            with open(filepath, 'wb') as f:
                                f.write(response.content)

                            with open(filepath, 'rb') as f:
                                file_checksum = hashlib.md5(f.read()).hexdigest()
                            filetree_data[file_itself] = file_checksum

                            print(f"Downloaded {file_itself}")
                        except Exception as e:
                            print(f"Error occurred! {e}")
                            continue

                        time.sleep(0.2)

    with open(filetree_file, 'w') as f:
        for file, checksum in filetree_data.items():
            f.write(f"{file} {checksum}\n")
