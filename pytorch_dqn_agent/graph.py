import numpy as np
import matplotlib as plt

res = np.load("reward.txt")

win_so_far = []
cur_win_count = 0

percetage_win_so_far = []
cur_prob_count = 0;

game_count = 0

for row in res:
	game_count = game_count + 1 # game counter
	if row == 1:
		cur_win_count = cur_win_count + row
		win.append(cur_win_count) 
		
		cur_prob_count = cur_win_count / game_count
		percetage_win_so_far.append(cur_prob_count)

plt(win_so_far, percetage_win_so_far)
