import matplotlib.pyplot as plt
import csv

with open("rewards.csv", 'rU') as f:
    res = csv.reader(f, delimiter=",")

    win_so_far, loss_so_far, tie_so_far = [], [], []
    cur_win_count, cur_loss_count, cur_tie_count = 0, 0, 0

    percetage_win_so_far, percetage_loss_so_far, percetage_tie_so_far = [], [], []
    cur_win_prob_count, cur_loss_prob_count, cur_tie_prob_count = 0, 0, 0

    game_count = 0

    count = list(range(75))

    for row in res:
        score = row[1]
        print(score)    
        game_count = game_count + 1  # game counter
        if score == "1":
            cur_win_count = cur_win_count + 1
            win_so_far.append(cur_win_count)

            cur_win_prob_count = cur_win_count / game_count * 100
            percetage_win_so_far.append(cur_win_prob_count)

            percetage_loss_so_far.append(cur_loss_prob_count)
            percetage_tie_so_far.append(cur_tie_prob_count) 
        elif score == "-1":
            cur_loss_count = cur_loss_count + 1
            loss_so_far.append(cur_loss_count)
 
            cur_loss_prob_count = cur_loss_count / game_count * 100
            percetage_loss_so_far.append(cur_loss_prob_count)

            percetage_win_so_far.append(cur_win_prob_count)
            percetage_tie_so_far.append(cur_tie_prob_count) 
        else:  # score == "0"
            cur_tie_count = cur_tie_count + 1
            tie_so_far.append(cur_tie_count)

            cur_tie_prob_count = cur_tie_count / game_count * 100
            percetage_tie_so_far.append(cur_tie_prob_count)

            percetage_win_so_far.append(cur_win_prob_count)
            percetage_loss_so_far.append(cur_loss_prob_count)

    # plots all 3 functions on same graph
    plt.title('SumpremeBot Learning Trend')
    plt.plot(count, percetage_win_so_far, "b", count,
             percetage_loss_so_far, "r", count, percetage_tie_so_far, "g")
    plt.legend(('Win', 'Loss', 'Tie'),
               loc='upper right')
    plt.ylabel('Win%,Loss%,Tie%')
    plt.xlabel('Episode')
    plt.show()
