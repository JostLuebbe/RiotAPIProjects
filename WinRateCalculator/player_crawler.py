import os
import pickle as pk
import WinRateCalculator.classes as cls
import WinRateCalculator.APICall as rapi
from WinRateCalculator.classes import *
import datetime as dt


global_player_list = cls.PlayerList()
global_match_list = cls.MatchList()
tiers = ['DIAMOND', 'MASTER', 'CHALLENGER']
global_resources_file_path = os.path.dirname(os.path.abspath(__file__)) + '/resources/'


def seed_player_list():
    me = cls.Player(None)
    me.account_id = '205658211'
    me.summoner_id = '43223755'
    me.summoner_name = 'Firoe'
    me.tier = 'DIAMOND'
    me.rank = 'II'

    global_player_list.add(me)


def get_matches(player):
    player_match_history = rapi.RiotAPICall(
        '/lol/match/v3/matchlists/by-account/' + player.account_id + '/recent',
        global_resources_file_path + 'player_match_history'
    )
    match_id_list = list()
    player.recently_pulled = True
    player.pull_date = dt.date.today()
    if player_match_history.xml_root.find('matches') is not None:
        for match_xml in player_match_history.xml_root.find('matches'):
            if match_xml.findtext('queue') == '420':
                match_id_list.append(match_xml.find('gameId').text)
    else:
        print('Could not find matches for that summoner!')

    temp_match_list = list()
    for match_id in match_id_list:
        match_details = rapi.RiotAPICall(
            '/lol/match/v3/matches/' + match_id,
            global_resources_file_path + 'match_details'
        )
        match = cls.Match(match_details.xml_root)
        match.pull_date = dt.date.today()
        temp_match_list.append(match)
    return temp_match_list


def get_players(match_list):
    temp_player_list = set()
    for match in match_list:
        for player in match.players:
            if not global_player_list.is_present(player):
                temp_player_list.add(player)
    return temp_player_list


def find_quality_players(player_list):
    temp_quality_players = list()
    for player in player_list:
        player_details = rapi.RiotAPICall(
            '/lol/league/v3/positions/by-summoner/' + player.summoner_id,
            global_resources_file_path + 'player_details'
        )
        player.update_self(player_details.xml_root)
        if player.tier in tiers:
            temp_quality_players.append(player)

    return temp_quality_players


def load_globals():
    global global_player_list
    global global_match_list
    global global_resources_file_path
    with open(global_resources_file_path + 'global_player_list.pkl', 'rb') as f:
        global_player_list = pk.load(f)

    with open(global_resources_file_path + 'global_match_list.pkl', 'rb') as f:
        global_match_list = pk.load(f)


def save_globals():
    global global_player_list
    global global_match_list
    global global_resources_file_path
    with open(global_resources_file_path + 'global_player_list.pkl', 'wb') as f:
        pk.dump(global_player_list, f)

    with open(global_resources_file_path + 'global_match_list.pkl', 'wb') as f:
        pk.dump(global_match_list, f)


def main():
    global global_player_list
    global global_match_list
    seed_player_list()

    while True:
        load_globals()
        print('Current global_player_list length: ' + str(len(global_player_list.player_list)))
        current_player = global_player_list.get_random_player()
        print(current_player)

        player_quality_match_list = get_matches(current_player)
        print('Quality match number: ' + str(len(player_quality_match_list)))

        for quality_match in player_quality_match_list:
            global_match_list.add(quality_match)

        players = get_players(player_quality_match_list)
        print(str(len(players)) + ' unique players found')

        quality_players = find_quality_players(players)

        print(str(len(quality_players)) + ' quality players found')

        for player in quality_players:
            global_player_list.add(player)

        save_globals()


if __name__ == '__main__':
    main()
