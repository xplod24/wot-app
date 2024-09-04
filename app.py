import PySimpleGUI as sg
from asset_downloader import apiCaller

def app():
    sg.theme('DarkGrey')
    layout = [[sg.Push(), sg.Text('Wot-app checker'),sg.Push()],
                [sg.Frame(title="Player searching",layout=[
                    [sg.Text("Serach players by their nickname")],
                    [sg.Input("", size=(45,1)), sg.Button("Search", k='-button-player-search-')],
                    [sg.Text("Write your nickname in field above, it is CASE SENSITIVE. You HAVE TO write your EXACT nickname. Once it is found, details will appear below.", size=(45,3))],
                    [sg.HSep()],
                    [sg.Text("Player name:"), sg.Push(), sg.Text("-", k='-player-name-after-search-')],
                    [sg.Text("Player ID:"), sg.Push(), sg.Text("-", k='-player-id-after-search-')]] ,size=(450, 200))
                , sg.Push(), sg.Frame(layout=[
                    [sg.Text(text="EU1"), sg.Text(text="-",k='-players-eu1-')],
                    [sg.Text(text="EU2"), sg.Text(text="-",k='-players-eu2-')],
                    [sg.Text(text="EU3"), sg.Text(text="-",k='-players-eu3-')],
                    [sg.Text(text="EU4"), sg.Text(text="-",k='-players-eu4-')],
                    [sg.Button('Check')]], title="Servers", size=(300, 200))],
                [sg.Button('Run full player check', k='-full-check-'), sg.Button('Just load player stats', k='-player-check-'), sg.Button('Just load player clan stats', k='-clan-check-')],
                [sg.TabGroup([[sg.Tab('Player statistics',[[]], expand_x=True, expand_y=True), sg.Tab('Clan', [[]], expand_x=True, expand_y=True)]], expand_x=True, expand_y=True)],
                [sg.VPush()],
                [sg.Button('Exit'),sg.Push(),sg.Frame(title="Request time", layout=[[sg.Text("Run any request first", k='-ping-api-')]])]]

    window = sg.Window('WOT-app Checker app for World Of Tanks @by xplod24', layout, size=(800,600), resizable=False, icon="game.ico")

    while True:  # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Check':
            xa = ""
            a = apiCaller("https://api.worldoftanks.eu/wgn/servers/info/?application_id=9ec1b1d893318612477ebc6807902c3c&game=wot")
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
            a = apiCaller("https://api.worldoftanks.eu/wot/account/list/?application_id=9ec1b1d893318612477ebc6807902c3c&type=exact&limit=1&search="+xa)
            window['-ping-api-'].update(value=str(a[1])+" ms")
            print(a[0])
            if a[0]['status'] == 'ok':
                window['-player-name-after-search-'].update(value=a[0]['data'][0]['nickname'])
                window['-player-id-after-search-'].update(value=a[0]['data'][0]['account_id'])

    window.close()