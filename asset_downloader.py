import requests
import os
from alive_progress import alive_bar
from log import addLog
import json
import PySimpleGUI as sg
import threading
import time

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
        raise Exception(f"Request Failed: {e}") from e
    
    ms = responseAPI.elapsed.total_seconds()*100
    print(str(ms) + " - Response time")
    data = responseAPI.text
    json_parse = json.loads(data)
    return json_parse, ms

def download_file(url, save_path, filename=None):
    """
    Download a file from a direct link with a progress bar.

    Args:
        url (str): The direct link to the file.
        save_path (str): The path where the file will be saved.
        filename (str, optional): The filename to use for the downloaded file. If not provided, the filename will be extracted from the URL.

    Returns:
        str: The path to the downloaded file.
    """
    # Send a GET request to the URL
    response = requests.get(url, stream=True)

    # Check if the response was successful
    if response.status_code != 200:
        raise Exception(f"Failed to download file: {response.status_code}")

    # Get the filename from the URL if not provided
    if not filename:
        filename = os.path.basename(url)

    # Create the full path to the file
    file_path = os.path.join(save_path, filename)
    if os.path.exists(file_path):
        print(f"File already exists! File: {filename}")
        return False

    # Get the total size of the file
    total_size = int(response.headers.get('Content-Length', 0))

    # Open the file in binary write mode
    with open(file_path, 'wb') as f:
        # Create a progress bar with alive_progress
        with alive_bar(total_size, title=f"Downloading {filename}") as bar:
            # Iterate over the response chunks and write them to the file
            for chunk in response.iter_content(1024):
                f.write(chunk)
                bar(len(chunk))  # Update the progress bar

    return file_path

class Downloader(threading.Thread):
    def __init__(self, url, save_path, exit_event, filename = None):
        threading.Thread.__init__(self)
        self.url = url
        self.save_path = save_path
        self.filename = filename
        self.suspended = False
        self.exit_event = exit_event
        self.daemon = True

    def run(self):
        while True:
            if self.exit_event.is_set():
                break  # exit thread when window is closed
            if self.suspended:
                time.sleep(0.1)  # wait for 100ms before checking again
                continue
            try:

                response = requests.get(self.url, stream=True)

                if response.status_code != 200:
                    raise Exception(f"Failed to download file: {response.status_code}")

                if not self.filename:
                    self.filename = os.path.basename(self.url)

                file_path = os.path.join(self.save_path, self.filename)
                if os.path.exists(file_path):
                    print(f"File already exists! File: {self.filename}")
                    break

                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
            except Exception as e:
                print(f"Error occured! {e}")
                break

    def suspend(self):
        self.suspended = True

    def resume(self):
        self.suspended = False
        
def randaa():
    layout_download = [
        [sg.Text("Downloading files...")],
        [sg.ProgressBar(10, size=(20, 20), key="-PROGRESS_BAR-")],
        [sg.Text("", key="-STATUS_TEXT-")]
    ]
    download_window = sg.Window("File Downloader", layout_download, modal=True)
    addLog("info", "Download window init...")
    assets_tanks_pager = apiCaller("https://api.worldoftanks.eu/wot/encyclopedia/vehicles/?application_id=9ec1b1d893318612477ebc6807902c3c&fields=images.big_icon&page_no=1")
    total_images = assets_tanks_pager[0]['meta']['total']
    
    if os.path.isdir("./assets"):
        i = len(os.listdir("./assets"))
    else:
        i = 0
        
    exit_event = threading.Event()
    downloader = None
    
    while True:
        event, values = download_window.read(timeout=100)
        print(event, values)
        while download_window.is_closed() != True:
            if os.path.isdir("./assets"):
                i = len(os.listdir("./assets"))
            else:
                i = 0
            download_window["-PROGRESS_BAR-"].update(i, total_images)
            download_window["-STATUS_TEXT-"].update(f"Files downloaded: {i}/{total_images}")
            
            assets_tanks_pager = apiCaller("https://api.worldoftanks.eu/wot/encyclopedia/vehicles/?application_id=9ec1b1d893318612477ebc6807902c3c&fields=images.big_icon&page_no=1")
            total_pages = assets_tanks_pager[0]['meta']['page_total']
            total_images = assets_tanks_pager[0]['meta']['total']

            for page in range(total_pages):
                page = page + 1
                assets_page = apiCaller("https://api.worldoftanks.eu/wot/encyclopedia/vehicles/?application_id=9ec1b1d893318612477ebc6807902c3c&fields=images.big_icon&page_no="+str(page))
                print(f"Current page: {page}")
                    
                if os.path.isdir("./assets"):
                    pass
                else:
                    os.makedirs("./assets")
                    
                for a, b in assets_page[0]['data'].items():
                    for x in b:
                        print(a)
                        print(b[x]['big_icon'])
                        file_to_download = b[x]['big_icon']
                        is_file = os.path.basename(file_to_download)
                        if os.path.isfile(os.path.join("./assets", is_file)):
                            print("File already in folder")
                            pass
                        else:
                            print("File will be downloaded")
                            downloader = Downloader(file_to_download, "./assets", exit_event).start()
            break
        if downloader:
            downloader.join()
        break
        
    download_window.close()