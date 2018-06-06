import random
import math
import os

import numpy as np
import pandas as pd

from collections import deque

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

_NOT_QUEUED = [0]
_QUEUED = [1]
_SELECT_ALL = [2]

_PLAYER_SELF = 1
_PLAYER_HOSTILE = 4
_ARMY_SUPPLY = 5

_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
_PLAYER_ID = features.SCREEN_FEATURES.player_id.index

_BUILD_ARMORY = actions.FUNCTIONS.Build_Armory_screen.id
_BUILD_BARRACKS = actions.FUNCTIONS.Build_Barracks_screen.id
_BUILD_COMMAND_CENTER = actions.FUNCTIONS.Build_CommandCenter_screen.id
_BUILD_FACTORY = actions.FUNCTIONS.Build_Factory_screen.id
_BUILD_FUSION_CORE = actions.FUNCTIONS.Build_FusionCore_screen.id
_BUILD_GHOST_ACADEMY = actions.FUNCTIONS.Build_GhostAcademy_screen.id
_BUILD_REFINERY = actions.FUNCTIONS.Build_Refinery_screen.id
_BUILD_STARPORT = actions.FUNCTIONS.Build_Starport_screen.id
_BUILD_SUPPLY_DEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
_BUILD_TECHLAB = actions.FUNCTIONS.Build_TechLab_screen.id
_BUILD_REACTOR = actions.FUNCTIONS.Build_Reactor_screen.id

_TRAIN_BANSHEE = actions.FUNCTIONS.Train_Banshee_quick.id
_TRAIN_BATTLE_CRUISER = actions.FUNCTIONS.Train_Battlecruiser_quick.id
_TRAIN_CYCLONE = actions.FUNCTIONS.Train_Cyclone_quick.id
_TRAIN_GHOST = actions.FUNCTIONS.Train_Ghost_quick.id
_TRAIN_HELLION = actions.FUNCTIONS.Train_Hellion_quick.id
_TRAIN_LIBERATOR = actions.FUNCTIONS.Train_Liberator_quick.id
_TRAIN_MARAUDER = actions.FUNCTIONS.Train_Marauder_quick.id
_TRAIN_MARINE = actions.FUNCTIONS.Train_Marine_quick.id
_TRAIN_MEDIVAC = actions.FUNCTIONS.Train_Medivac_quick.id
_TRAIN_RAVEN = actions.FUNCTIONS.Train_Raven_quick.id
_TRAIN_REAPER = actions.FUNCTIONS.Train_Reaper_quick.id
_TRAIN_SCV = actions.FUNCTIONS.Train_SCV_quick.id
_TRAIN_SIEGE_TANK = actions.FUNCTIONS.Train_SiegeTank_quick.id
_TRAIN_VIKING = actions.FUNCTIONS.Train_VikingFighter_quick.id
_TRAIN_THOR = actions.FUNCTIONS.Train_Thor_quick.id

_NO_OP = actions.FUNCTIONS.no_op.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_ATTACK_MINIMAP = actions.FUNCTIONS.Attack_minimap.id
_HARVEST_GATHER = actions.FUNCTIONS.Harvest_Gather_screen.id

_NEUTRAL_VESPENE_GEYSER = 342
_NEUTRAL_MINERAL_FIELD = 341

_ARMORY = 29
_BARRACKS = 21
_FACTORY = 27
_FUSION_CORE = 30
_GHOST_ACADEMY = 26
_STARPORT = 28
_COMMAND_CENTER = 18
#_ENGINEERING_BAY = 22
_REFINERY = 20
_SUPPLY_DEPOT = 19
_TECHLAB = 5
#_BANSHEE = 55
#_BATTLE_CRUISER = 57
#_CYCLONE = 692
#_GHOST = 50
#_HELLION = 53
#_LIBERATOR = 689
#_MARAUDER = 51
_MARINE = 48
#_MEDIVAC = 54
#_RAVEN = 56
#_REAPER = 49
#_SIEGE_TANK = 33
#_THOR = 52
#_VIKING = 35
_SCV = 45
_REACTOR = 6

