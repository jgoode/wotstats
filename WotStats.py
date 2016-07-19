import json
import os
import ast
from datetime import datetime
from pymongo import MongoClient

from WotApi import WotApi


class WotPersonalStats(object):
    def __init__(self, jsond=None):
        if jsond is None:
            jsond = None
            return

        self.max_frags_tank_id = jsond['max_frags_tank_id']
        self.explosion_hits_received = jsond['explosion_hits_received']
        self.avg_damage_assisted_track = jsond['avg_damage_assisted_track']
        self.shots = jsond['shots']
        self.tanking_factor = jsond['tanking_factor']
        self.spotted = jsond['spotted']
        self.max_xp_tank_id = jsond['max_xp_tank_id']
        self.losses = jsond['losses']
        self.draws = jsond['draws']
        self.wins = jsond['wins']
        self.max_xp = jsond['max_xp']
        self.max_damage = jsond['max_damage']
        self.max_frags = jsond['max_frags']
        self.explosion_hits = jsond['explosion_hits']
        self.battles = jsond['battles']
        self.damage_dealt = jsond['damage_dealt']
        self.max_damage_tank_id = jsond['max_damage_tank_id']
        self.damage_received = jsond['damage_received']
        self.survived_battles = jsond['survived_battles']
        self.frags = jsond['frags']
        self.direct_hits_received = jsond['direct_hits_received']
        self.avg_damage_assisted = jsond['avg_damage_assisted']
        self.xp = jsond['xp']
        self.capture_points = jsond['capture_points']
        self.hits = jsond['hits']
        self.battle_avg_xp = jsond['battle_avg_xp']
        self.avg_damage_blocked = jsond['avg_damage_blocked']
        self.piercings = jsond['piercings']
        self.avg_damage_assisted_radio = jsond['avg_damage_assisted_radio']
        self.dropped_capture_points = jsond['dropped_capture_points']
        self.no_damage_direct_hits_received = jsond['no_damage_direct_hits_received']
        self.hits_percents = jsond['hits_percents']
        self.piercings_received = jsond['piercings_received']


class WotPersonalData(object):
    def __init__(self, jsond=None, vehicle=None):
        from WotApi import WotApi
        if jsond is None:
            jsond = None
            return
        self.expected_tanks = WotApi.get_expected_values()
        jsond = jsond
        self.add_date = jsond['add_date']
        self.global_rating = jsond['global_rating']
        self.clan_id = jsond['clan_id']
        self.nickname = jsond['nickname']
        self.account_id = jsond['account_id']
        self.last_battle_time = jsond['last_battle_time']

        #self.personal_stats = WotPersonalStats(jsond['stats'])
        self.exp_dmg = 0.0
        self.exp_spot = 0.0
        self.exp_frag = 0.0
        self.exp_def = 0.0
        self.exp_winrate = 0.0
        self.bc = 0.0
        self.avg_damage = 0.0
        self.r_damage = 0.0
        self.r_spot = 0.0
        self.r_frag = 0.0
        self.r_def = 0.0
        self.r_win = 0.0
        self.total_tanks = 0.0
        self.total_tier = 0.0
        self.total_wins = 0
        self.total_damage = 0.0
        self.total_spot = 0.0
        self.total_frag = 0.0
        self.total_def = 0.0

        c = []
        if vehicle is not None:
            for a in vehicle:
                v = WotVehicleData(a)
                expected_tank = self.find_tank(v.tank_id)
                if expected_tank is not None:
                    v.expected_tank = expected_tank
                    self.bc += v.battles
                    self.total_tanks += 1
                    self.total_tier += expected_tank['tier'] * v.battles
                    self.total_wins += v.wins
                    self.total_damage += v.damage_delt
                    v.tank_name = expected_tank['tankName']
                    v.tier = expected_tank['tier']

                    v.exp_dmg = float(expected_tank['expDamage'])
                    v.exp_spot = float(expected_tank['expSpot'])
                    v.exp_frag = float(expected_tank['expFrag'])
                    v.exp_def = float(expected_tank['expDef'])
                    v.exp_winrate = float(expected_tank['expWinRate'])

                    if v.battles > 0:
                        self.exp_dmg += v.exp_dmg * v.battles
                        self.exp_spot += v.exp_spot * v.battles
                        self.exp_frag += v.exp_frag * v.battles
                        self.exp_def += v.exp_def * v.battles
                        self.exp_winrate += v.exp_winrate / 100 * v.battles
                    else:
                        self.exp_dmg += v.exp_dmg
                        self.exp_spot += v.exp_spot
                        self.exp_frag += v.exp_frag
                        self.exp_def += v.exp_def
                        self.exp_winrate += v.exp_winrate / 100

                    self.total_spot += v.spotted
                    self.total_frag += v.frags
                    self.total_def += v.dropped_capture_points
                    self.avg_damage += v.avg_damage

                    v.r_damage = v.avg_damage / v.exp_dmg
                    # self.r_damage += v.r_damage

                    v.r_spot = v.avg_spot / v.exp_spot
                    # self.r_spot += v.r_spot

                    v.r_frag = v.avg_frag / v.exp_frag
                    # self.r_frag += v.r_frag

                    v.r_def = v.avg_def / v.exp_def
                    # self.r_def += v.r_def

                    v.r_win = v.avg_winrate * 100 / v.exp_winrate
                    # self.r_win += v.r_win

                    v.wn8 = Wn8.calculate(v.r_damage, v.r_spot, v.r_frag, v.r_def, v.r_win)

                c.append(v)
        self.vehicle_stats = c
        self.total_winrate = self.total_wins

        self.r_damage = self.total_damage / self.exp_dmg
        self.r_frag = self.total_frag / self.exp_frag
        self.r_spot = self.total_spot / self.exp_spot
        self.r_def = self.total_def / self.exp_def
        self.r_win = self.total_winrate / self.exp_winrate

        damagec = max(0, (self.r_damage - 0.22) / (1 - .22))
        fragc = max(0, min(damagec + 0.2, (self.r_frag - 0.12) / (1 - 0.12)))
        spotc = max(0, min(damagec + 0.1, (self.r_spot - 0.38) / (1 - 0.38)))
        defc = max(0, min(damagec + 0.1, (self.r_def - 0.10) / (1 - 0.10)))
        winc = max(0, (self.r_win - 0.71) / (1 - 0.71))

        edamage = 980 * damagec
        efrag = 210 * damagec * fragc
        espot = 155 * fragc * spotc
        edef = 75 * defc * fragc
        ewin = 145 * min(1.8, winc)

        self.wn8 = edamage + efrag + espot + edef + ewin
        self.expected_tanks = []

        # self.wn8 = Wn8.calculate(self.r_damage, self.r_spot, self.r_frag, self.r_def, self.r_win)

    def find_tank(self, tank_id):
        match = next((t for t in self.expected_tanks if t['IDNum'] == tank_id), None)
        return match
        # for t in self.expected_tanks['data']:
        #     print(t)
        #     if t['IDNum'] == tank_id:
        #         return t

    def __str__(self):
        result = 'nickname = ' + self.nickname + '\n'
        result += 'global_rating = ' + str(self.global_rating) + '\n'
        result += 'last_battle_time = ' + str(self.last_battle_time) + '\n' + '\n'
        for a in self.vehicle_stats:
            result += 'tank_id = ' + str(a.tank_id) + '\n'
            result += 'battles = ' + str(a.battles) + '\n'
            result += 'avg_damage = ' + str(a.avg_damage) + '\n' + '\n'
        return result


