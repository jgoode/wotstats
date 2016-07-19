import os

import requests


class WotApi(object):
    def __init__(self, account_id, app_id):
        self.account_id = account_id
        self.app_id = app_id

    def get_account_data(self):
        api_url = "https://api.worldoftanks.com/wot/account/info/?application_id=" + self.app_id + "&account_id=" + self.account_id
        response = requests.get(api_url)
        json = response.json()
        d = json['data'][self.account_id]
        last_battle_time = d["last_battle_time"]
        global_rating = d["global_rating"]
        clan_id = d["clan_id"]
        nickname = d["nickname"]
        stats = d["statistics"]["all"]
        from datetime import datetime
        now = datetime.now()
        return {
            "account_id": self.account_id,
            "last_battle_time": last_battle_time,
            "global_rating": global_rating,
            "nickname": nickname,
            "clan_id": clan_id,
            "stats": stats,
            "add_date": now.strftime('%Y/%m/%d %H:%M:%S')
        }

    def get_vehicle_stats(self):
        api_url = "https://api.worldoftanks.com/wot/tanks/stats/?application_id=" + self.app_id + "&account_id=" + self.account_id
        response = requests.get(api_url)
        json = response.json()
        d = json['data'][self.account_id]
        from datetime import datetime
        now = datetime.now()
        result = []
        for x in d:
            result.append({
                "account_id": self.account_id,
                "max_frags": x["max_frags"],
                "tank_id": x["tank_id"],
                "hits_percents": x["all"]["hits_percents"],
                "dropped_capture_points": x["all"]["dropped_capture_points"],
                "wins": x["all"]["wins"],
                "direct_hits_received": x["all"]["direct_hits_received"],
                "frags": x["all"]["frags"],
                "piercings_received": x["all"]["piercings_received"],
                "explosion_hits": x["all"]["explosion_hits"],
                "damage_dealt": x["all"]["damage_dealt"],
                "piercings": x["all"]["piercings"],
                "draws": x["all"]["draws"],
                "tanking_factor": x["all"]["tanking_factor"],
                "battle_avg_xp": x["all"]["battle_avg_xp"],
                "avg_damage_blocked": x["all"]["avg_damage_blocked"],
                "hits": x["all"]["hits"],
                "xp": x["all"]["xp"],
                "losses": x["all"]["losses"],
                "explosion_hits_received": x["all"]["explosion_hits_received"],
                "spotted": x["all"]["spotted"],
                "no_damage_direct_hits_received": x["all"]["no_damage_direct_hits_received"],
                "battles": x["all"]["battles"],
                "damage_received": x["all"]["damage_received"],
                "survived_battles": x["all"]["survived_battles"],
                "shots": x["all"]["shots"],
                "capture_points": x["all"]["capture_points"],
                "in_garage": x["in_garage"],
                "max_xp": x["max_xp"],
                "mark_of_mastery": x["mark_of_mastery"],
                "add_date": now.strftime('%Y/%m/%d %H:%M:%S')
            })

        return result

    @staticmethod
    def get_account_id(nickname):
        app_id = os.environ.get('WOT_APP_KEY', '')
        if len(app_id) > 1:
            api_url = "https://api.worldoftanks.com/wot/account/list/?application_id=" + app_id + "&search=" + nickname
            response = requests.get(api_url)
            json = response.json()
            print(json['data'][0]['account_id'])
            return json['data'][0]['account_id']

    @staticmethod
    def get_expected_values():
        import json
        with open("expected_tank_values.json", encoding='utf-8') as data_file:
            data = json.load(data_file)

        with open("tank_data.json", encoding='utf-8') as data_tanks:
            tank_data = json.load(data_tanks)

        result = []
        tanks = tank_data['data']

        for d in data['data']:
            # match = next((t for t in tank_data['data'] if t['tank_id'] == d['IDNum']), None)
            tank_id = str(d['IDNum'])
            if tank_id in tanks:
                match = tanks[tank_id]
                result.append({
                    'IDNum': d['IDNum'],
                    'expFrag': d['expFrag'],
                    'expDamage': d['expDamage'],
                    'expSpot': d['expSpot'],
                    'expDef': d['expDef'],
                    'expWinRate': d['expWinRate'],
                    'nation': match['nation'],
                    'tier': match['level'],
                    'tankName': match['short_name_i18n'],
                    'type': match['type_i18n']
                })

        return result
