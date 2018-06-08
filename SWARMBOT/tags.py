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
_BUILD_REFINERY = actions.FUNCTIONS.Build_Refinery_screen.id
_BUILD_STARPORT = actions.FUNCTIONS.Build_Starport_screen.id
_BUILD_SUPPLY_DEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
## techlab is an add-on to barracks, factory, or starport
## used to create (marauders, ghosts), (Seige Tanks, Thors),
## (Ravens, banshees, and battlecruisers) respectively
## figuring out which to add on to is key... (not sure whether to use screen or quick)
_BUILD_TECHLAB = actions.FUNCTIONS.Build_TechLab_screen.id
_BUILD_TECHLAB_BARRACKS = actions.FUNCTIONS.Build_TechLab_Barracks_quick.id
_BUILD_TECHLAB_FACTORY = actions.FUNCTIONS.Build_TechLab_Factory_quick.id
_BUILD_TECHLAB_STARPORT = actions.FUNCTIONS.Build_TechLab_Starport_quick.id
## same idea as a techlab 
_BUILD_REACTOR = actions.FUNCTIONS.Build_Reactor_screen.id
_BUILD_REACTOR_BARRACKS = actions.FUNCTIONS.Build_Reactor_Barracks_quick.id
_BUILD_REACTOR_FACTORY = actions.FUNCTIONS.Build_Reactor_Factory_quick.id
_BUILD_REACTOR_STARPORT = actions.FUNCTIONS.Build_Reactor_Starport_quick.id

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
_RAVEN = 56
_REAPER = 49
_SIEGE_TANK = 33
_THOR = 52
## viking can transform to
## ASSAULT mode (34)
_VIKING = 35
_SCV = 45
_REACTOR = 6

## there seems to be a bug with pysc2
## where building reactors and techlabs
## to specific buildings is not available
## must check how to build these units in
## the desired building. Might fist implement
## something like selecting the building first
## then make the general build command for each
_REACTOR_BARRACKS = 38
_REACTOR_FACTORY = 40
_REACTOR_STARPORT = 42
_TECHLAB_BARRACKS = 37
_TECHLAB_FACTORY = 39
_TECHLAB_STARPORT = 41

DATA_FILE = 'refined_agent_data'

ACTION_DO_NOTHING = 'donothing'
ACTION_ATTACK = 'attack'
ACTION_RETREAT = 'retreat'

ACTION_T_BANSHEE = 't_banshee'
ACTION_T_BATTLECRUISER = 't_battlecruiser'
ACTION_T_CYCLONE = 't_cyclone'
ACTION_T_GHOST = 't_ghost'
ACTION_T_HELLION = 't_hellion'
ACTION_T_LIBERATOR = 't_liberator'
ACTION_T_MARAUDER = 't_marauder'
ACTION_T_MARINE = 't_marine'
ACTION_T_MEDIVAC = 't_medivac'
ACTION_T_RAVEN = 't_raven'
ACTION_T_REAPER = 't_reaper'
ACTION_T_SIEGETANK = 't_siegetank'
ACTION_T_SCV = 't_scv'
ACTION_T_VIKING = 't_viking'
ACTION_T_THOR = 't_thor'

ACTION_B_ARMORY = 'b_armory'
ACTION_B_BARRACKS = 'b_barracks'
ACTION_B_COMMANDCENTER = 'b_commandcenter'
ACTION_B_ENGINEERINGBAY = 'b_engineeringbay'
ACTION_B_FACTORY = 'b_factory'
ACTION_B_FUSIONCORE ='b_fusioncore'
ACTION_B_GHOSTACADEMY = 'b_ghostacademy'
ACTION_B_REFINERY = 'b_refinery'
ACTION_B_STARPORT = 'b_starport'
ACTION_B_SUPPLYDEPOT = 'b_supplydepot'
ACTION_B_TECHLAB_BARRACKS = 'b_techlab_barracks'
ACTION_B_TECHLAB_STARPORT = 'b_techlab_starport'
ACTION_B_TECHLAB_FACTORY = 'b_techlab_factory'
ACTION_B_REACTOR_BARRACKS = 'b_reactor_barracks'
ACTION_B_REACTOR_STARPORT = 'b_reactor_starport'
ACTION_B_REACTOR_FACTORY = 'b_reactor_factory'

units_capable_of_attacking = [
	'banshee',		'battlecruiser',
	'cyclone',		'ghost',
	'hellion',		'liberator',
	'marauder',		'marine',
	'medivac',		'raven',
	'reaper', 		'siegetank',
	'scv',	'viking',	'thor'
]