ACTION_DO_NOTHING = 'donothing'
ACTION_ATTACK = 'attack'

#ACTION_T_BANSHEE = 't_banshee'
#ACTION_T_BATTLECRUISER = 't_battlecruiser'
#ACTION_T_CYCLONE = 't_cyclone'
#ACTION_T_GHOST = 't_ghost'
#ACTION_T_HELLION = 't_hellion'
#ACTION_T_LIBERATOR = 't_liberator'
#ACTION_T_MARAUDER = 't_marauder'
ACTION_T_MARINE = 't_marine'
#ACTION_T_MEDIVAC = 't_medivac'
#ACTION_T_RAVEN = 't_raven'
#ACTION_T_REAPER = 't_reaper'
#ACTION_T_SIEGETANK = 't_siegetank'
ACTION_T_SCV = 't_scv'
#ACTION_T_VIKING = 't_viking'
#ACTION_T_THOR = 't_thor'

ACTION_B_ARMORY = 'b_armory'
ACTION_B_BARRACKS = 'b_barracks'
#ACTION_B_COMMANDCENTER = 'b_commandcenter'
ACTION_B_FACTORY = 'b_factory'
ACTION_B_FUSIONCORE ='b_fusioncore'
ACTION_B_GHOSTACADEMY = 'b_ghostacademy'
ACTION_B_REFINERY = 'b_refinery'
ACTION_B_STARPORT = 'b_starport'
ACTION_B_SUPPLYDEPOT = 'b_supplydepot'
ACTION_B_TECHLAB_BARRACKS = 'b_techlab_barracks'
#ACTION_B_TECHLAB_STARPORT = 'b_techlab_starport'
#ACTION_B_TECHLAB_FACTORY = 'b_techlab_factory'
ACTION_B_REACTOR_BARRACKS = 'b_reactor_barracks'
#ACTION_B_REACTOR_STARPORT = 'b_reactor_starport'
#ACTION_B_REACTOR_FACTORY = 'b_reactor_factory'

units_capable_of_attacking = [
	#'banshee',		
	#'battlecruiser',
	#'cyclone',		
	#'ghost',
	#'hellion',		
	#'liberator',
	#'marauder',		
	'marine'
	#'medivac',		
	#'raven',
	#'reaper', 		
	#'siegetank',
	#'viking',	
	#'thor'
]

unit_dict = {
	#'banshee': _BANSHEE,
	#'battlecruiser': _BATTLE_CRUISER,
	#'cyclone': _CYCLONE,
	#'ghost': _GHOST,
	#'hellion': _HELLION,
	#'liberator': _LIBERATOR,
	#'marauder': _MARAUDER,
	'marine': _MARINE,
	#'medivac': _MEDIVAC,
	#'raven': _RAVEN,
	#'reaper': _REAPER,
	#'siegetank': _SIEGE_TANK,
	'scv': _SCV,
	#'viking': _VIKING,
	#'thor': _THOR,
	'techlab': _TECHLAB,
	'supplydepot': _SUPPLY_DEPOT, 
	'starport': _STARPORT,
	'refinery': _REFINERY,
	'ghostacademy': _GHOST_ACADEMY,
	'fusioncore': _FUSION_CORE,
	'factory': _FACTORY,
	#'engineeringbay': _ENGINEERING_BAY,
	'commandcenter': _COMMAND_CENTER,
	'barracks': _BARRACKS,
	'armory': _ARMORY,
	'reactor': _REACTOR
}

build_to_action = {
	'barracks':_BUILD_BARRACKS, 
	'supplydepot':_BUILD_SUPPLY_DEPOT, 
	#'commandcenter':_BUILD_COMMAND_CENTER, 
	'refinery':_REFINERY,
	'ghostacademy':_BUILD_GHOST_ACADEMY, 
	'factory':_BUILD_FACTORY, 
	'armory':_BUILD_ARMORY, 
	'starport':_BUILD_STARPORT, 
	'fusioncore':_BUILD_FUSION_CORE, 
	'techlab': _BUILD_TECHLAB, 
	'reactor':_BUILD_REACTOR
}

