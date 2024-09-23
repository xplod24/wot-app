import PySimpleGUI as sg
from layouts import layout
from asset_downloader import apiWotAssetsDownloader
from config_reader import *
import re
import time

def autocomplete(input_text):
    if len(input_text) < 3 or not re.match(r'^[\w_]', input_text):
        return []
    response = apiWotAssetsDownloader(wotApiPlayerList, "pl", [f"&search={input_text}"])
    nicknames = response[1]['data']
    return nicknames

def app():

    window = sg.Window('WOT-app Checker app for World Of Tanks @by xplod24', layout, size=(1200,800), resizable=False, icon="game.ico")

    while True:
        event, values = window.read()
        print(event, values)
        aa = values['-input-']
        if aa is not None:
            nickname_list = []
            input_text = values['-input-']
            suggestions = autocomplete(input_text)
            for nick in suggestions:
                print(nick['nickname'])
                nickname_list.append(nick['nickname']) 
            print(suggestions)
            window['-listbox-'].update(values=nickname_list,)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Check':
            xa = ""
            a = apiWotAssetsDownloader(wgApiServers, "pl", ["server","players_online&game=wot"])
            window['-ping-api-'].update(value=str(a[2])+" ms")
            for i in a[1]['data']['wot']:
                xa = "Serwer: " + i['server'] + " Gracze: " + str(i['players_online'])
                print(xa)
                print(i)
                if i['server'] == "EU1":
                    print(str(i['players_online']))
                    window['-players-eu1-'].update(value=str(i['players_online']))
                elif i['server'] == "EU2":
                    print(str(i['players_online']))
                    window['-players-eu2-'].update(value=str(i['players_online']))
                elif i['server'] == "203":
                    print(str(i['players_online']))
                    window['-players-eu3-'].update(value=str(i['players_online']))
                elif i['server'] == "204":
                    print(str(i['players_online']))
                    window['-players-eu4-'].update(value=str(i['players_online']))
        if event == '-button-player-search-':
            if values['-input-'] is not None:
                xa = values['-input-']
            print(xa)
            a = apiWotAssetsDownloader(wgPlayerInfo, "pl", [f"&search={xa}&=type=exact&limit=10"])
            window['-ping-api-'].update(value=str(a[2])+" ms")
            print(a[1])
            if a[1]['status'] == 'ok':
                window['-player-name-after-search-'].update(value=a[1]['data'][0]['nickname'])
                window['-player-id-after-search-'].update(value=a[1]['data'][0]['account_id'])

    window.close()

app()