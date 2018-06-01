import pickle
import numpy as np
import time
import pandas as pd
from pprint import pprint
from collections import OrderedDict
from psutil import virtual_memory

np.set_printoptions(suppress=True)

PATH = 'G:/SCII/misc/data.pkl'

def dict2numpy(GAME):
    dataset = []
    for game in GAME:
        player1 = game[0].copy()
        player2 = game[1].copy()
        player1_keys = list(player1.keys())
        player2_keys = list(player2.keys())

        x = []
        for p1_items in list(player1.items()):
            a = list(p1_items[1])
            a.append(p1_items[0])
            x.append(a)
        y = []
        for p2_items in list(player2.items()):
            b = list(p2_items[1])
            b.append(p2_items[0])
            y.append(b)

        player1 = np.array(x)
        player2 = np.array(y)
            
        dataset.append((player1, player2, game[2], game[3]))
    return dataset

def findVal(each, units):
    if len(each) == 3 and type(each[1]) == str:
        return units[each[1]]
    elif len(each) == 3 and type(each[1]) == int:
        return each[1]
    elif len(each) == 4 and each[1] == '-':
        return -1*units[each[2]]
    elif len(each) == 4 and each[1] == '+':
        return units[each[2]]
    else:
        return 0
    
def transform(game, events, units, stats):
    prev_frame = 0
    temp = {}

    game = sorted(game, key=lambda k: k[0])
    
    for each in game:
        if each[0] not in temp:
            if len(temp) != 0:
                events = temp[prev_frame].copy()
            temp[each[0]] = events.copy()
            if len(each) == 3:
                temp[each[0]][stats[each[2]]] = findVal(each, units)
            else:
                temp[each[0]][stats[each[3]]] = findVal(each, units)
            prev_frame = each[0]
        else:
            if len(each) == 3:
                temp[each[0]][stats[each[2]]] = findVal(each, units)
            else:
                temp[each[0]][stats[each[3]]] = findVal(each, units)
    return temp

def appendLabel(game):
    appended_game = [] 
    for label in game:
        for step in range(len(game[label])):
            appended_game.append(game[label][step] + (label,))
    return appended_game

def dict_map(itr, oh):
    TEMP = {}
    for i, a in enumerate(itr):
        TEMP[a] = i+oh
    return TEMP

if __name__ == '__main__':
    with open(PATH, 'rb') as data:
        DATA = pickle.load(data)
        games = DATA['games']
        zerg_units = DATA['zerg_units']
        zerg_stats = DATA['zerg_stats']
        terran_units = DATA['terran_units']
        terran_stats = DATA['terran_stats']
        protoss_units = DATA['protoss_units']
        protoss_stats = DATA['protoss_stats']
        del DATA
        
    units = sorted(list(set(zerg_units + terran_units + protoss_units)))
    
    units = dict_map(units, 1)
    
    zs_length = len(zerg_stats)
    ps_length = len(protoss_stats)
    ts_length = len(terran_stats)
    lengths = {'Zerg': zs_length,
               'Terran': ts_length,
               'Protoss': ps_length}

    zerg_mapped = dict_map(zerg_stats, 0)
    terran_mapped = dict_map(terran_stats, 0)
    protoss_mapped = dict_map(protoss_stats, 0)
    statatistics = {'Zerg': zerg_mapped,
                    'Terran': terran_mapped,
                    'Protoss': protoss_mapped}
    
    GAME = {'Zerg': [],
            'Terran': [],
            'Protoss': []}
    for k, game in enumerate(games):
        map_name = game['Win'][0]
        win_race = game['Win'][2]
        loss_race = game['Loss'][2]
        win_labels = game['Win'][3]
        loss_labels = game['Loss'][3]
        win_game = appendLabel(game['Win'][4])
        loss_game = appendLabel(game['Loss'][4])
        del game

        winner_events = np.zeros(shape=(lengths[win_race]))
        loser_events = np.zeros(shape=(lengths[loss_race]))

        player1 = transform(win_game, winner_events, units, statistics[win_race])
        player2 = transform(loss_game, loser_events, units, statistics[loss_race])
        
        GAME[win_race].append((player1, player2, map_name, 1))
        GAME[loss_race].append((player2, player1, map_name, 0))
        print(k+1, '/', len(games), 'replays done..')

    with open('game_info.pkl', 'wb') as gipkl:
        pickle.dump(GAME, gipkl)

    zerg_dataset = dict2numpy(GAME['Zerg'])
    protoss_dataset = dict2numpy(GAME['Protoss'])
    terran_dataset = dict2numpy(GAME['Terran'])

    Dataset = {'Zerg': zerg_dataset,
               'Protoss': protoss_dataset,
               'Terran': terran_dataset}

    with open('dataset.pkl', 'wb') as dpkl:
        pickle.dump(Dataset, dpkl)

    

    

    






    
