import requests
import PySimpleGUI as sg
import json

def apiCaller(stringToCall):
    responseAPI = requests.get(stringToCall)
    ms = responseAPI.elapsed.total_seconds()*100
    print(str(ms) + " - Response time")
    data = responseAPI.text
    json_parse = json.loads(data)
    return json_parse, ms


sg.theme('BluePurple')

layout = [[sg.Text('Check WOT server status')],
            [sg.Frame(title="Audible",layout=[
                [sg.Text("Pryc")]] ,size=(450, 300))
            , sg.Push(), sg.Frame(layout=[
                [sg.Text(text="EU1"), sg.Text(text="-",k='-players-eu1-')],
                [sg.Text(text="EU2"), sg.Text(text="-",k='-players-eu2-')],
                [sg.Text(text="EU3"), sg.Text(text="-",k='-players-eu3-')],
                [sg.Text(text="EU4"), sg.Text(text="-",k='-players-eu4-')],
                [sg.Text("Request handled in"), sg.Text("Run check first", k='-ping-api-')]], title="Servers", size=(300, 300))],
            [sg.Button('Check'), sg.Button('Exit')]]

window = sg.Window('Pattern 2B', layout, size=(800,600), resizable=False)

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
            
        

window.close()

# for i in servers:
#     print("Serwer: " + i['server'])
#     print("Gracze: " + str(i['players_online']))
