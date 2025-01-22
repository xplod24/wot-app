from textwrap import indent
import requests
from log import addLog
import json
import PySimpleGUI as sg
from config_reader import *

# BASE API CALLER AND BUILDER
def apiCaller(whatApiToCall, fields=None, extra="", tomato=False):
    """API caller and builder to connect to WG API or tomato.gg API

    Args:
        whatApiToCall (variable): Use correct variable from config _reader
        fields (List[string]) or (int): List of strings of field elements to get response of. CARE: if totmato is True, then it takes only int
        tomato (boolean): Call to tomato.gg API (currently only player sessions)

    Returns:
        (apiToCall, jsonParse, callTime): returns url called, then parsed json and call time (in ms)
    """
    addLog("info","apiCaller used")
    try:
        if not tomato:
        # Builder portion - this is based on .ini file and configuration. This should be robust, as it require single config file
            apiToCall = main_api_url + whatApiToCall + app_id + extra
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
                addLog("critical", "\'Fields\' is not correct type")
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
            show_parse = json.dumps(json_parse, indent=1)
        elif tomato is True:
            apiToCall = whatApiToCall
            if isinstance(fields, int):
                apiToCall = apiToCall + f"{fields}"
            else:
                addLog("critical", "\'Fields\' is not correct type. It must be int when calling tomato.gg api")
                print(f"Fields must be int not {type(fields)}")
                sg.Popup("Error in api calling! Check logs, and report issue on github.")
                raise Exception("Fields must be int not {}".format(type(fields)))
            print(apiToCall)
            responseApi = requests.get(apiToCall)
            responseApi.raise_for_status()
            code = responseApi.status_code
            callTime = responseApi.elapsed.total_seconds()*100
            print(str(callTime) + " - Response time")
            data = responseApi.text
            json_parse = json.loads(data)
            show_parse = json.dumps(json_parse, indent=1)
    except Exception as error:
        addLog("critical", f"Fatal error: {error}")
        print(f"Error: {error}")
        sg.Popup(f"Fatal error: {error}")
        exit(1)
    print(f"Function called this url: {apiToCall}")
    print(f"And received:\n {show_parse}")
    print(f"Response time was:  {callTime} ms")
    return apiToCall, json_parse, round(callTime, 2), code