unit_dict = {
	'banshee': _BANSHEE,
	'battlecruiser': _BATTLE_CRUISER,
	'cyclone': _CYCLONE,
	'ghost': _GHOST,
	'hellion': _HELLION,
	'liberator': _LIBERATOR,
	'marauder': _MARAUDER,
	'marine': _MARINE,
	'medivac': _MEDIVAC,
	'raven': _RAVEN,
	'reaper': _REAPER,
	'siegetank': _SIEGE_TANK,
	'scv': _SCV,
	'viking': _VIKING,
	'thor': _THOR,
	'techlab': _TECHLAB,
	'supplydepot': _SUPPLY_DEPOT, 
	'starport': _STARPORT,
	'refinery': _REFINERY,
	'ghostacademy': _GHOST_ACADEMY,
	'fusioncore': _FUSION_CORE,
	'factory': _FACTORY,
	'engineeringbay': _ENGINEERING_BAY,
	'commandcenter': _COMMAND_CENTER,
	'barracks': _BARRACKS,
	'armory': _ARMORY,
	'reactor': _REACTOR
}

build_to_action = {'barracks':_BUILD_BARRACKS, 'supplydepot':_BUILD_SUPPLY_DEPOT, 'commandcenter':_BUILD_COMMAND_CENTER, 'refinery':_REFINERY,
				'ghostacademy':_BUILD_GHOST_ACADEMY, 'factory':_BUILD_FACTORY, 'armory':_BUILD_ARMORY, 'starport':_BUILD_STARPORT, 
				'fusioncore':_BUILD_FUSION_CORE}

unit_to_action = {'banshee':_TRAIN_BANSHEE,
'battlecruiser':_TRAIN_BATTLE_CRUISER,
'cyclone':_TRAIN_CYCLONE,
'ghost':_TRAIN_GHOST,
'hellion':_TRAIN_HELLION,
'liberator':_TRAIN_LIBERATOR,
'marauder':_TRAIN_MARAUDER,
'marine':_TRAIN_MARINE,
'medivac':_TRAIN_MEDIVAC,
'raven':_TRAIN_RAVEN,
'reaper':_TRAIN_REAPER,
'scv':_TRAIN_SCV,
'siegetank':_TRAIN_SIEGE_TANK,
'viking':_TRAIN_VIKING,
'thor':_TRAIN_THOR
}

build_with_SCV = ['barracks', 'supplydepot', 'commandcenter', 'refinery',
				'ghostacademy', 'factory', 'armory', 'starport', 'fusioncore']

starport_units = ['banshee', 'battlecruiser', 'liberator', 'medivac', 'raven', 'viking']

barracks_units = ['ghost', 'marauder', 'marine', 'reaper']

factory_units = ['cyclone', 'hellion', 'siegetank', 'thor']

Buildings = [_BARRACKS, _ARMORY, _REACTOR, _COMMAND_CENTER, _ENGINEERING_BAY, _FACTORY,
			_FUSION_CORE, _GHOST_ACADEMY, _REFINERY, _STARPORT, _SUPPLY_DEPOT, _TECHLAB, 
			_NEUTRAL_MINERAL_FIELD, _NEUTRAL_VESPENE_GEYSER]

smart_actions = [	
	ACTION_DO_NOTHING, 			ACTION_T_BANSHEE,			ACTION_RETREAT,
	ACTION_T_BATTLECRUISER, 	ACTION_T_CYCLONE, 			ACTION_T_GHOST,
	ACTION_T_HELLION, 			ACTION_T_LIBERATOR, 		ACTION_T_MARAUDER,
	ACTION_T_MARINE, 			ACTION_T_MEDIVAC,			ACTION_T_RAVEN,
	ACTION_T_REAPER,			ACTION_T_SIEGETANK, 		ACTION_T_SCV,
	ACTION_T_VIKING,			ACTION_T_THOR,				ACTION_B_ARMORY,
	ACTION_B_BARRACKS,			ACTION_B_COMMANDCENTER,		ACTION_B_ENGINEERINGBAY,
	ACTION_B_FACTORY,			ACTION_B_GHOSTACADEMY,		
	ACTION_B_REFINERY,			ACTION_B_STARPORT,			ACTION_B_SUPPLYDEPOT,
	ACTION_B_TECHLAB_FACTORY, 	ACTION_B_TECHLAB_STARPORT, 	ACTION_B_TECHLAB_BARRACKS,
	ACTION_B_REACTOR_FACTORY, 	ACTION_B_REACTOR_STARPORT, 	ACTION_B_REACTOR_BARRACKS
]