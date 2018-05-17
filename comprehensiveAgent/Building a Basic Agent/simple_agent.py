from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

import time

#The semantic meaning of these actions can mainly be found by searching:
# http://liquipedia.net/starcraft2/ or http://starcraft.wikia.com/ .
# Functions
_BUILD_BARRACKS = actions.FUNCTIONS.Build_Barracks_screen.id
_BUILD_SUPPLYDEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
_NOOP = actions.FUNCTIONS.no_op.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id
#For marines. 
_TRAIN_MARINE = actions.FUNCTIONS.Train_Marine_quick.id
_RALLY_UNITS_MINIMAP = actions.FUNCTIONS.Rally_Units_minimap.id
#For attacking
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_ATTACK_MINIMAP = actions.FUNCTIONS.Attack_minimap.id


#index: Index refers to layer into the set of layers.
#Functions found in features.py 
# Features
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
#Player relative is an array that contains a list of units relative to current player
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index

# Unit IDs
_TERRAN_BARRACKS = 21
_TERRAN_COMMANDCENTER = 18
_TERRAN_SUPPLYDEPOT = 19
_TERRAN_SCV = 45

# Parameters
_PLAYER_SELF = 1
_SUPPLY_USED = 3
_SUPPLY_MAX = 4
_NOT_QUEUED = [0]
_QUEUED = [1]

class SimpleAgent(base_agent.BaseAgent):
    #The mini map is 64 units across and 64 units tall, with (0, 0) being the top left coordinate
    #But the screen is 84*84 "units". 
    base_top_left = None
    #To track SCV
    supply_depot_built = False
    scv_selected = False
    #To track barrack construction
    barracks_built = False
    barracks_selected = False
    barracks_rallied = False
    #tracking army control.
    army_selected = False
    army_rallied = False

    def transformLocation(self, x, x_distance, y, y_distance):
        #Helper method to work with locations relative to our base. 
        #Here x and y are initial coordinates and x_distance and y_distance is where we want our selected point to be. 
        if not self.base_top_left:
            return [x - x_distance, y - y_distance]
        
        return [x + x_distance, y + y_distance]
    
    def step(self, obs): #step method. 
        super(SimpleAgent, self).step(obs)
        
        time.sleep(0.5)
        
        # Find all units that belong to the current player by taking mean of their coordinates. 
        if self.base_top_left is None:
            player_y, player_x = (obs.observation["minimap"][_PLAYER_RELATIVE] == _PLAYER_SELF).nonzero()
            self.base_top_left = player_y.mean() <= 31
            
        if not self.supply_depot_built:
            if not self.scv_selected:
                #First get x and y coordinate of all SCV units on the screen.
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_SCV).nonzero()
                #Then select first 
                target = [unit_x[0], unit_y[0]]
                
                self.scv_selected = True
                #Call function will instruct the game to "click" mouse at the SCV's location.
                return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
            
            #After we have selected th SCV, now we want to build the supply depot. 
            elif _BUILD_SUPPLYDEPOT in obs.observation["available_actions"]:
                
                #Get location of the command center 
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_COMMANDCENTER).nonzero()
                
                target = self.transformLocation(int(unit_x.mean()), 0, int(unit_y.mean()), 20)
                
                self.supply_depot_built = True
                
                return actions.FunctionCall(_BUILD_SUPPLYDEPOT, [_NOT_QUEUED, target])
            
         #Building barrack is similar to supply depot. Except we want barrack to the right of the command center. 
        elif not self.barracks_built:
            if _BUILD_BARRACKS in obs.observation["available_actions"]:
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_COMMANDCENTER).nonzero()
                
                target = self.transformLocation(int(unit_x.mean()), 20, int(unit_y.mean()), 0)
                
                self.barracks_built = True
                
                return actions.FunctionCall(_BUILD_BARRACKS, [_NOT_QUEUED, target])
       
    #Before we train any marines, we should set the rally point of the barracks to the top of our ramp 
    #so we can defend ourselves until we have enough units to move out:
    elif not self.barracks_rallied:
            if not self.barracks_selected:
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_BARRACKS).nonzero()
                
                #we use .any() for availability. 
                if unit_y.any():
                    target = [int(unit_x.mean()), int(unit_y.mean())]
                
                    self.barracks_selected = True
                
                    return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
            else:
                self.barracks_rallied = True
                
                if self.base_top_left:
                    return actions.FunctionCall(_RALLY_UNITS_MINIMAP, [_NOT_QUEUED, [29, 21]])
                
                return actions.FunctionCall(_RALLY_UNITS_MINIMAP, [_NOT_QUEUED, [29, 46]])
        elif obs.observation["player"][_SUPPLY_USED] < obs.observation["player"][_SUPPLY_MAX] and _TRAIN_MARINE in obs.observation["available_actions"]:
            return actions.FunctionCall(_TRAIN_MARINE, [_QUEUED])
        
        #For army
        elif not self.army_rallied:
            if not self.army_selected:
                if _SELECT_ARMY in obs.observation["available_actions"]:
                    self.army_selected = True
                    self.barracks_selected = False
                
                    return actions.FunctionCall(_SELECT_ARMY, [_NOT_QUEUED])
            elif _ATTACK_MINIMAP in obs.observation["available_actions"]:
                self.army_rallied = True
                self.army_selected = False
            
                if self.base_top_left:
                    return actions.FunctionCall(_ATTACK_MINIMAP, [_NOT_QUEUED, [39, 45]])
            
                return actions.FunctionCall(_ATTACK_MINIMAP, [_NOT_QUEUED, [21, 24]])
        #instruct the game to step ahead if none of the conditions are true. 
        return actions.FunctionCall(_NOOP, [])
