import PySimpleGUI as sg
from asset_downloader import apiCaller
from config_reader import *
import re
from datetime import *
import threading
import queue
from plyer import notification

#Send native notification to os
def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Wot-app Checker",
        timeout=10,
    )

# Autocomplete function for nicknames searching
def autocomplete(input_text, event):
    if len(input_text) < 3 or not re.match(r'^[\w_]', input_text):
        return []
    response = apiCaller(wgPlayerInfo, [f"&search={input_text}&=type=exact&limit=10"])
    nicknames = response[1]['data']
    print(f"Nicknames returned {nicknames}")
    q.put(nicknames)
    q.put(response[2])
    event.set()

# Search for player in background
def player_loader(player, event):
    addLog("info", "Started loading player info")
    a = apiCaller(wotApiPlayerList, [f"&search={player}&=type=exact&limit=1"])                               #Download user info
    chosen_nickname = a[1]['data'][0]['nickname']                                                                  #Set variable chosen_nickname to user's actual nickaname
    chosen_player_id = a[1]['data'][0]['account_id']                                                               #Set variable chosen_player_id to user's actual id
    player_data = apiCaller(wotApiPlayerInfo, [f"&account_id={chosen_player_id}"])                           #Load player data by his player_id
    print(player_data[1])                                                                                          #Show it
    player_clan_id = player_data[1]['data'][str(chosen_player_id)]['clan_id']                                      #Set variable player_clan id to actual player's clan id
    addLog("info", "Checking if player has clan...")
    if player_clan_id is not None:                                                                                 # If player is in clan
        addLog("info", "Player is in clan!")
        clan_data = apiCaller(wotApiClanData, [f"&clan_id={player_clan_id}"])                                #Load user's clan data
        player_clan_name = clan_data[1]['data'][str(player_clan_id)]['name']                                       #Set variable of clan's name
        player_clan_tag = clan_data[1]['data'][str(player_clan_id)]['tag']                                         #Set variable of clan's id
    else:                                                                                                          #Otherwise, just leave it blank
        addLog("info", "Player is not in clan!")
        player_clan_name = "Not in clan"
        player_clan_tag = "Not in clan"
    q.put([chosen_nickname, chosen_player_id, player_clan_name, player_clan_id, player_clan_tag])                  #Add all needed variables to queue
    event.set()                                                                                                    #Finish event

# Server status checking (one time or periodical)
def server_checker(event):
    a = apiCaller(wgApiServers, ["server", "players_online&game=wot"])
    for i in a[1]['data']['wot']:
        xa = "Server: " + i['server'] + " Players: " + str(i['players_online'])
        print(xa)
        if i['server'] == "EU1":
            print(str(i['players_online']))
            srv1 = i['players_online']
        elif i['server'] == "EU2":
            print(str(i['players_online']))
            srv2 = i['players_online']
        elif i['server'] == "203":
            print(str(i['players_online']))
            srv3 = i['players_online']
        elif i['server'] == "204":
            print(str(i['players_online']))
            srv4 = i['players_online']
    q.put(a[2])
    q.put([srv1, srv2, srv3, srv4])
    event.set()
# Covert timestamp into HH:MM:SS, DD-MM-YYYY
def timestamp_covert(timestamp):
    date_to_return = datetime.fromtimestamp(timestamp)
    formatted_time = date_to_return.strftime("%H:%M:%S, %d-%m-%Y")
    print(f"Timestamp {timestamp} converted into {formatted_time}")
    return formatted_time

eventer = threading.Event()
eventer2 = threading.Event()
player_event = threading.Event()
q = queue.Queue()

#################################################################################################
# MAIN APP LAYOUT
#################################################################################################


