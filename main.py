
import shutil
import threading
from app import app
from asset_downloader import apiCaller
from config_reader import *

##############################################################################################################################

# TODO: This whole file should be changed, it should only run once at first boot, create config.ini, and allow first setup
# TODO: Move init for creating config.ini to this file
# TODO: Make a settings.py and allow user to manage settings of an app
# TODO: Add functionality to allow user to choose between saving images to local storage or load from web
# TODO: Add functionality to allow user to change rate of downloading refreshed data
# TODO: Add ability for user to write default player nickname to run most recent info of

##############################################################################################################################


if __name__ == "__main__":
    addLog("info", "App init...")

    # TODO: CHECK FOR UPDATES FROM GITHUB, IF ONE IS FOUND THEN PROMPT USER TO DOWNLOAD AND UPDATE
    # BELOW IS JUST A PROPOSED PROCESS OF UPDATING THE APP
    # try:
    #     check = check_for_update()
    #     if (check):
    #       download_update() -> run_script_end_program()
    #       do_update() -> finish_update_run_program()
    #     else:
    #       pass
    # except Exception as e:
    #     raise Exception(f"{e}")
    app()