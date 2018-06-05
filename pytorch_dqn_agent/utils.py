# from pysc2.lib import actions
# from pysc2.lib import features
#
# _NO_OP = actions.FUNCTIONS.no_op.id
# _SELECT_POINT = actions.FUNCTIONS.select_point.id
# _BUILD_SUPPLY_DEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
# _BUILD_BARRACKS = actions.FUNCTIONS.Build_Barracks_screen.id
# _TRAIN_MARINE = actions.FUNCTIONS.Train_Marine_quick.id
# _SELECT_ARMY = actions.FUNCTIONS.select_army.id
# _ATTACK_MINIMAP = actions.FUNCTIONS.Attack_minimap.id
# _HARVEST_GATHER = actions.FUNCTIONS.Harvest_Gather_screen.id
#
# _PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
# # _UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
# _PLAYER_ID = features.SCREEN_FEATURES.player_id.index
#
# _PLAYER_SELF = 1
# _PLAYER_HOSTILE = 4
# _ARMY_SUPPLY = 5
#
# _TERRAN_COMMANDCENTER = 18
# _TERRAN_SCV = 45
# _TERRAN_SUPPLY_DEPOT = 19
# _TERRAN_BARRACKS = 21
# _NEUTRAL_MINERAL_FIELD = 341
#
# _NOT_QUEUED = [0]
# _QUEUED = [1]
# _SELECT_ALL = [2]
#
# DATA_FILE = 'refined_agent_data'
#
# ACTION_DO_NOTHING = 'donothing'
# ACTION_BUILD_SUPPLY_DEPOT = 'buildsupplydepot'
# ACTION_BUILD_BARRACKS = 'buildbarracks'
# ACTION_BUILD_MARINE = 'buildmarine'
# ACTION_ATTACK = 'attack'
#
# smart_actions = [
#     ACTION_DO_NOTHING,
#     ACTION_BUILD_SUPPLY_DEPOT,
#     ACTION_BUILD_BARRACKS,
#     ACTION_BUILD_MARINE,
# ]
#
#
# def check_available(obs, action):
#     return action in obs.observation["available_actions"]
#
#
# def transformLocation(base_top_left,  x, x_distance, y, y_distance):
#     if not base_top_left:
#         return [x - x_distance, y - y_distance]
#
#     return [x + x_distance, y + y_distance]
#
#
# def splitAction(action_id):
#     smart_action = smart_actions[action_id]
#
#     x = 0
#     y = 0
#     if '_' in smart_action:
#         smart_action, x, y = smart_action.split('_')
