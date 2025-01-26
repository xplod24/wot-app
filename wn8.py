import requests
import json
from asset_downloader import apiCaller
from config_reader import *

class WN8:
    """
    This class calculates wn8 of player
    """

    def __init__(self, search):
        self.expected_tank_values = None
        self.wn8 = None
        self.account_id = search

    def calculate(self):
        """This function is required to calculate given player wn8
        Its automatically called after init of class.

        Returns:
            int: A integer of player's wn8. Defaults to 0 if no battles found on
            any tanks on player's account.
        """
        if self.wn8 is None:
            account_id = self.account_id
            # Get summary values
            sum = apiCaller(wotApiPlayerInfo, ['statistics.all.battles' ,'statistics.all.frags','statistics.all.damage_dealt','statistics.all.dropped_capture_points','statistics.all.spotted','statistics.all.wins',f"&account_id={account_id}"], wg=True)
            # print(sum.text)
            data = sum[1]
            summary = data["data"][str(account_id)]["statistics"]['all']
            # print(summary)
            # Get tanks values
            tan = apiCaller(wotApiPlayerTanksData, ['tank_id,statistics.battles',f"&account_id={account_id}"], wg=True)
            dat = tan[1]
            tanks = dat["data"][str(account_id)]
            #print(tanks)
            if not tanks:
                self.wn8 = 0
                return self.wn8
            
            response = requests.get('https://static.modxvm.com/wn8-data-exp/json/wn8exp.json')
            da = json.loads(response.text)
            expected_tank_values = da["data"]
            # print(expected_tank_values)
            expDAMAGE = expFRAGS = expSPOT = expDEF = expWIN = 0
            missing = []
            found = []

            for x in expected_tank_values:
                for tank in tanks:
                    # print(x)
                    if (tank['tank_id'] == x["IDNum"]):
                        tank_battles = tank['statistics']['battles']
                        expDAMAGE   = expDAMAGE + (x['expDamage'] * tank_battles)
                        expSPOT     = expSPOT   + (x['expSpot'] * tank_battles)
                        expFRAGS    = expFRAGS  + (x['expFrag'] * tank_battles)
                        expDEF      = expDEF    + (x['expDef'] * tank_battles)
                        expWIN      = expWIN    + (0.01 * x['expWinRate'] * tank_battles)
                        found.append(x["IDNum"])
                if x["IDNum"] not in found:
                    missing.append(x["IDNum"])
            print(expDAMAGE, expSPOT, expFRAGS, expDEF, expWIN)
            print(len(found), len(missing))
            # Is it even worth to do it?
            # for x in missing:
            #     sum = apiCaller(wotApiPlayerTanksStats, ['all.battles','all.frags','all.damage_dealt','all.dropped_capture_points','all.spotted','all.wins',f"&tank_id={x}&account_id={account_id}&"])                
            #     if sum[1]['data'][str(account_id)] is not None:
            #         summary['damage_dealt'] -= sum[1]['data'][str(account_id)][0]['all']['damage_dealt']
            #         summary['spotted'] -= sum[1]['data'][str(account_id)][0]['all']['spotted']
            #         summary['frags'] -= sum[1]['data'][str(account_id)][0]['all']['frags']
            #         summary['dropped_capture_points'] -= sum[1]['data'][str(account_id)][0]['all']['dropped_capture_points']
            #         summary['wins'] -= sum[1]['data'][str(account_id)][0]['all']['wins']
            #         print(expDAMAGE, expSPOT, expFRAGS, expDEF, expWIN)

            
            rDAMAGE =   summary['damage_dealt']             / expDAMAGE
            rSPOT =     summary['spotted']                  / expSPOT
            rFRAG =     summary['frags']                    / expFRAGS
            rDEF =      summary['dropped_capture_points']   / expDEF
            rWIN =      summary['wins']                     / expWIN
            rWINc =     max(0,    (rWIN     - 0.71) / (1 - 0.71))
            rDAMAGEc =  max(0,    (rDAMAGE  - 0.22) / (1 - 0.22))
            rFRAGc =    max(0, min(rDAMAGEc + 0.2, (rFRAG - 0.12) / (1 - 0.12)))
            rSPOTc =    max(0, min(rDAMAGEc + 0.1, (rSPOT - 0.38) / (1 - 0.38)))
            rDEFc =     max(0, min(rDAMAGEc + 0.1, (rDEF - 0.10) / (1 - 0.10)))

            wn8 = (980 * rDAMAGEc + 210 * rDAMAGEc * rFRAGc + 155 * rFRAGc * rSPOTc + 75 * rDEFc * rFRAGc + 145 * min(1.8, rWINc))
            self.wn8 = round(wn8, 0)
            print("Current account WN8: "+ str(self.wn8))
        return round(self.wn8, 0)