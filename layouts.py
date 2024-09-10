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
                       [sg.Button("Download", k='-player-assets-down-'), sg.Button("Delete", k='-player-assets-del-'), sg.Button("Check", k='-player-assets-ref-')]]),sg.Push(),],
    [sg.VPush()],
    [sg.Text("Current news:", font="bold")],
    [sg.Text("Login will be available soon, this will only add ability to see private info.")],
    [sg.Push(),sg.Button("Login", k='-login-button-', disabled=True), sg.Button("Proceed to app", k='-proceed-to-app-'),sg.Push()]
]