unit_to_action = {
#'banshee':_TRAIN_BANSHEE,
#'battlecruiser':_TRAIN_BATTLE_CRUISER,
#'cyclone':_TRAIN_CYCLONE,
#'ghost':_TRAIN_GHOST,
#'hellion':_TRAIN_HELLION,
#'liberator':_TRAIN_LIBERATOR,
#'marauder':_TRAIN_MARAUDER,
'marine':_TRAIN_MARINE,
#'medivac':_TRAIN_MEDIVAC,
#'raven':_TRAIN_RAVEN,
#'reaper':_TRAIN_REAPER,
'scv':_TRAIN_SCV,
#'siegetank':_TRAIN_SIEGE_TANK,
#'viking':_TRAIN_VIKING,
#'thor':_TRAIN_THOR
}

building_sizes = {
'barracks': 12, 
'supplydepot': 9, 
'refinery': 11, 
'ghostacademy': 12, 
'factory': 12, 
'armory': 12, 
'starport': 12, 
'fusioncore': 12,
'techlab': 8,
'reactor': 8
}

Buildings = [_BARRACKS, _ARMORY, _REACTOR, _COMMAND_CENTER, _FACTORY,
			_FUSION_CORE, _GHOST_ACADEMY, _REFINERY, _STARPORT, _SUPPLY_DEPOT, _TECHLAB, 
			_NEUTRAL_MINERAL_FIELD, _NEUTRAL_VESPENE_GEYSER]

smart_actions = [	
	ACTION_DO_NOTHING, 			
	#ACTION_T_BANSHEE,			
	#ACTION_RETREAT,
	#ACTION_T_BATTLECRUISER, 	
	#ACTION_T_CYCLONE, 			
	#ACTION_T_GHOST,
	#ACTION_T_HELLION, 			
	#ACTION_T_LIBERATOR, 		
	#ACTION_T_MARAUDER,
	ACTION_T_MARINE, 			
	#ACTION_T_MEDIVAC,			
	#ACTION_T_RAVEN,
	#ACTION_T_REAPER,			
	#ACTION_T_SIEGETANK, 		
	#ACTION_T_SCV,
	#ACTION_T_VIKING,			
	#ACTION_T_THOR,				
	#ACTION_B_ARMORY,
	ACTION_B_BARRACKS,			
	#ACTION_B_COMMANDCENTER,		
	#ACTION_B_FACTORY,			
	#ACTION_B_GHOSTACADEMY,		
	ACTION_B_REFINERY,			
	#ACTION_B_STARPORT,			
	ACTION_B_SUPPLYDEPOT
	#ACTION_B_TECHLAB_FACTORY, 	
	#ACTION_B_TECHLAB_STARPORT, 	
	ACTION_B_TECHLAB_BARRACKS,
	#ACTION_B_REACTOR_FACTORY, 	
	#ACTION_B_REACTOR_STARPORT, 	
	ACTION_B_REACTOR_BARRACKS
]

## adds attack <which> quadrant actions and with <which> attacking unit
for mm_x in range(0, 64):
	for mm_y in range(0, 64):
		if (mm_x + 1) % 32 == 0 and (mm_y + 1) % 32 == 0:
			smart_actions.append(ACTION_ATTACK + '_' + str(mm_x - 16) + '_' + str(mm_y - 16))

