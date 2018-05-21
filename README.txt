game_info.pkl:

	This file is opened with pickle and it contains all game information
	in the form of nested dictionaries...
	To open use:

		with open('game_info.pkl', 'rb') as game_info:
			data = pickle.load(game_info)
	
	The data dictionary contains 3 keys: 'Zerg', 'Terran', and 'Protoss' 
	which each contains a set of games (use len(data[race]) to find how 
	many game data is included in that specific race set) where player 
	# 1 is of the race used as a key. 
	The contents of each game instance:
		
		- [0] player1: contains a dictionary with frames as keys, the
			values of each key is a numpy array of size specific
			for the race of player # 1 (based on mappings)

		- [1] player2: contains a dictionary with frames as keys, the
			values of each key is a numpy array of size specific
			for the race of player # 2 (based on mappings)

		- [2] map_name: the name identifier for the map used in the
			game replay instance. 

		- [3] result: the result (1/0) of the match, respective of 
			player # 1. If 1, player # 1 won, otherwise it lost.


dataset.pkl:

	This file is opened with pickle and it contains all game information
	in the form of dictionaries with numpy 2-D arrays...
	To open use:

		with open('dataset.pkl', 'rb') as dataset:
			data = pickle.load(dataset)
	
	The data contains again, 3 keys: 'Zerg', 'Terran', 'Protoss', which 
	each contain a set of games where player # 1 is of the race used as 
	a key.
	The contents of each game instance:
		- [0] player1: contains a numpy array of size MxN where M is 
			the number of frames in which an event occured during 
			the game. N is equal to the lengths of the stat specific 
			for the race selected. e.i Zerg's number of stats is 70, 
			an extra stat is included which is not present in 
			mappings, 'frame'. 'frame' is a common stat in all races, 
			and contains the frame stamps in which all other stats 			occured. Also the values are cumulative per state, meaning 			that we know the advancement of the game at every step. 

		- [1] player2: contains a numpy array of size MxN where M is 
			the number of frames in which an event occured during 
			the game. N is equal to the lengths of the stat specific 
			for the race selected. e.i Zerg's number of stats is 70, 
			an extra stat is included which is not present in 
			mappings, 'frame'. 'frame' is a common stat in all races, 
			and contains the frame stamps in which all other stats 			occured. Also the values are cumulative per state, meaning 				that we know the advancement of the game at every step.

		- [2] map_name: the name identifier for the map used in the
			game replay instance. 

		- [3] result: the result (1/0) of the match, respective of 
			player # 1. If 1, player # 1 won, otherwise it lost.
	

mappings.pkl:

	This file is a dictionary simply contains two dictionaries that map name of units or statistics to integer values. Accessable with the keys 'stats', and 'units', each maps units or stats to values. 
