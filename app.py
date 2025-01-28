import PySimpleGUI as sg
from asset_downloader import apiCaller
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from config_reader import *
import re
import os
from datetime import *
import threading
import queue
import ctypes
from plyer import notification
from wn8 import WN8
from matplotlib import use as use_agg
from ctypes import windll
import matplotlib.pyplot as plt

#Something important
windll.shcore.SetProcessDpiAwareness(1)
sg.theme('DarkGrey3')
use_agg('TkAgg')

# Get current screen size (where app is launched)
def screen_size():
    user32 = ctypes.windll.user32
    screensizex = user32.GetSystemMetrics(0)/3
    screensizey = user32.GetSystemMetrics(1)/3
    return (int(round(screensizex*2, 0)), int(round(screensizey*2, 0)))
    
#Pack canvas into render frame
def pack_figure(graph, figure):
    canvas = FigureCanvasTkAgg(figure, graph.Widget)
    plot_widget = canvas.get_tk_widget()
    plot_widget.pack(side='top', fill='both', expand=1)
    return plot_widget

#Plot the chart into canvas, using data for x and y axis
def plot_figure(index, datax, datay, nick, period):
    fig = plt.figure(index)
    ax = plt.gca()
    x = datax
    y = datay
    ax.cla()
    ax.set_title(f"WN8 per {period} for player {nick}", pad=20)
    ax.set_xlabel(f"{period}")
    ax.tick_params(axis='x', which='major' ,labelrotation=60)
    ax.set_ylabel("WN8")
    ax.grid()
    plt.plot(x, y, 'bo-')
    for a,b in zip(x,y):
        label = "{:.0f}".format(b)
        plt.annotate(label, (a,b), textcoords="offset points", xytext=(-3,10), ha='left', rotation=90)
    plt.tight_layout()
    
    fig.canvas.draw()
    
#Send native notification to os
def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Wot-app Checker",
        timeout=10,
    )

#Write function
def hitory_write_to_file(filename, target):
    with open(filename, 'w') as file:
        for element in target:
            # Check if the element is already in the file (to avoid duplicates)
            file.write(f"{element}\n")
    print(f"Elements written to {filename}.")

#Read function
def history_read_from_file(filename):
    try:
        history_list = []
        with open(filename, 'r') as file:
            for line in file:
                element = line.strip()
                history_list.append(element)
        return history_list
    except FileNotFoundError:
        print(f"The file {filename} does not exist.")
            
# Autocomplete function for nicknames searching
def autocomplete(input_text, event):
    if len(input_text) < 3 or not re.match(r'^[\w_]', input_text):
        return []
    response = apiCaller(wotApiPlayerList, extra=f"&search={input_text}&=type=exact&limit=10", wg=True)
    nicknames = response[1]['data']
    print(f"Nicknames returned {nicknames}")
    q.put(nicknames)
    q.put(response[2])
    event.set()

# Search for player in background
def player_loader(player, event):
    addLog("info", "Started loading player info")
    #Download user info
    a = apiCaller(wotApiPlayerList, ['nickname', 'account_id'], extra=f"&search={player}&=type=exact&limit=1", wg=True)
    #Set variable chosen_nickname to user's actual nickaname
    chosen_nickname = a[1]['data'][0]['nickname']
    #Set variable chosen_player_id to user's actual id
    chosen_player_id = a[1]['data'][0]['account_id']
    #Load player data by his player_id
    player_data = apiCaller(wotApiPlayerInfo, extra=f"&account_id={chosen_player_id}", fields=['statistics.all','clan_id'], wg=True)
    #Show it
    print(player_data[1])
    #Set variable player_clan id to actual player's clan id
    player_clan_id = player_data[1]['data'][str(chosen_player_id)]['clan_id']
    addLog("info", "Checking if player has clan...")
    # If player is in clan
    if player_clan_id is not None:
        addLog("info", "Player is in clan!")
        #Load user's clan data
        clan_data = apiCaller(wotApiClanData, ["name", "tag",f"&clan_id={player_clan_id}"], wg=True)
        #Set variable of clan's name
        player_clan_name = clan_data[1]['data'][str(player_clan_id)]['name']
        #Set variable of clan's id
        player_clan_tag = clan_data[1]['data'][str(player_clan_id)]['tag']
    #Otherwise, just leave it blank
    else:
        addLog("info", "Player is not in clan!")
        player_clan_name = "Not in clan"
        player_clan_tag = "Not in clan"
    #Add all needed variables to queue
    player_wn8 = WN8(chosen_player_id).calculate()
    q.put([chosen_nickname, chosen_player_id, player_clan_name, player_clan_id, player_clan_tag, player_wn8])
    #Finish event
    event.set()