class QLearningTable:
	def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
		self.round = 0
		self.actions = actions
		self.lr = learning_rate
		self.gamma = reward_decay
		self.epsilon = e_greedy
		self.q_table = pd.DataFrame(columns=self.actions)
		
		
		accum = open("acc_qtable.csv", "w+")
		name = "qtable.csv"
		if os.path.exists(name):
			self.q_table = pd.DataFrame(columns=self.actions).from_csv(name)
			#self.printTable()
		else:
			self.q_table = pd.DataFrame(columns=self.actions)


	def save_csv(self, name):
		self.round += 1
		self.q_table.to_csv(name)
		print("Saving")
		accum_f = open("acc_qtable.csv", "w")
		accum_f.write(str(self.q_table)+"\n")
		accum_f.write("Round: "+str(self.round)+"\n")



	def choose_action(self, observation):
		self.check_state_exist(observation)
		
		if np.random.uniform() < self.epsilon:
			# choose best action
			state_action = self.q_table.ix[observation, :]
			
			# some actions have the same value
			state_action = state_action.reindex(np.random.permutation(state_action.index))
			
			action = state_action.max()
		else:
			# choose random action
			action = np.random.choice(self.actions)
		return int(action)

	def printTable(self):
		print(self.q_table)
		
	def learn(self, s, a, r, s_):
		self.check_state_exist(s_)
		self.check_state_exist(s)

		q_predict = self.q_table.ix[s, a]
		#q_target = r + self.gamma * self.q_table.ix[s_, :].max()
		
		# update
		#self.q_table.ix[s, a] += self.lr * (q_target - q_predict)
		if s_ != 'terminal':
			q_target = r + self.gamma * self.q_table.ix[s_, :].max()
		else:
			q_target = r
		
		## update 
		self.q_table.ix[s, a] += self.lr * (q_target - q_predict)

	def check_state_exist(self, state):
		if state not in self.q_table.index:
			# append new state to q table

			self.q_table = self.q_table.append(pd.Series([0] * len(self.actions), index=self.q_table.columns, name=state))
			
