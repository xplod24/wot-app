import PySimpleGUI as sg
from layouts import layout

def app():
    sg.theme('DarkGrey')

    window = sg.Window('WOT-app Checker app for World Of Tanks @by xplod24', layout, size=(800,600), resizable=False, icon="game.ico")

    while True:  # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Check':
            xa = ""
            a = "" ## CALL WG SERVER API
            window['-ping-api-'].update(value=str(a[1])+" ms")
            for i in a[0]['data']['wot']:
                xa = "Serwer: " + i['server'] + " Gracze: " + str(i['players_online'])
                print(xa)
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
            xa = values[0]
            print(xa)
            a = "" ## TO DO API CALL FOR player search
            window['-ping-api-'].update(value=str(a[1])+" ms")
            print(a[0])
            if a[0]['status'] == 'ok':
                window['-player-name-after-search-'].update(value=a[0]['data'][0]['nickname'])
                window['-player-id-after-search-'].update(value=a[0]['data'][0]['account_id'])

    window.close()