import os
import pickle as pk
from WinRateCalculator.classes import *

global_file_path = os.path.dirname(os.path.abspath(__file__))

with open(global_file_path + '/resources/global_player_list.pkl', 'rb') as f:
    global_player_list = pk.load(f)

with open(global_file_path + '/resources/global_match_list.pkl', 'rb') as f:
    global_match_list = pk.load(f)

print(len(global_player_list))
print(len(global_match_list))