class SwarmbotAgent(base_agent.BaseAgent):
	def __init__(self):
		super(SwarmbotAgent, self).__init__()
		self.round = 0 ## round number (games)
		self.rewardFile = open('rewards.csv', 'a+')
		self.rewardTotal = 0 # uhm... a reward win or loss, [1, 0]
		self.qlearn = QLearningTable(actions=list(range(len(smart_actions))))
		self.move_number = 0 ## what move in the smart action are we on
		#self.unit_coords = {} ## (x, y) coordinates for locating units
		self.unit_counts = {} ## counts of every unit , for state evaluation
		self.unit_types = None ## updated after every step with all units in the screen
		self.base_top_left = None ## location of self
		self.actions_taken = [(-1, [-1, -1])] ## actions that were returned to the base agent
		self.states_happened = [] ## states that yielded an action at a certain step 
		self.point_selected = None ## point in the screen currently selected. 
		self.depot_x = 5 ## starting x position used for finding locations for buildings
		self.depot_y = 5 ## starting y position used for finding locations for buildings


	## lent from https://github.com/jlboes/Starcraft-II-learning-bot/blob/master/src/scagent.py
	## credit to the creator, before using, update the self.unit_types
	def findLocationForBuilding(self, size, distance=6, chance=10):
		## start from mineral fields 
		mf_y, mf_x = (self.unit_types == _NEUTRAL_MINERAL_FIELD).nonzero()
		## obtain map limits 
		max_x, max_y = self.unit_types.shape
		while True:
			## selects random points where to place the building predetermined within radious of (5,5)
			s_target_x = int(self.depot_x + np.random.choice([-1,0,1], 1) * distance)
			s_target_y = int(self.depot_y + np.random.choice([-1,0,1], 1) * distance)
			## if the point fits in the screen 
			within_map = (0 < s_target_x < max_x - size) and (0 < s_target_y < max_y - size)
			## checks to see if there is space available for the building in between other buildings
			area = self.unit_types[s_target_y : s_target_y + 6][s_target_x : s_target_x + 6]
			space_available = not any(x in area for x in Buildings)
			## if the mineral fields are not in the way... idk if vespene geysers might need to be included as well
			within_mineral_field = (min(mf_y) < s_target_y < max(mf_y)) and (min(mf_x) < s_target_x < max(mf_x) + 11)
			chance += -1 
			## once you know that the building is within the map area
			## once you know that there is space available to place it in
			## and once you know that they're out of the mineral fields
			if within_map and space_available and not within_mineral_field:
				self.depot_y = s_target_y
				self.depot_x = s_target_x
				s_target = [s_target_x, s_target_y]
				break
			## increase the distance between
			## buildings after every 10 chances 
			## to find a place to put the building 
			if chance == 0:
				distance += 1
				chance = 10
			## wasnt sure if it could at somepoint 
			## stay in an infinite loop in case it 
			## never found a location
			if distance > 40:
				s_target = None
				break
		return s_target

	def get_current_state(self, obs, hot_squares):
		score_cumulative = list(obs.observation['score_cumulative'])
		player_info = list(obs.observation['player'])
		player_info = player_info[1:9] ## since we dont need player id or warpgate and larva counts 
		temp = score_cumulative + player_info
		for unit in build_to_action:
			if unit in self.unit_counts:
				temp.append(self.unit_counts[unit])
			else:
				temp.append(0)
		reversed_actions_taken = [self.actions_taken[i*-1][0] for i in range(1, len(self.actions_taken))]
		if len(reversed_actions_taken) < 15: 
			reversed_actions_taken = [0]*(15 - len(reversed_actions_taken)) + reversed_actions_taken
		else:
			reversed_actions_taken = reversed_actions_taken[:15]
		temp = temp + reversed_actions_taken
		temp.append(self.base_top_left)
		temp = temp + list(hot_squares)
		return temp

	def reset(self):
		super(SwarmbotAgent, self).reset()
		self.round += 1
		self.rewardFile = open("rewards.csv", "a+")
		self.rewardFile.write(str(self.round)+","+str(self.rewardTotal)+"\n")
		self.qlearn.save_csv("qtable.csv")

	def transformLocation(self, x, y):
		"""
			converts a location based on your location
		"""
		if not self.base_top_left:
			return [64 - x, 64 - y]
		return [x, y]

	def select_valid_SCV(self, unit_x, unit_y, obs):
		self.unit_types = obs.observation['screen'][_UNIT_TYPE]
		mf_y, mf_x = (self.unit_types == _NEUTRAL_MINERAL_FIELD).nonzero()
		if self.base_top_left:
			limit_x = max(mf_x) - 2
			limit_y = min(mf_y) + 2
		else:
			limit_x = min(mf_x) - 2
			limit_y = max(mf_y) + 2
		target = None
		for i in range(len(unit_y)):
			if self.base_top_left:
				if unit_y[i] > limit_y and unit_x[i] < limit_x:
					target = [unit_x[i], unit_y[i]]
					break
			else:
				if unit_y[i] < limit_y and unit_x[i] > limit_x:
					target = [unit_x[i], unit_y[i]]
					break
		return target

	def splitAction(self, action_id):
		"""
			splits action for location needed for selecting and attack location
			can also split to whether we are training or building a unit
		"""
		action = smart_actions[action_id]
		if 'attack' in action: ## if its an attack
			splitted = action.split('_')
			if len(splitted) == 4: ## unit specific attack
				action, x, y, unit = splitted
				return (action, x, y, unit, None)
			else:
				action, x, y = splitted
				return (action, x, y, None, None) ## attack with all units
		elif 'reactor' in action or 'techlab' in action: ## two main add-ons
			action, unit, attachment = action.split('_')
			return (action, None, None, unit, attachment)
		else:	## regular action (either build or train a unit)
			if action == 'donothing':
				return (None, None, None, None, None)
			else:
				action, unit = action.split('_')
				return (action, None, None, unit, None)

	def step(self, obs):
		super(SwarmbotAgent, self).step(obs)

		## begins by obtaining all the unit types available on the screen
		self.unit_types = obs.observation['screen'][_UNIT_TYPE]

		if obs.first():
			## obtains player location in the map
			player_y, player_x = (obs.observation['minimap'][_PLAYER_RELATIVE] == _PLAYER_SELF).nonzero()
			self.base_top_left = 1 if player_y.any() and player_y.mean() <= 31 else 0

			cc_y, cc_x = (self.unit_types == _COMMAND_CENTER).nonzero()
			self.unit_counts[_COMMAND_CENTER] = 1 if cc_y.any() else 0
			
			## loactes all unit types that are vespene geysers in the form x, y
			vg_y, vg_x = (self.unit_types == _NEUTRAL_VESPENE_GEYSER).nonzero()
			self.unit_counts[_NEUTRAL_VESPENE_GEYSER] = 2 if vg_y.any() else 0

			## locates all unit types that are mineral fields in the form x, y
			mf_y, mf_x = (self.unit_types == _NEUTRAL_MINERAL_FIELD).nonzero()
			self.unit_counts[_NEUTRAL_MINERAL_FIELD] = 1 if mf_y.any() else 0	

			self.workers_in_refinery = 0

			self.prev_state = None
			self.prev_action = None

			self.current_state = []

		if obs.last():
			self.reward = obs.reward
			self.qlearn.learn(str(self.prev_state), self.prev_action, self.reward, 'terminal')
			self.reset()
			self.prev_action = None
			self.prev_state = None
			self.move_number = 0

			## in states happened the 3 is terminal. 
			self.states_happened.append((self.prev_state, 3))
			self.actions_taken.append((_NO_OP, []))
			return actions.FunctionCall(_NO_OP, [])

		if self.move_number == 0:
			self.move_number += 1

			## obtains locations at which the enemy would appear. 
			hot_squares = np.zeros(4)
			enemy_y, enemy_x = (obs.observation['minimap'][_PLAYER_RELATIVE] == _PLAYER_HOSTILE).nonzero()
			for i in range(0, len(enemy_y)):
				y = int(math.ceil((enemy_y[i] + 1) / 32))
				x = int(math.ceil((enemy_x[i] + 1) / 32))
				hot_squares[((y-1)*2) + (x - 1)] = 1

			## inverts the map or not based on your location
			if not self.base_top_left:
				hot_squares = hot_squares[::-1]

			## from obs and counts obtain the current state to be used in the qtable
			self.current_state = self.get_current_state(obs, hot_squares)

			if self.prev_action is not None:
				self.qlearn.learn(str(self.prev_state), self.prev_action, 0, str(self.current_state))

			## use q table to learn previous action and to choose an action.
			new_action = self.qlearn.choose_action(str(self.current_state))


			self.prev_state = self.current_state 
			self.prev_action = new_action 