# Server status checking (one time or periodical)
def server_checker(event):
    #Call api to get servers status
    a = apiCaller(wgApiServers, ["server", "players_online&game=wot"], wg=True)
    #Check if servers are available over the api and populate info correctly
    if len(a[1]['data']['wot']) > 0:
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
    #Otherwise return "Unknown"
    else:
        srv1 = "Unknown"
        srv2 = "Unknown"
        srv3 = "Unknown"
        srv4 = "Unknown"
    #Put response timing first
    q.put(a[2])
    #Put info about servers after
    q.put([srv1, srv2, srv3, srv4])
    #Finish event
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
session_history = []

#################################################################################################
# MAIN APP LAYOUT
#################################################################################################
listbox1 = [
    [sg.Text("Search player name from this list"),],
    [sg.Listbox(values=[], key='-listbox-', size=(10, 10), expand_x=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)], 
    [sg.Button("Search", key='-button-search-')]
]

listbox2 = [
    [sg.Text("Or choose player name from history"),],
    [sg.Listbox(values=session_history, key='-history-listbox-', size=(10, 10), expand_x=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)], 
    [sg.Button("Search", key='-button-search-history-')]
]

layout = [[sg.Frame(title="Player searching", layout=[
                        [sg.Text("Search for players by their nickname:"), sg.Input("", k='-input-', size=(45, 1)), sg.Button("Search", k='-button-player-search-')],
                        [sg.Column(listbox1        
                            ,expand_x=True, element_justification="center"),
                        sg.Column(listbox2  
                            ,expand_x=True, element_justification="center")],
          ], expand_x=True, expand_y=True)
              ,
           sg.Frame(title="Player info", layout=[
                [sg.Text("Player Name:"), sg.Push(), sg.Text("-", k='-player-name-after-search-')],
                [sg.Text("Player ID:"), sg.Push(), sg.Text("-", k='-player-id-after-search-')],
                [sg.Text("Player Clan:"), sg.Push(), sg.Text("-", k='-player-clan-')],
                [sg.Text("Player Clan ID:"), sg.Push(), sg.Text("-", k='-player-clan-id-')]
           ], expand_x=True, expand_y=True)
              ,
           sg.Frame(layout=[
               [sg.Text(text="EU1"), sg.Text(text="-----", k='-players-eu1-')],
               [sg.Text(text="EU2"), sg.Text(text="-----", k='-players-eu2-')],
               [sg.Text(text="EU3"), sg.Text(text="-----", k='-players-eu3-')],
               [sg.Text(text="EU4"), sg.Text(text="-----", k='-players-eu4-')],
               [sg.Button('Check', k='-button-serv-chk-')]], title="Servers", expand_x=True, expand_y=True)],
          [sg.TabGroup([
                [sg.Tab('Player stats', [
                  [sg.Push(),
                   sg.Column([[sg.Text("WN8:")],
                              [sg.Text("Battles")],
                              [sg.Text("Victories")],
                              [sg.Text("Lost")],
                              [sg.Text("Draws")],
                              [sg.Text("Max XP")],
                              [sg.Text("Average XP per battle")],
                              [sg.Text("Max DMG")],
                              [sg.Text("Shots fired")]]),
                   sg.Column([[sg.Text("-", k='-player-wn8-')],
                              [sg.Text("-", k='-battles-')],
                              [sg.Text("-", k='-victories-')],
                              [sg.Text("-", k='-lost-')],
                              [sg.Text("-", k='-draws-')],
                              [sg.Text("-", k='-max-xp-')],
                              [sg.Text("-", k='-avr-xp-battle-')],
                              [sg.Text("-", k='-max-dmg-')],
                              [sg.Text("-", k='-shots-fired-')]]),
                   sg.Push(),
                   ]], expand_x=True, expand_y=True),
                sg.Tab('Player\'s Clan', [[

                ]], expand_x=True, expand_y=True),
                sg.Tab('Monthly WN8 - Player Charts', [
                    [sg.Column([
                        # [sg.Button("Daily", key='-btn-player-daily-'), sg.Button("Weekly", key='-btn-player-weekly-'), sg.Button("Monthly", key='-btn-player-monthly')],
                        [sg.Graph((1000,750),(0,0),(1000,750), key='Graph1'), sg.Text("Sample chart")]
                        
                    ], size=(1550, 500), scrollable=True, vertical_scroll_only=True, key='-column-canvas-1-')]
                ], expand_x=True, expand_y=True),
                sg.Tab('Clan Charts', [[

                ]], expand_x=True, expand_y=True),
                ]],
                expand_x=True, expand_y=True,)],
          [sg.Button('Exit'), sg.Push(),
           sg.Frame(title="Request time", layout=[[sg.Text("Run any request first", k='-ping-api-')]])]]

#################################################################################################
# MAIN APP
#################################################################################################

