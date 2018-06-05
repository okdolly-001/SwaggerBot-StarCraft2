import numpy as np
import matplotlib.pyplot as plt
import csv

with open("reward.txt", 'rU') as f:
	res = csv.reader(f, delimiter = ",")
	win_so_far = []
	cur_win_count = 0

	percetage_win_so_far = []
	cur_prob_count = 0;

	game_count = 0

	for row in res:
		row = ''.join(row) # converts list to string
		game_count = game_count + 1 # game counter
		if row == "-1":
			cur_win_count = cur_win_count + 1
			win_so_far.append(cur_win_count) 
			
			cur_prob_count = cur_win_count / game_count
			percetage_win_so_far.append(cur_prob_count)

	plt.plot(win_so_far, percetage_win_so_far)
	plt.show()
