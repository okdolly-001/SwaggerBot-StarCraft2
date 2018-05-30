import pickle
import numpy as np
from pprint import pprint

units = [	'Armory', 
			'Barracks', 
			'Factory', 
			'FusionCore', 
			'GhostAcademy', 
			'Starport', 
			'CommandCenter',
			'EngineeringBay',
			'Refinery',
			'SupplyDepot',
			'TechLab',
			'Banshee', 
			'Battlecruiser', 
			'Cyclone', 
			'Ghost', 
			'Hellion', 
			'Liberator', 
			'Marauder', 
			'Marine', 
			'Medivac', 
			'Nuke', 
			'Raven', 
			'Reaper', 
			'SiegeTank', 
			'Thor', 
			'Viking',
			'SCV'
		]

terran_y = ['air_building', 
			'army_event', 	
			'expansion_event', 
			'ground_building', 
			'supply_event', 
			'worker_event', 
			'tech_building',  
			'vespene_event']

terran_x = ['army_air', 
			'army_count', 		
			'army_ground', 
			'building_Armory_count', 
			'building_Barracks_count', 
			'building_Factory_count', 
			'building_FusionCore_count', 
			'building_GhostAcademy_count', 
			'building_Starport_count', 
			'building_CommandCenter_count',
			'building_EngineeringBay_count',
			'building_Refinery_count',
			'building_SupplyDepot_count',
			'building_TechLab_count',
			'unit_Banshee_count', 
			'unit_Battlecruiser_count', 
			'unit_Cyclone_count', 
			'unit_Ghost_count', 
			'unit_Hellion_count', 
			'unit_Liberator_count', 
			'unit_Marauder_count', 
			'unit_Marine_count', 
			'unit_Medivac_count', 
			'unit_Nuke_count', 
			'unit_Raven_count', 
			'unit_Reaper_count', 
			'unit_SiegeTank_count', 
			'unit_Thor_count', 
			'unit_Viking_count',
			'unit_Battlecruiser_count',
			'unit_SCV_count', 
			'expansion_buildings',  
			'mineral_spend', 
			'minerals_available', 
			'supply_available', 
			'supply_consumed',
			'vespene_available', 	
			'vespene_spend',
			'workers_active']

def dict_map(itr, oh):
    TEMP = {}
    for i, a in enumerate(itr):
        TEMP[a] = i+oh
    return TEMP

with open('data.pkl', 'rb') as d:
	data = pickle.load(d)
	games = data['games']
	del data

units = sorted(units)

mapped_units = dict_map(units, 1)
##for a in sorted(mapped_units):
##	print(a, mapped_units[a])
victories = []
for k, game in enumerate(games):
	print('### working on game {} of {}'.format(k, len(games)))
	win_race = game['Win'][2]
	if win_race == 'Terran':
		win_game = game['Win'][4]
		local_labels = list(win_game.keys())
		temp = []
		for label in local_labels:
			if label in terran_x or label in terran_y:
				for item in win_game[label]:
					if len(item) == 3 and item[1] == '+' and item[2] in units:
						mapped = mapped_units[item[2]]
						new_item = (item[0],) + (mapped,) + (label,)
						temp.append(new_item)
					elif len(item) == 2:
						new_item = item + (label,)
						temp.append(new_item)

		temp = sorted(temp, key= lambda k: k[0])
		state = [0]*len(terran_x)
		mapped_states = dict_map(terran_x, 0)

		#count = 0
		x = []
		y = []
		for timestep in temp:
			if timestep[2] in terran_x:
				state[mapped_states[timestep[2]]] = timestep[1]
			elif timestep[2] in terran_y and timestep[0] != 0:
				##print(state)
				##print('--->', timestep)
				x.append(state)
				y.append([timestep[1], timestep[2]])
				#count += 1
		x = np.asarray(x)
		y = np.asarray(y)
		victories.append((x, y))
		#print(count)

		##for p in sorted(mapped_states):
			##print(p, mapped_states[p])

print(len(victories))

with open('preped_data.pkl', 'wb') as prep:
	pickle.dump(victories, prep)