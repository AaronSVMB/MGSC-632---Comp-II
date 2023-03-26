"""_summary_
Tests various functions from the public_goods_utils.py. 
"""
from src.plots import *

#==========================================================================================
# Currently Working on: Data Visualization Part 2

# Goal: access the data stored in metrics_of_interest.csv, use this to create meaningful visuals
#==========================================================================================

metrics_of_interest = pd.read_csv('metrics_of_interest.csv', index_col = 0)

example_round_avg = player_round_average_contributions(metrics_of_interest, SIMS, NUM_PLAYERS, NUM_ROUNDS)

player_round_avg_contribution_graph(example_round_avg)


player_avg_bar_chart(example_round_avg)

x = group_round_average_contribution(metrics_of_interest, NUM_GROUPS, NUM_ROUNDS, SIMS)
print(x)