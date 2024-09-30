import PySimpleGUI as sg

## MAIN LAYOUT OF FIRST SCREEN
## ULTIMATELY THIS SCREEN WILL BE SHOWN ONLY ON FIRST APP LAUNCH
## NEXT ACCESS WOULD BE ONLY IN APP ITSELF IN OPTIONS SECTION

layoutfirst = [
    [sg.Push(), sg.Text("Hello!"),sg.Push()],
    [sg.Push(), sg.Text("Thanks for downloading my app!"), sg.Push()],
    [sg.Push(), sg.Text("This app needs assets in order to function properly"), sg.Push()],
    [sg.Push(), sg.Text("Buttons below will tell you if you need to update folders with assets"), sg.Push()],
    [sg.Push(),sg.Column([[sg.Text("Tanks assets")],[sg.Text("Modules assets")],[sg.Text("Player stats assets")]]), 
                         sg.Column([[sg.Text("Refresh to update status", k='-tank-assets-status-')], [sg.Text("Refresh to update status", k='-modules-assets-status-')], [sg.Text("Refresh to update status", k='-player-assets-status-')]]),
                         sg.Column([[sg.Button("Download", k='-assets-tanks-down-'), sg.Button("Delete", k='-assets-tanks-del-'), sg.Button("Check", k='-assets-tanks-ref-')], 
                                                 [sg.Button("Download", k='-modules-assets-down-'), sg.Button("Delete", k='-modules-assets-del-'), sg.Button("Check", k='-modules-assets-ref-')], 
                                                 [sg.Button("Download", k='-player-assets-down-'), sg.Button("Delete", k='-player-assets-del-'), sg.Button("Check", k='-player-assets-ref-')]]),
                         sg.Column([[sg.ProgressBar(10, size=(10, 20), key="-tanks-assets-pb-")], [sg.ProgressBar(10, size=(10, 20), key="-modules-assets-pb-")], [sg.ProgressBar(10, size=(10, 20), key="-player-assets-pb-")]]),
                         sg.Column([[sg.Text("Checking...", key="-tanks-assets-text-")], [sg.Text("Checking...", key="-modules-assets-text-")], [sg.Text("Checking...", key="-player-assets-text-")]]),
     sg.Push(),],
    [sg.VPush()],
    [sg.Text("Current news:", font="bold")],
    [sg.Text("Login will be available soon, this will only add ability to see private info.")],
    [sg.Push(),sg.Button("Login", k='-login-button-', disabled=True), sg.Button("Proceed to app", k='-proceed-to-app-'),sg.Push()]
]

## MAIN APP LAYOUT WINDOW

layout = [[sg.Push(), sg.Text('Wot-app checker'),sg.Push()],
            [sg.Frame(title="Player searching",layout=[
                [sg.Text("Serach players by their nickname")],
                [sg.Input("",k='-input-', size=(45,1)), sg.Button("Search", k='-button-player-search-')],
                [sg.Listbox(values=[], key='-listbox-', size=(40, 10), expand_x=True, bind_return_key=True,select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)],
                ] ,size=(450, 200))
            , sg.Push(),
            sg.Frame(title="Player info", layout=[
                [[sg.HSep()],
                [sg.Text("Player name:"), sg.Push(), sg.Text("-", k='-player-name-after-search-')],
                [sg.Text("Player ID:"), sg.Push(), sg.Text("-", k='-player-id-after-search-')],]
            ], size=(350, 200)) 
            , sg.Push(),
            sg.Frame(layout=[
                [sg.Text(text="EU1"), sg.Text(text="-",k='-players-eu1-')],
                [sg.Text(text="EU2"), sg.Text(text="-",k='-players-eu2-')],
                [sg.Text(text="EU3"), sg.Text(text="-",k='-players-eu3-')],
                [sg.Text(text="EU4"), sg.Text(text="-",k='-players-eu4-')],
                [sg.Button('Check')]], title="Servers", size=(300, 200))],
            [sg.Button('Run full player check', k='-full-check-'), sg.Button('Just load player stats', k='-player-check-'), sg.Button('Just load player clan stats', k='-clan-check-')],
            [sg.TabGroup([
                [sg.Tab('Player statistics',[[
                    
                    ]], expand_x=True, expand_y=True), 
                 sg.Tab('Clan', [[
                     
                     ]], expand_x=True, expand_y=True)]], 
                        size=(1200,400))],
            [sg.VPush()],
            [sg.Button('Exit'),sg.Push(),sg.Frame(title="Request time", layout=[[sg.Text("Run any request first", k='-ping-api-')]])]]