class Wn8(object):
    @staticmethod
    def calculate(r_damage, r_spot, r_frag, r_def, r_win):
        rwinc = max(0, (r_win - 0.71) / (1 - 0.71))
        rdamagec = max(0, (r_damage - 0.22) / (1 - 0.22))
        rfragc = max(0, min(rdamagec + 0.2, (r_frag - 0.12) / (1 - 0.12)))
        rspotc = max(0, min(rdamagec + 0.1, (r_spot - 0.38) / (1 - 0.38)))
        rdefc = max(0, min(rdamagec + 0.1, (r_def - 0.10) / (1 - 0.10)))
        return 980 * rdamagec + 210 * rdamagec * rfragc + 155 * rfragc * rspotc + 75 * rdefc * rfragc + 145 * min(1.8,
                                                                                                                  rwinc)


class WotVehicleData(object):
    def __init__(self, jsond=None, ):
        if jsond is None:
            jsond = None
            return

        self.tank_id = int(jsond['tank_id'])
        self.losses = float(jsond['losses'])
        self.wins = float(jsond['wins'])
        self.spotted = float(jsond['spotted'])
        self.frags = float(jsond['frags'])
        self.battles = self.wins + self.losses
        self.damage_delt = float(jsond['damage_dealt'])
        self.dropped_capture_points = float(jsond['dropped_capture_points'])
        self.wins = float(jsond['wins'])
        self.tank_name = ''
        self.tier = 0
        self.wn8 = 0.0

        if self.battles is not None and self.battles > 0:
            self.avg_damage = self.damage_delt / self.battles
            self.avg_spot = self.spotted / self.battles
            self.avg_frag = self.frags / self.battles
            self.avg_def = self.dropped_capture_points / self.battles
            self.avg_winrate = self.wins / self.battles
        else:
            self.avg_damage = self.damage_delt
            self.avg_spot = self.spotted
            self.avg_frag = self.frags
            self.avg_def = self.dropped_capture_points
            self.avg_winrate = self.wins


class WotStatsMongoClient(object):
    def __init__(self):
        self.uid = os.environ.get('MONGO_ID', '')
        self.pwd = os.environ.get('MONGO_PWD', '')
        self.domain = os.environ.get('MONGO_DOMAIN', '')
        self.url = 'mongodb://' + self.uid + ':' + self.pwd + '@' + self.domain + '/?ssl=true'

        self.client = MongoClient(self.url)

    @staticmethod
    def get_client():
        client_instance = WotStatsMongoClient()
        return client_instance.client


class WotStatsAccountService(object):
    @staticmethod
    def get_users_to_track():
        client = WotStatsMongoClient.get_client()
        db = client.WotStats
        collection = db.accounts
        return collection.find()

    @staticmethod
    def get_user_account_id(nickname):
        return WotApi.get_account_id(nickname)


class WotStatService(object):
    def __init__(self):
        """

        :rtype: object
        """
        self.users_to_track = WotStatsAccountService.get_users_to_track()
        self.user_data = []

    def process_user_stats(self):
        client = WotStatsMongoClient.get_client()
        db = client.WotStats
        for user in self.users_to_track:
            account_id = WotStatsAccountService.get_user_account_id(user['nickname'])
            api = WotApi(str(account_id), os.environ.get('WOT_APP_KEY', ''))
            jsond = api.get_account_data()
            vehicles = api.get_vehicle_stats()
            now = datetime.now()
            wot_data = WotPersonalData(jsond, vehicles)
            d = {"account_id": account_id, "date": now.strftime('%Y/%m/%d %H:%M:%S'), "data": ast.literal_eval(json.dumps(wot_data, default=lambda o: o.__dict__))}
            print(d)
            db.stats.insert_one(d)
            self.user_data.append(wot_data)





