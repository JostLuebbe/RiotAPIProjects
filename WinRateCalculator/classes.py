import random
import WinRateCalculator.APICall as rapi
import datetime as dt


class PlayerList:
    def __init__(self):
        self.tiers = ['DIAMOND', 'MASTER', 'CHALLENGER']
        self.player_list = list()

    def get_random_player(self):
        while True:
            random_player = self.player_list[random.randint(0, len(self.player_list)-1)]
            if not random_player.pulled:
                return random_player

    def is_present(self, inc_player):
        for player in self.player_list:
            if player.summoner_id == inc_player.summoner_id:
                return True
        return False

    def cull_list(self):
        temp_player_list = list()
        for player in self.player_list:
            player_details = rapi.RiotAPICall(
                '/lol/league/v3/positions/by-summoner/' + player.summoner_id,
                None
            )
            player.update_self(player_details.xml_root)
            if player.tier in self.tiers:
                if player.pull_date < dt.date.today() - dt.timedelta(weeks=2):
                    player.pulled = False
                temp_player_list.append(player)
        self.player_list = temp_player_list

    def add(self, player):
        if not self.is_present(player):
            self.player_list.append(player)

    def __len__(self):
        return len(self.player_list)

    def __str__(self):
        output_str = 'Players: '
        for player in self.player_list:
            output_str += player.summoner_name
        output_str += '\n'
        return output_str


class MatchList:
    def __init__(self):
        self.match_list = list()

    def cull_match_list(self):
        temp_match_list = list()
        for match in self.match_list:
            if match.pull_date < dt.date.today() - dt.timedelta(weeks=2):
                temp_match_list.append(match)
        self.match_list = temp_match_list

    def is_present(self, inc_match):
        for match in self.match_list:
            if match.match_id == inc_match.match_id:
                return True
        return False

    def __len__(self):
        return len(self.match_list)

    def add(self, match):
        if not self.is_present(match):
            self.match_list.append(match)


class Player:

    def __init__(self, inc_xml):
        self.summoner_name = ''
        self.account_id = ''
        self.summoner_id = ''
        self.tier = ''
        self.rank = ''
        self.recently_pulled = False
        self.pull_date = dt.date

        if inc_xml is not None:
            self.create_player(inc_xml)

    def create_player(self, inc_xml):
        self.summoner_name = inc_xml.find('summonerName').text
        self.account_id = inc_xml.find('accountId').text
        self.summoner_id = inc_xml.find('summonerId').text

    def update_self(self, inc_xml):
        for league in inc_xml:
            if league.find('queueType').text == 'RANKED_SOLO_5x5':
                self.tier = league.find('tier').text
                self.rank = league.find('rank').text

    def __str__(self):
        output_str = ''
        output_str += 'Summoner Name: ' + self.summoner_name + '\n'
        output_str += 'Summoner ID: ' + self.summoner_id + '\n'
        output_str += 'Acount ID: ' + self.account_id + '\n'
        output_str += 'League Position: ' + self.tier + ' ' + self.rank + '\n'
        output_str += 'Pulled: ' + str(self.recently_pulled) + '\n'
        return output_str


class Match:
    def __init__(self, inc_xml):
        self.xml_root = inc_xml
        self.match_id = ''
        self.game_type = ''
        self.players = list()
        self.champions = list()
        self.pull_date = dt.date

        self.create_match()

    def create_match(self):
        self.match_id = self.xml_root.find('gameId').text
        self.game_type = self.xml_root.find('gameType').text
        for champion_info in self.xml_root.find('participants'):
            self.champions.append(champion_info.find('championId').text)
        for player_info in self.xml_root.find('participantIdentities'):
            self.players.append(Player(player_info[1]))

    def update_self(self, inc_xml):
        self.xml_root = inc_xml