layout = [[sg.Push(), sg.Text('Wot-app checker'), sg.Push()],
          [sg.Frame(title="Player searching", layout=[
              [sg.Text("Search for players by their nickname:")],
              [sg.Input("", k='-input-', size=(45, 1)), sg.Button("Search", k='-button-player-search-')],
              [sg.Text("Choose player name from this list")],
              [sg.Listbox(values=[], key='-listbox-', size=(40, 10), expand_x=True, bind_return_key=True,
                          select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)],
          ], size=(450, 200))
              , sg.Push(),
           sg.Frame(title="Player info", layout=[
               [[sg.HSep()],
                [sg.Text("Player Name:"), sg.Push(), sg.Text("-", k='-player-name-after-search-')],
                [sg.Text("Player ID:"), sg.Push(), sg.Text("-", k='-player-id-after-search-')], ],
               [sg.Text("Player Clan:"), sg.Push(), sg.Text("-", k='-player-clan-')],
               [sg.Text("Player Clan ID:"), sg.Push(), sg.Text("-", k='-player-clan-id-')]
           ], size=(350, 200))
              , sg.Push(),
           sg.Frame(layout=[
               [sg.Text(text="EU1"), sg.Text(text="-", k='-players-eu1-')],
               [sg.Text(text="EU2"), sg.Text(text="-", k='-players-eu2-')],
               [sg.Text(text="EU3"), sg.Text(text="-", k='-players-eu3-')],
               [sg.Text(text="EU4"), sg.Text(text="-", k='-players-eu4-')],
               [sg.Button('Check', k='-button-serv-chk-')]], title="Servers", size=(300, 200))],
          [sg.Text("Click \'ENTER\' to run")],
          [sg.TabGroup([
              [sg.Tab('Player statistics', [
                  [sg.Push(),
                   sg.Column([[sg.Text("Player Rating:")],
                              [sg.Text("Battles")],
                              [sg.Text("Victories")],
                              [sg.Text("Lost")],
                              [sg.Text("Draws")],
                              [sg.Text("Survived")],
                              [sg.Text("Max XP")],
                              [sg.Text("Average XP per battle")],
                              [sg.Text("Max DMG")],
                              [sg.Text("Shots fired")]]),
                   sg.Column([[sg.Text("-", k='-player-rating-')],
                              [sg.Text("-", k='-battles-')],
                              [sg.Text("-", k='-victories-')],
                              [sg.Text("-", k='-lost-')],
                              [sg.Text("-", k='-draws-')],
                              [sg.Text("-", k='-survived-')],
                              [sg.Text("-", k='-max-xp-')],
                              [sg.Text("-", k='-avr-xp-battle-')],
                              [sg.Text("-", k='-max-dmg-')],
                              [sg.Text("-", k='-shots-fired-')]]),
                   sg.Column([[sg.Text("Spotted")],
                              [sg.Text("Piercings")],
                              [sg.Text("Frags total")],
                              [sg.Text("Stuns total")],
                              [sg.Text("Damage total DEALT")],
                              [sg.Text("Damage total RECEIVED")],
                              [sg.Text("Damage total SPOTTED")],
                              [sg.Text("Max Frags")],
                              [sg.Text("Shots on target")]]),
                   sg.Column([[sg.Text("-", k='-spotted-')],
                              [sg.Text("-", k='-piercings-')],
                              [sg.Text("-", k='-frags-total-')],
                              [sg.Text("-", k='-stuns-total-')],
                              [sg.Text("-", k='-dmg-total-dealt-')],
                              [sg.Text("-", k='-dmg-total-received-')],
                              [sg.Text("-", k='dmg-total-spotted-')],
                              [sg.Text("-", k='-max-frags-')],
                              [sg.Text("-", k='-shots-hit-')]]),
                   sg.Push(),
                   ]], expand_x=True, expand_y=True),
               sg.Tab('Clan', [[

               ]], expand_x=True, expand_y=True)]],
              size=(1200, 400))],
          [sg.VPush()],
          [sg.Button('Exit'), sg.Push(),
           sg.Frame(title="Request time", layout=[[sg.Text("Run any request first", k='-ping-api-')]])]]

#################################################################################################
# MAIN APP
#################################################################################################


def app():

    processed = False
    servers_processed = False
    players_processed = False
    window = sg.Window('WOT-app Checker app for World Of Tanks @by xplod24', layout, size=(1200,800), resizable=False, icon="game.ico")

    while True:
        event, values = window.read(timeout=100)
        print(event, values)
        
        if event == sg.WIN_CLOSED or event == 'Exit':
            addLog("info", "App closed correctly.")
            break
        
        # Check input values and define data_loader thread
        input_text = values['-input-']
        if len(values['-listbox-']) > 0:
            xa = values['-listbox-'][0]  # Check for chosen player from listbox
            print(xa)
        else:
            xa = None

        data_loader = threading.Thread(target=autocomplete, args=(input_text,eventer,))
        server_check = threading.Thread(target=server_checker, args=(eventer2,))
        player_check = threading.Thread(target=player_loader, args=(xa,player_event,))

        # Search button clicked
        if event == '-button-player-search-':
            addLog("info", "Searching players...")
            if len(input_text) <= 3:
                sg.popup("Nickname has to contain at least 4 or more characters.")
                addLog("warning", "Nickname too short...")
            else:
                eventer.clear()     #Clear events
                processed = False   #Disable processed flag
                window['-button-player-search-'].update(text="Searching...", disabled=True) #Disable search button
                data_loader.start() #Start searching thread
                addLog("info", "Started searching for players, search button disabled")
                
        # If thread is still alive and not processed yet
        if  not processed and eventer.is_set():
            suggestions = q.get()#Get results from queue
            window['-ping-api-'].update(value=str(q.get())+" ms")
            nickname_list = []      
            for nick in suggestions:
                print(nick['nickname'])
                nickname_list.append(nick['nickname']) 
            print(suggestions)
            window['-listbox-'].update(values=nickname_list,)
            processed = True    #Mark it as processed
            addLog("info","Processing of thread is finished, terminated. Search button reenabled")
            window['-button-player-search-'].update(text="Search", disabled=False) #Reenable button
     
        # Server status check
        if event == '-button-serv-chk-':
            eventer2.clear()
            servers_processed = False
            window['-button-serv-chk-'].update(text="Checking...", disabled=True)
            server_check.start()
            addLog("info", "Started server checking and pinging...")
        
        # This is to ensure that all this is done in background
        if not servers_processed and eventer2.is_set():
            window['-ping-api-'].update(value=str(q.get())+" ms") # Get ressponse time
            i = q.get()                                           # Load array from queue
            window['-players-eu1-'].update(value=str(i[0]))
            window['-players-eu2-'].update(value=str(i[1]))
            window['-players-eu3-'].update(value=str(i[2]))
            window['-players-eu4-'].update(value=str(i[3]))
            window['-button-serv-chk-'].update(text="Check", disabled=False)
            addLog("info", "Finished server checking and pinging...")
            servers_processed = True                              # Mark this task as processed

        # Updating listbox element when searching for player
        if event == '-listbox-':
            addLog("info", "Started check for selected player from list...")
            player_event.clear()
            player_check.start()
            players_processed = False

        if not players_processed and player_event.is_set():
            data = q.get()
            window['-player-name-after-search-'].update(value=data[0]+"["+ data[4] +"]")
            window['-player-id-after-search-'].update(value=data[1])
            window['-player-clan-'].update(value=data[2])
            window['-player-clan-id-'].update(value=data[3])
            addLog("info", "Check is finished")
            players_processed = True
                    
    window.close()