## ------------------------------------------------------------------------------------------------------------------- ##
## xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx ##
## ------------------------------------------------------------------------------------------------------------------- ##

			action, x, y, unit, attachment = self.splitAction(self.prev_action)

			if action == 'b' and unit == 'supplydepot' and _SELECT_POINT in obs.observation['available_actions']:
				self.unit_types = obs.observation['screen'][_UNIT_TYPE]
				unit_y, unit_x = (self.unit_types == _SCV).nonzero()
				if unit_y.any():
					temp = self.select_valid_SCV(unit_x, unit_y, obs)
					j = random.randint(0, len(unit_y) - 1)
					target = temp if temp is not None else [unit_x[j], unit_y[j]]
					self.point_selected = (target, 'scv')
					self.states_happened.append((self.prev_state, self.move_number))
					self.actions_taken.append((_SELECT_POINT, [_NOT_QUEUED, target]))
					return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])

			elif action == 'b' and unit == 'refinery' and _SELECT_POINT in obs.observation['available_actions']:
				self.unit_types = obs.observation['screen'][_UNIT_TYPE]
				unit_y, unit_x = (self.unit_types == _SCV).nonzero()
				if unit_y.any():
					temp = self.select_valid_SCV(unit_x, unit_y, obs)
					j = random.randint(0, len(unit_y) - 1)
					target = temp if temp is not None else [unit_x[j], unit_y[j]]
					self.point_selected = (target, 'scv')
					self.states_happened.append((self.prev_state, self.move_number))
					self.actions_taken.append((_SELECT_POINT, [_NOT_QUEUED, target]))
					return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])

			elif action == 'b' and unit == 'barracks' and _SELECT_POINT in obs.observation['available_actions']:
				self.unit_types = obs.observation['screen'][_UNIT_TYPE]
				unit_y, unit_x = (self.unit_types == _SCV).nonzero()
				if unit_y.any():
					temp = self.select_valid_SCV(unit_x, unit_y, obs)
					j = random.randint(0, len(unit_y) - 1)
					target = temp if temp is not None else [unit_x[j], unit_y[j]]
					self.point_selected = (target, 'scv')
					self.states_happened.append((self.prev_state, self.move_number))
					self.actions_taken.append((_SELECT_POINT, [_NOT_QUEUED, target]))
					return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])

			elif action == 't' and unit == 'marine' and _SELECT_POINT in obs.observation['available_actions']:
				self.unit_types = obs.observation['screen'][_UNIT_TYPE]
				unit_y, unit_x = (self.unit_types == _BARRACKS).nonzero()
				if unit_y.any():
					j = random.randint(0, len(unit_y) - 1)
					target = [unit_x[j], unit_y[j]]
					self.point_selected = (target, 'barracks')
					self.states_happened.append((self.prev_state, self.move_number))
					self.actions_taken.append((_SELECT_POINT, [_SELECT_ALL, target]))
					return actions.FunctionCall(_SELECT_POINT, [_SELECT_ALL, target])

			elif action == 'attack' and _SELECT_ARMY in obs.observation['available_actions']:
				self.select_point = (None, 'army')
				self.states_happened.append((self.prev_state, self.move_number))
				self.actions_taken.append((_SELECT_ARMY, [_NOT_QUEUED]))
				return actions.FunctionCall(_SELECT_ARMY, [_NOT_QUEUED])

			