def app():

    addLog("info", "App init: app()")
    processed = False
    servers_processed = False
    players_processed = False
    if not os.path.exists("history.txt"):
        hitory_write_to_file("history.txt", [])
    read = history_read_from_file("history.txt")
    session_history = read
    sizer = screen_size()
    window = sg.Window('WOT-app Checker app for World Of Tanks @by xplod24', layout, size=(sizer[0],sizer[1]), resizable=False, icon="game.ico")
    addLog("info", "Window created, launching...")
    
    graph1 = window['Graph1']
    fig1 = plt.figure(1, figsize=(9,4), dpi=80)
    first = True
    init_history = False
    
    while True:
        event, values = window.read(timeout=100)
        # print(event, values)
        # addLog("info",f"{event}, {values}")

        if event == sg.WIN_CLOSED or event == 'Exit':
            addLog("info", "Main window closed correctly.")
            addLog("info", "App closed: app()")
            exit(0)
            break
        
        if not init_history:
            window['-history-listbox-'].update(values=session_history)
            init_history = True

        # Check input values and define data_loader thread
        if type(values["-input-"]) is not None:
            input_text = values['-input-']    
        data_loader = threading.Thread(target=autocomplete, args=(input_text,eventer,))
        server_check = threading.Thread(target=server_checker, args=(eventer2,))
        # print(xa)
        # Search button clicked
        if event == '-button-player-search-':
            addLog("info", "Searching players...")
            if len(input_text) <= 3:
                sg.popup("Nickname has to contain at least 4 or more characters.")
                addLog("warning", "POPUP WINDOW: Nickname too short")
            else:
                eventer.clear()     #Clear events
                processed = False   #Disable processed flag
                window['-button-player-search-'].update(text="Searching...", disabled=True) #Disable search button
                data_loader.start() #Start searching thread
                addLog("info", "Started searching for players, search button disabled")
                
        # If thread is still alive and not processed yet
        if not processed and eventer.is_set():
            suggestions = q.get()#Get results from queue
            window['-ping-api-'].update(value=str(q.get())+" ms")
            nickname_list = []      
            for nick in suggestions:
                print(nick['nickname'])
                nickname_list.append(nick['nickname']) 
            print(suggestions)
            window['-listbox-'].update(values=nickname_list,)
            processed = True    #Mark it as processed
            addLog("info","Processing of thread is finished and terminated. Search button reenabled")
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
        
        if event == '-button-search-':
            window['-button-search-'].update(disabled=True)
            window['-button-search-history-'].update(disabled=True)
            xa = values['-listbox-'][0]  # Check for chosen player from listbox
            player_check = threading.Thread(target=player_loader, args=(xa,player_event,))
            addLog("info", "Started check for selected player from list...")
            player_event.clear()
            player_check.start()
            players_processed = False
            window['-player-wn8-'].update(value="Calculating...")
            window['Graph1'].erase()
            plt.clf()

                
        if event == '-button-search-history-':
            window['-button-search-'].update(disabled=True)
            window['-button-search-history-'].update(disabled=True)
            xa = values['-history-listbox-'][0] # Check for chosen player from listbox
            player_check = threading.Thread(target=player_loader, args=(xa,player_event,))
            addLog("info", "Started check for selected player from history...")
            player_event.clear()
            player_check.start()
            players_processed = False
            window['-player-wn8-'].update(value="Calculating...")
            window['Graph1'].erase()
            plt.clf()
            
        if not players_processed and player_event.is_set():
            # Read data from queue
            data = q.get()
            window['-player-name-after-search-'].update(value=data[0]+"["+ data[4] +"]")
            window['-player-id-after-search-'].update(value=data[1])
            window['-player-clan-'].update(value=data[2])
            window['-player-clan-id-'].update(value=data[3])
            window['-player-wn8-'].update(value=str(data[5]))
            if str(data[0]) not in session_history and not None:
                session_history.append(data[0])
                hitory_write_to_file("history.txt", session_history)
            window['-history-listbox-'].update(values=session_history)
            dates = []
            wn8s = []

            a = apiCaller(main_api_tomato+tomatoSessions, int(data[1]), tomato=True)
            month_data = a[1]['data']['sesmonth']
            for month in month_data:
                a = month['timestamp']
                wn8 = month['wn8']
                date = datetime.fromisoformat(a[:-1]).astimezone(timezone.utc)
                # print(date.strftime('%m-%Y') + f" WN8: {wn8}")
                dates.append(date.strftime('%m-%Y'))
                wn8s.append(wn8)
            # print(len(month_data))
            plt.ioff()
            #This is funny hahaha
            if first:
                pack_figure(graph1, fig1)
                first=False
            
            plot_figure(1, dates, wn8s, data[0], "month")
            window['-column-canvas-1-'].contents_changed()
            window['-button-search-'].update(disabled=False)
            window['-button-search-history-'].update(disabled=False)
            addLog("info", "Check is finished")
            players_processed = True
                    
    window.close()