import random
import math
import os

import numpy as np
import pandas as pd

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
_BUILD_ENGINEERING_BAY = actions.FUNCTIONS.Build_EngineeringBay_screen.id
_BUILD_FACTORY = actions.FUNCTIONS.Build_Factory_screen.id
_BUILD_FUSION_CORE = actions.FUNCTIONS.Build_FusionCore_screen.id
_BUILD_GHOST_ACADEMY = actions.FUNCTIONS.Build_GhostAcademy_screen.id
_BUILD_NUKE = actions.FUNCTIONS.Build_Nuke_quick.id
_BUILD_REFINERY = actions.FUNCTIONS.Build_Refinery_screen.id
_BUILD_STARPORT = actions.FUNCTIONS.Build_Starport_screen.id
_BUILD_SUPPLY_DEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
## techlab is an add-on to barracks, factory, or starport
## used to create (marauders, ghosts), (Seige Tanks, Thors),
## (Ravens, banshees, and battlecruisers) respectively
## figuring out which to add on to is key... 
_BUILD_TECHLAB = actions.FUNCTIONS.Build_TechLab_screen.id
_BUILD_TECHLAB_BARRACKS = actions.FUNCTIONS.Build_TechLab_Barracks_quick.id
_BUILD_TECHLAB_FACTORY = actions.FUNCTIONS.Build_TechLab_Factory_quick.id
_BUILD_TECHLAB_STARPORT = actions.FUNCTIONS.Build_TechLab_Starport_quick.id

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
_TRAIN_SEIGE_TANK = actions.FUNCTIONS.Train_SeigeTank_quick.id
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
_ENGINEERING_BAY = 22
_REFINERY = 20
_SUPPLY_DEPOT = 19
_TECHLAB = 5
_BANSHEE = 55
_BATTLE_CRUISER = 57
_CYCLONE = 692
_GHOST = 50
_HELLION = 53
_LIBERATOR = 689
_MARAUDER = 51
_MARINE = 48
_MEDIVAC = 54
_NUKE = 58
_RAVEN = 56
_REAPER = 49
_SEIGETANK = 33
_THOR = 52
## viking can transform to
## ASSAULT mode (34)
_VIKING = 35
_SCV = 45

DATA_FILE = 'refined_agent_data'
ACTION_DO_NOTHING = 'donothing'
ACTION_ATTACK = 'attack'
ACTION_T_BANSHEE =
ACTION_T_BATTLECRUISER =
ACTION_T_CYCLONE =
ACTION_T_GHOST =
ACTION_
ACTION_
ACTION_
ACTION_
ACTION_
ACTION_
ACTION_
ACTION_
ACTION_
ACTION_

smart_actions = [ACTION_DO_NOTHING]

## adds attack <which> quadrant actions
for mm_x in range(0, 64):
    for mm_y in range(0, 64):
        if (mm_x + 1) % 32 == 0 and (mm_y + 1) % 32 == 0:
            smart_actions.append(ACTION_ATTACK + '_' + str(mm_x - 16) + '_' + str(mm_y - 16))