## ------------------------------------------------------------------------------------------------------------------- ##
## xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx ##
## ------------------------------------------------------------------------------------------------------------------- ##

		if self.move_number == 1:
			self.move_number += 1

			action, x, y, unit, attachment = self.splitAction(self.prev_action)

			if action == 'b' and unit == 'supplydepot' and _BUILD_SUPPLY_DEPOT in obs.observation['available_actions']:
				target = self.findLocationForBuilding(building_sizes['supplydepot'])
				if self.point_selected[1] == 'scv' and target is not None:
					self.point_selected = None
					if _SUPPLY_DEPOT in self.unit_counts and self.unit_counts[_SUPPLY_DEPOT] <= 5:
						self.unit_counts[_SUPPLY_DEPOT] += 1
						self.states_happened.append((self.prev_state, self.move_number))
						self.actions_taken.append((_BUILD_SUPPLY_DEPOT, [_NOT_QUEUED, target]))
						return actions.FunctionCall(_BUILD_SUPPLY_DEPOT, [_NOT_QUEUED, target])
					else:
						self.unit_counts[_SUPPLY_DEPOT] = 1
						self.states_happened.append((self.prev_state, self.move_number))
						self.actions_taken.append((_BUILD_SUPPLY_DEPOT, [_NOT_QUEUED, target]))
						return actions.FunctionCall(_BUILD_SUPPLY_DEPOT, [_NOT_QUEUED, target])

			elif action == 'b' and unit == 'refinery' and _BUILD_REFINERY in obs.observation['available_actions']:
				self.unit_types = obs.observation['screen'][_UNIT_TYPE]
				unit_y, unit_x = (self.unit_types == _NEUTRAL_VESPENE_GEYSER).nonzero()
				if unit_y.any():
					i = random.randint(0, len(unit_y) - 1)
					target = [unit_x[i], unit_y[i]]
					self.point_selected = None
					if _REFINERY in self.unit_counts and self.unit_counts[_REFINERY] <= 2:
						self.unit_counts[_SUPPLY_DEPOT] += 1
						self.states_happened.append((self.prev_state, self.move_number))
						self.actions_taken.append((_BUILD_REFINERY, [_NOT_QUEUED, target]))
						return actions.FunctionCall(_BUILD_REFINERY, [_NOT_QUEUED, target])
					else:
						self.unit_counts[_SUPPLY_DEPOT] = 1
						self.states_happened.append((self.prev_state, self.move_number))
						self.actions_taken.append((_BUILD_REFINERY, [_NOT_QUEUED, target]))
						return actions.FunctionCall(_BUILD_REFINERY, [_NOT_QUEUED, target])

			elif action == 'b' and unit == 'barracks' and _BUILD_BARRACKS in obs.observation['available_actions']:
				target = self.findLocationForBuilding(building_sizes['barracks'])
				if self.point_selected[1] == 'scv' and target is not None:
					self.point_selected = None
					if _BARRACKS in self.unit_counts and self.unit_counts[_BARRACKS] <= 4:
						self.unit_counts[_BARRACKS] += 1
						self.states_happened.append((self.prev_state, self.move_number))
						self.actions_taken.append((_BUILD_BARRACKS, [_NOT_QUEUED, target]))
						return actions.FunctionCall(_BUILD_BARRACKS, [_NOT_QUEUED, target])
					else:
						self.unit_counts[_BARRACKS] = 1
						self.states_happened.append((self.prev_state, self.move_number))
						self.actions_taken.append((_BUILD_BARRACKS, [_NOT_QUEUED, target]))
						return actions.FunctionCall(_BUILD_BARRACKS, [_NOT_QUEUED, target])

			elif action == 't' and unit == 'marine' and _TRAIN_MARINE in obs.observation['available_actions']:
				self.select_point = None
				self.states_happened.append((self.prev_state, self.move_number))
				self.actions_taken.append((_TRAIN_MARINE, [_QUEUED]))
				return actions.FunctionCall(_TRAIN_MARINE, [_QUEUED])

			elif action == 'attack' and _ATTACK_MINIMAP in obs.observation['available_actions']:
				do_it = True
				if len(obs.observation['single_select']) > 0 and obs.observation['single_select'][0][0] == _SCV:
					do_it = False
				if len(obs.observation['multi_select']) > 0 and obs.observation['multi_select'][0][0] == _SCV:
					do_it = False
				if do_it and _ATTACK_MINIMAP in obs.observation["available_actions"]:
					x_offset = random.randint(-1, 1)
					y_offset = random.randint(-1, 1)

					target = self.transformLocation(int(x) + (x_offset * 8), int(y) + (y_offset * 8))

					self.select_point = None
					self.states_happened.append((self.prev_state, self.move_number))
					self.actions_taken.append((_ATTACK_MINIMAP, [_NOT_QUEUED, target]))
					return actions.FunctionCall(_ATTACK_MINIMAP, [_NOT_QUEUED, target])


## ------------------------------------------------------------------------------------------------------------------- ##
## xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx ##
## ------------------------------------------------------------------------------------------------------------------- ##

		if self.move_number == 2:
			self.move_number = 0

			action, x, y, unit, attachment = self.splitAction(self.prev_action)

			if action == 'b' and unit != 'refinery' and _HARVEST_GATHER in obs.observation['available_actions']:
				self.unit_types = obs.observation['screen'][_UNIT_TYPE]
				unit_y, unit_x = (self.unit_types == _NEUTRAL_MINERAL_FIELD).nonzero()
				if unit_y.any():
					i = random.randint(0, len(unit_y) - 1)
					target = [int(unit_x[i]), int(unit_y[i])]
					self.states_happened.append((self.prev_state, self.move_number))
					self.actions_taken.append((_HARVEST_GATHER, [_NOT_QUEUED, target]))
					return actions.FunctionCall(_HARVEST_GATHER, [_QUEUED, target])

## ------------------------------------------------------------------------------------------------------------------- ##
## xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx ##
## ------------------------------------------------------------------------------------------------------------------- ##

		return actions.FunctionCall(_NO_OP, [])


