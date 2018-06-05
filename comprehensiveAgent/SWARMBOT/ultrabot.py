import random
import math
import os

import numpy as np
import pandas as pd

from collections import deque

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

## import tags, which equate to 
## labels for unit names, and thier 
## ids didn't want to have all those
## assignments in the bot file
from tags import *

## given two arrays of coords returns number of pixels per unit.
from countUnits import count_units

## adds attack <which> quadrant actions and with <which> attacking unit
for mm_x in range(0, 64):
	for mm_y in range(0, 64):
		##for u in units_capable_of_attacking:
		##	if (mm_x + 1) % 32 == 0 and (mm_y + 1) % 32 == 0:
		##		smart_actions.append(ACTION_ATTACK + '_' + str(mm_x - 16) + '_' + str(mm_y - 16) + u)
		if (mm_x + 1) % 32 == 0 and (mm_y + 1) % 32 == 0:
			smart_actions.append(ACTION_ATTACK + '_' + str(mm_x - 16) + '_' + str(mm_y - 16))

"""
	Main Agent Class:
		This bot specifically focuses on build order prediction. From a Qtable it will obtain 
		the action with most probability to be done at a given state in the game. Currently, we are
		trying to implement the build order for mobile, air, and ground units. (this including buildings,
		workers, and attacking units). We hard-code the actions but the agent chooses what action to take
		at each given state. Our first approach is simply to get the bot running using the qtable alone. 
		as inplemented by: 
			https://github.com/skjb/pysc2-tutorial/blob/master/Refining%20the%20Sparse%20Reward%20Agent/refined_agent.py
		The code implements certain aspects of the agent differently from the one by 'skjb'. but not a huge difference. Just 
		a broader application for more actions, also facilitates the addition of newer actions to th smart actions array.  
		The second part after the Qtable implementation is completed is to use the current states that we had been passing 
		to the Qtable as indexes as actual inputs to a Recurrent Neural Network, so that the agent can learn from a sequence
		of moves that it has done throughout periods of or the entirety of the game. The current state is being defined by
		unit counts and global state evealuation of economy at the moment, we are also thinking of adding enemy info when 
		visible, in order to learn better and adapt to enemy strategies.

"""
class SwarmbotAgent(base_agent.BaseAgent):
	def __init__(self):
		super(SwarmbotAgent, self).__init__()

		self.reward = 0 # uhm... a reward win or loss, [1, 0]
		self.qlearn = None ## Nothing yet
		self.move_number = 0 ## what move in the smart action are we on
		self.unit_sizes = {} ## pixel sizes of each unit used to compute counts
		self.unit_coords = {} ## (x, y) coordinates for locating units
		self.unit_counts = {} ## counts of every unit , for state evaluation
		self.unit_types = None ## updated after every step with all units in the screen
		self.base_top_left = None ## location of self
		self.action_queue = deque() ## if an action has requirements, queue it for later
		self.actions_taken = [] ## actions that were returned to the base agent
		self.states_happened = [] ## states that yielded an action at a certain step 
		self.wait_2_count = deque() ## queues those units that require to be counted
		self.point_selected = (None, None) ## point in the screen currently selected. 
		self.depot_x = 5 ## starting x position used for finding locations for buildings
		self.depot_y = 5 ## starting y position used for finding locations for buildings


	def transfromDistance(self, x, x_distance, y, y_distance):
		"""
			converts a distance based on your location
		"""
		if not self.base_top_left:
			return [x - x_distance, y - y_distance]
		return [x + x_distance, y + y_distance]

	def transformLocation(self, x, y):
		"""
			converts a location based on your location
		"""
		if not self.base_top_left:
			return [64 - x, 64 - y]
		return [x, y]

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
			return (action, x, y, None, None) ## attack with all units
		elif 'reactor' in action or 'techlab' in action: ## two main add-ons
			action, unit, attachment = action.split('_')
			return (action, None, None, unit, attachment)
		else:	## regular action (either build or train a unit)
			action, unit = action.split('_')
			return (action, None, None, unit, None)

	## lent from https://github.com/jlboes/Starcraft-II-learning-bot/blob/master/src/scagent.py
	## credit to the creator, before using, update the self.unit_types
	def findLocationForBuilding(self, size_of_unit, distance=6, chance=10):
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
			within_mineral_field = (min(mf_y) < s_target_y < max(mf_y)) and (min(mf_x) < s_target_x < max(mf_x))
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
			if distance > 20:
				s_target = [-1, -1]
		return s_target


	def apply_counts(self, unit_name=None):
		"""
			applies the count to units as they are created. 
			main part of this is to check if sizes of units 
			have been seen, otherwise these will be updated 
			later. 
		"""
		## this if is only supposed to be done at the beginning of every game
		if not self.unit_counts:
			## locates all unit types that are command centers in the form x, y
			cc_y, cc_x = (self.unit_types == _COMMAND_CENTER).nonzero()
			self.unit_sizes[_COMMAND_CENTER] = len(cc_x)
			self.unit_coords[_COMMAND_CENTER] = [cc_x, cc_y]
			self.unit_counts[_COMMAND_CENTER] = 1 if cc_y.any() else 0
			
			## loactes all unit types that are vespene geysers in the form x, y
			vg_y, vg_x = (self.unit_types == _NEUTRAL_VESPENE_GEYSER).nonzero()
			self.unit_sizes[_NEUTRAL_VESPENE_GEYSER] = len(vg_x)/2 ## two geysers
			self.unit_coords[_NEUTRAL_VESPENE_GEYSER] = [vg_x, vg_y]
			self.unit_counts[_NEUTRAL_VESPENE_GEYSER] = 2 if vg_y.any() else 0

			## locates all unit types that are mineral fields in the form x, y
			mf_y, mf_x = (self.unit_types == _NEUTRAL_MINERAL_FIELD).nonzero()
			self.unit_sizes[_NEUTRAL_MINERAL_FIELD] = 1 ## doesnt matter for now
			self.unit_coords[_NEUTRAL_MINERAL_FIELD] = [vg_x, vg_y]
			self.unit_counts[_NEUTRAL_MINERAL_FIELD] = 1 if vg_y.any() else 0
		## either queues a count for the update step or it increases the count of a unit
		if unit_name is not None:
			unit_y, unit_x = (self.unit_types == self.unit_dict[unit_name]).nonzero()
			## if we still dont know the size of the unit place it in a queue to count later
			if unit_y.any() is None or self.unit_dict[unit_name] not in self.unit_sizes:
				self.wait_2_count.append(unit_name)
			else:
				## increases the count by one for every action to train or build
				## in some situations, we might be training more than 1 unit at a
				## time, but for now we will leave it like so. When we do a full 
				## count this will be fixed by itself
				self.unit_counts[self.unit_dict[unit_name]] += 1
		

	def update_counts(self):
		"""
			Updates counts at the end of every step of the game if necessary. It would update counts
			only if we had just completed a battle. meaning we are counting our loses and the remaining
			units we have now. 
			The first while loop gets the sies for newly seen and created units so that we can count later on
		"""
		## first we need to create the counts, sizes and coords for the queued units
		not_yet_built = deque()
		while(len(self.wait_2_count) != 0):
			unit_name = self.wait_2_count.popLeft()
			unit_x, unit_y = (self.unit_types == self.unit_dict[unit_name]).nonzero()
			if unit_y.any():
				## gets the pixel size of every unit in the waiting queue
				self.unit_sizes[self.unit_dict[unit_name]] = count_units(unit_x, unit_y)
				self.unit_counts[self.unit_dict[unit_name]] = int(math.ceil(len(unit_y) / self.unit_sizes[self.unit_dict[unit_name]]))
			else: ## those that were just popped out will bw placed back since they havent been built
				not_yet_built.append(unit_name)
		self.wait_2_count = deque(not_yet_built)
		## after we have been in a battle only
		if _ATTACK_MINIMAP == self.actions_taken[-1][0]:
			for unit_id in self.unit_sizes:
				unit_y, _ = (self.unit_types == unit_id).nonzero()
				if unit_y.any():
					self.unit_counts[unit_id] = int(math.ceil(len(unit_y) / self.unit_sizes[unit_id]))
				else:
					self.unit_counts[unit_id] = 0

	def step(self, obs):
		super(SwarmbotAgent, self).step(obs)

		## begins by obtaining all the unit types available on the screen
		self.unit_types = obs.observation['screen'][_UNIT_TYPE]
		## updates counts if necessary for the unit types that are visible
		self.update_counts()

		if obs.last():
			self.reward = obs.reward
			self.prev_action = None
			self.prev_state = None
			self.move_number = 0
			self.action_queue.clear()

			## in states happened the 3 is terminal. 
			self.states_happened.append((prev_state, 3))
			self.actions_taken.append((_NO_OP, []))
			return actions.FunctionCall(_NO_OP, [])

		if obs.first():
			## obtains player location in the map
			player_y, player_x = (obs.observation['minimap'][_PLAYER_RELATIVE] == _PLAYER_SELF).nonzero()
			self.base_top_left = 1 if player_y.any() and player_y.mean() <= 31 else 0	
			## applies initial counts and locations to command centers, vespene geysers and mineral fields
			self.apply_counts()

		if self.move_number == 0:
			self.move_number += 1

			## from obs and counts obtain the current state to be used in the qtable

			## obtains locations at which the enemy would appear. 
			hot_squares = np.zeros(4)
			enemy_y, enemy_x = (obs.observation['minimap'][_PLAYER_RELATIVE] == _PLAYER_HOSTILE).nonzero()
			for i in rane(0, len(enemy_y)):
				y = int(math.ceil((enemy_y[i] + 1) / 32))
				x = int(math.ceil((enemy_x[i] + 1) / 32))
				hot_squares[((y-1)*2) + (x - 1)] = 1

			## inverts the map or not based on your location
			if not self.base_top_left:
				hot_squares = hot_squares[::-1]

			## adds enemy locations to the current state. 

			## use q table to learn previous action and to choose an action. 

			##self.prev_state = current_state 
			##self.prev_action = new_action 

			action, x, y, unit, attachment = self.splitAction(self.prev_action)

			self.point_selected = (None, None)

			## Building creation ::

			if action == 'b' and unit in build_with_SCV: ## make barracks
				unit_y, unit_x = (self.unit_types == _SCV).nonzero()
				if unit_y.any():
					i = random.randint(0, len(unit_y) - 1)
					target = [unit_x[i], unit_y[i]]
					self.point_selected = (target, 'scv')
					self.states_happened.append((self.prev_state, self.move_number))
					self.actions_taken.append((_SELECT_POINT, [_NOT_QUEUED, target]))
					return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])

			elif action == 'b' and (unit == 'techlab' or unit == 'reactor'):
				unit_y, unit_x = (self.unit_types == self.unit_dict[attachment]).nonzero()
				if unit_y.any():
					i = random.randint(0, len(unit_y) - 1)
					target = [unit_x[i], unit_y[i]]
					self.point_selected = (target, attachment)
					self.states_happened.append((self.prev_state, self.move_number))
					self.actions_taken.append((_SELECT_POINT, [_NOT_QUEUED, target]))
					return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])

			## Training units ::

			elif action == 't' and unit == 'scv':
				unit_y, unit_x = (self.unit_types == _COMMAND_CENTER).nonzero()
				if unit_y.any():
					i = random.randint(0, len(unit_y) - 1)
					target = [unit_x[i], unit_y[i]]
					self.point_selected = (target, 'commandcenter')
					self.states_happened.append((self.prev_state, self.move_number))
					self.actions_taken.append((_SELECT_POINT, [_NOT_QUEUED, target]))
					return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])

			elif action == 't' and unit in starport_units:
				unit_y, unit_x = (self.unit_types == _STARPORT).nonzero()
				if unit_y.any():
					i = random.randint(0, len(unit_y) - 1)
					target = [unit_x[i], unit_y[i]]
					self.point_selected = (target, 'starport')
					self.states_happened.append((self.prev_state, self.move_number))
					self.actions_taken.append((_SELECT_POINT, [_NOT_QUEUED, target]))
					return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])


			elif action == 't' and unit in barracks_units:
				unit_y, unit_x = (self.unit_types == _BARRACKS).nonzero()
				if unit_y.any():
					i = random.randint(0, len(unit_y) - 1)
					target = [unit_x[i], unit_y[i]]
					self.point_selected = (target, 'barracks')
					self.states_happened.append((self.prev_state, self.move_number))
					self.actions_taken.append((_SELECT_POINT, [_NOT_QUEUED, target]))
					return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])


			elif action == 't' and unit in factory_units:
				unit_y, unit_x = (self.unit_types == _FACTORY).nonzero()
				if unit_y.any():
					i = random.randint(0, len(unit_y) - 1)
					target = [unit_x[i], unit_y[i]]
					self.point_selected = (target, 'factory')
					self.states_happened.append((self.prev_state, self.move_number))
					self.actions_taken.append((_SELECT_POINT, [_NOT_QUEUED, target]))
					return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])

			## send out attack... might add unit specific

			elif action == 'attack' and _SELECT_ARMY in obs.observation['available_actions']:
				self.states_happened.append((self.prev_state, self.move_number))
				self.actions_taken.append((_SELECT_ARMY, [_NOT_QUEUED]))
				return actions.FunctionCall(_SELECT_ARMY, )


		elif self.move_number == 1:
			self.move_number += 1

			action, x, y, unit, attachment = self.splitAction(self.prev_action)

			if action == 'b' and unit == 'refinery': ## make refinery 
				unit_y, unit_x = (self.unit_types == _NEUTRAL_VESPENE_GEYSER).nonzero()
				if unit_y.any():
					i = random.randint(0, len(unit_y) - 1)
					target = [unit_x[i], unit_y[i]]
					self.states_happened.append((self.prev_state, self.move_number))
					self.actions_taken.append((_BUILD_REFINERY, [_NOT_QUEUED, target]))
					return actions.FunctionCall(_BUILD_REFINERY, [_NOT_QUEUED, target])

			elif action == 'b' and (unit == 'techlab' or unit == 'reactor'): ## place add-on
				unit_y, unit_x = (self.unit_types == _SCV).nonzero()
				if self.point_selected is not (None, None):
					target = self.point_selected[0]
					if self.point_selected[1] != 'scv':
						## if we ppreviously didnt select scvs
						self.point_selected = (None, None)
						self.states_happened.append((self.prev_state, self.move_number))
						self.actions_taken.append((_BUILD_TECHLAB, [_NOT_QUEUED, target]))
						return actions.FunctionCall(_BUILD_TECHLAB, [_NOT_QUEUED, target])

			## will compress later
			elif action == 'b' and (unit in build_with_SCV and unit != 'refinery'): ## make barracks
				
				if unit == 'armory':
					if self.unit_dict[unit] in self.unit_counts:
						count = self.unit_counts[self.unit_dict[unit]]
						if count < 2:
							size = int(math.ceil(math.sqrt(self.unit_sizes[self.unit_dict[unit]])))
							target = self.findLocationForBuilding(size)
							if target is not [-1, -1]:
								self.apply_counts(unit)
								self.states_happened.append((self.prev_state, self.move_number))
								self.actions_taken.append((_BUILD_ARMORY, [_NOT_QUEUED, target]))
								return actions.FunctionCall(_BUILD_ARMORY, [_NOT_QUEUED, target])
					else:
						guess = 150
						target = self.findLocationForBuilding(guess)
						if target is not [-1, -1]
							self.apply_counts(unit)
							self.states_happened.append((self.prev_state, self.move_number))
							self.actions_taken.append((_BUILD_ARMORY, [_NOT_QUEUED, target]))
							return actions.FunctionCall(_BUILD_ARMORY, [_NOT_QUEUED, target])


				elif unit == 'barracks':
					if self.unit_dict[unit] in self.unit_counts:
						count = self.unit_counts[self.unit_dict[unit]]
						if count < 4:
							size = int(math.ceil(math.sqrt(self.unit_sizes[self.unit_dict[unit]])))
							target = self.findLocationForBuilding(size)
							if target is not [-1, -1]:
								self.apply_counts(unit)
								self.states_happened.append((self.prev_state, self.move_number))
								self.actions_taken.append((_BUILD_BARRACKS, [_NOT_QUEUED, target]))
								return actions.FunctionCall(_BUILD_BARRACKS, [_NOT_QUEUED, target])
					else:
						guess = 150
						target = self.findLocationForBuilding(guess)
						if target is not [-1, -1]
							self.apply_counts(unit)
							self.states_happened.append((self.prev_state, self.move_number))
							self.actions_taken.append((_BUILD_BARRACKS, [_NOT_QUEUED, target]))
							return actions.FunctionCall(_BUILD_BARRACKS, [_NOT_QUEUED, target])

				elif unit == 'factory': 
					if self.unit_dict[unit] in self.unit_counts:
						count = self.unit_counts[self.unit_dict[unit]]
						if count < 2:
							size = int(math.ceil(math.sqrt(self.unit_sizes[self.unit_dict[unit]])))
							target = self.findLocationForBuilding(size)
							if target is not [-1, -1]:
								self.apply_counts(unit)
								self.states_happened.append((self.prev_state, self.move_number))
								self.actions_taken.append((_BUILD_FACTORY, [_NOT_QUEUED, target]))
								return actions.FunctionCall(_BUILD_FACTORY, [_NOT_QUEUED, target])
					else:
						guess = 150
						target = self.findLocationForBuilding(guess)
						if target is not [-1, -1]
							self.apply_counts(unit)
							self.states_happened.append((self.prev_state, self.move_number))
							self.actions_taken.append((_BUILD_FACTORY, [_NOT_QUEUED, target]))
							return actions.FunctionCall(_BUILD_FACTORY, [_NOT_QUEUED, target])

				elif unit == 'fusioncore':
					if self.unit_dict[unit] in self.unit_counts:
						count = self.unit_counts[self.unit_dict[unit]]
						if count < 2:
							size = int(math.ceil(math.sqrt(self.unit_sizes[self.unit_dict[unit]])))
							target = self.findLocationForBuilding(size)
							if target is not [-1, -1]:
								self.apply_counts(unit)
								self.states_happened.append((self.prev_state, self.move_number))
								self.actions_taken.append((_BUILD_FUSION_CORE, [_NOT_QUEUED, target]))
								return actions.FunctionCall(_BUILD_FUSION_CORE, [_NOT_QUEUED, target])
					else:
						guess = 150
						target = self.findLocationForBuilding(guess)
						if target is not [-1, -1]
							self.apply_counts(unit)
							self.states_happened.append((self.prev_state, self.move_number))
							self.actions_taken.append((_BUILD_FUSION_CORE, [_NOT_QUEUED, target]))
							return actions.FunctionCall(_BUILD_FUSION_CORE, [_NOT_QUEUED, target])

				elif unit == 'ghostacademy':
					if self.unit_dict[unit] in self.unit_counts:
						count = self.unit_counts[self.unit_dict[unit]]
						if count < 2:
							size = int(math.ceil(math.sqrt(self.unit_sizes[self.unit_dict[unit]])))
							target = self.findLocationForBuilding(size)
							if target is not [-1, -1]:
								self.apply_counts(unit)
								self.states_happened.append((self.prev_state, self.move_number))
								self.actions_taken.append((_BUILD_GHOST_ACADEMY, [_NOT_QUEUED, target]))
								return actions.FunctionCall(_BUILD_GHOST_ACADEMY, [_NOT_QUEUED, target])
					else:
						guess = 150
						target = self.findLocationForBuilding(guess)
						if target is not [-1, -1]
							self.apply_counts(unit)
							self.states_happened.append((self.prev_state, self.move_number))
							self.actions_taken.append((_BUILD_GHOST_ACADEMY, [_NOT_QUEUED, target]))
							return actions.FunctionCall(_BUILD_GHOST_ACADEMY, [_NOT_QUEUED, target])

				elif unit == 'starport':
					if self.unit_dict[unit] in self.unit_counts:
						count = self.unit_counts[self.unit_dict[unit]]
						if count < 2:
							size = int(math.ceil(math.sqrt(self.unit_sizes[self.unit_dict[unit]])))
							target = self.findLocationForBuilding(size)
							if target is not [-1, -1]:
								self.apply_counts(unit)
								self.states_happened.append((self.prev_state, self.move_number))
								self.actions_taken.append((_BUILD_STARPORT, [_NOT_QUEUED, target]))
								return actions.FunctionCall(_BUILD_STARPORT, [_NOT_QUEUED, target])
					else:
						guess = 150
						target = self.findLocationForBuilding(guess)
						if target is not [-1, -1]
							self.apply_counts(unit)
							self.states_happened.append((self.prev_state, self.move_number))
							self.actions_taken.append((_BUILD_STARPORT, [_NOT_QUEUED, target]))
							return actions.FunctionCall(_BUILD_STARPORT, [_NOT_QUEUED, target])

				elif unit == 'supplydepot':
					if self.unit_dict[unit] in self.unit_counts:
						count = self.unit_counts[self.unit_dict[unit]]
						if count < 5:
							size = int(math.ceil(math.sqrt(self.unit_sizes[self.unit_dict[unit]])))
							target = self.findLocationForBuilding(size)
							if target is not [-1, -1]:
								self.apply_counts(unit)
								self.states_happened.append((self.prev_state, self.move_number))
								self.actions_taken.append((_BUILD_SUPPLY_DEPOT, [_NOT_QUEUED, target]))
								return actions.FunctionCall(_BUILD_SUPPLY_DEPOT, [_NOT_QUEUED, target])
					else:
						guess = 150
						target = self.findLocationForBuilding(guess)
						if target is not [-1, -1]
							self.apply_counts(unit)
							self.states_happened.append((self.prev_state, self.move_number))
							self.actions_taken.append((_BUILD_SUPPLY_DEPOT, [_NOT_QUEUED, target]))
							return actions.FunctionCall(_BUILD_SUPPLY_DEPOT, [_NOT_QUEUED, target])

				## elif unit == 'commandcenter': ## will not be implemented yet 

			## traing  units ::

			## might expand idk yet
			elif action == 't' and self.point_selected is not (None, None):
				if unit_to_action[unit] in obs.observation['available_actions']:
					self.states_happened.append((self.prev_state, self.move_number))
					self.actions_taken.append((unit_to_action[unit], [_QUEUED]))
					return actions.FunctionCall(unit_to_action[unit], [_QUEUED])

			## actually attack

			elif action == 'attack':
				do_it = True
				
				if len(obs.observation['single_select']) > 0 and obs.observation['single_select'][0][0] == _SCV:
					do_it = False
				
				if len(obs.observation['multi_select']) > 0 and obs.observation['multi_select'][0][0] == _SCV:
					do_it = False
				
				if do_it and _ATTACK_MINIMAP in obs.observation["available_actions"]:
					x_offset = random.randint(-1, 1)
					y_offset = random.randint(-1, 1)
					
					return actions.FunctionCall(_ATTACK_MINIMAP, [_NOT_QUEUED, self.transformLocation(int(x) + (x_offset * 8), int(y) + (y_offset * 8))])
				

		elif self.move_number == 2:
			self.move_number = 0

			action, x, y, unit, attachment = self.splitAction(self.prev_action)

			## returns idle scvs to mineral harvesting 
			if action == 'b' and unit in build_with_SCV:
				if _HARVEST_GATHER in obs.observation['available_actions']:
                    unit_y, unit_x = (unit_type == _NEUTRAL_MINERAL_FIELD).nonzero()
                    if unit_y.any():
                        i = random.randint(0, len(unit_y) - 1)
                        target = [int(unit_x[i]), int(unit_y[i])]
                        self.states_happened.append((self.prev_state, self.move_number))
						self.actions_taken.append((_HARVEST_GATHER, [_NOT_QUEUED, target]))
                        return actions.FunctionCall(_HARVEST_GATHER, [_QUEUED, target])

            ## at this point you can also add research actions... 

		self.states_happened.append((self.prev_state, self.move_number))
		self.actions_taken.append((_NO_OP, []))
		return actions.FunctionCall(_NO_OP, [])



