import requests
from log import addLog
import json
import PySimpleGUI as sg
import threading
import time
import hashlib
from config_reader import *

# BASE API CALLER AND BUILDER
def apiCaller(whatApiToCall, fields):
    """API caller and builder to connect to WG API

    Args:
        whatApiToCall (variable): Use correct variable from config _reader
        lang (string): DEPRECATED SOON: Language of response
        fields (List[string]): List of strings of field elements to get response of. 

    Returns:
        (apiToCall, jsonParse, callTime): returns url called, then parsed json and call time (in ms)
    """
    try:
        # Builder portion - this is based on .ini file and configuration. This should be robust, as it require single config file
        apiToCall = main_api_url + whatApiToCall + app_id
        # Fields, can contain other calls, should be renamed into something more informative
        if fields is not None and isinstance(fields, list):
            apiToCall = apiToCall + "&fields="
            if  len(fields) > 1:
                for field in fields:
                    apiToCall = apiToCall  + field + "%2C"
            else:
                apiToCall = apiToCall  + fields[0]
        elif fields is None:
            pass
        else:
            print(f"Fields must be a list of strings not {type(fields)}")
            sg.Popup("Error in api calling! Check logs, and report issue on github.")
            raise Exception("Fields must be a list of strings not {}".format(type(fields)))
        print(apiToCall)
        responseApi = requests.get(apiToCall)
        responseApi.raise_for_status()
        code = responseApi.status_code
        callTime = responseApi.elapsed.total_seconds()*100
        print(str(callTime) + " - Response time")
        data = responseApi.text
        json_parse = json.loads(data)
    except Exception as error:
        print(f"Error: {error}")
        sg.Popup(f"Fatal error: {error}")
        exit(1)
    print(f"Function called this url: {apiToCall}")
    print(f"And received:\n {json_parse}")
    print(f"Response time was:  {callTime} ms")
    return apiToCall, json_parse, round(callTime, 2), code