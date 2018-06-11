import os
import pickle as pk
from WinRateCalculator.classes import *
import WinRateCalculator.classes as cls

global_file_path = os.path.dirname(os.path.abspath(__file__)) + '/resources/'

with open(global_file_path + 'global_player_list.pkl', 'rb') as f:
    global_player_list = pk.load(f)

with open(global_file_path + 'global_match_list.pkl', 'rb') as f:
    global_match_list = pk.load(f)

for player in global_player_list.player_list:
    if not player.pulled:
        player_match_history = rapi.RiotAPICall(
            '/lol/match/v3/matchlists/by-account/' + player.account_id + '/recent',
            global_file_path + 'player_match_history'
        )
        match_id_list = list()
        player.pulled = True
        player.pull_date = dt.date.today()
        if player_match_history.xml_root.find('matches') is not None:
            for match_xml in player_match_history.xml_root.find('matches'):
                if match_xml.findtext('queue') == '420':
                    match_id_list.append(match_xml.find('gameId').text)
        else:
            print('Could not find matches for that summoner!')

        for match_id in match_id_list:
            match_details = rapi.RiotAPICall(
                '/lol/match/v3/matches/' + match_id,
                global_file_path + 'match_details'
            )
            match = cls.Match(match_details.xml_root)
            global_match_list.add(match)

        with open(global_file_path + 'global_match_list.pkl', 'wb') as f:
            pk.dump(global_match_list, f)
        print('Current number of matches found: ' + str(len(global_match_list)))