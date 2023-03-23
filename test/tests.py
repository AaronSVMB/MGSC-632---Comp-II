"""_summary_
Tests various functions from the public_goods_utils.py. 
"""
from src.monte_carlo_sim import *

#==========================================================================================
# Currently Working on: data visualization
# Goals: Make my visuals compatible with the way I now store my data from my simulation
# Ensure that I can make graphs with both the "metrics_of_interest.csv" and the returned
# "all_round_avg_contribution_df". 
#==========================================================================================

test_mc = monte_carlo_simulation(SIMS)
print(test_mc)

# BELOW

x = [i for i in range(NUM_ROUNDS)]
y = example_MC[1][:-1]
plt.title(f"Endowment: {ENDOWMENT}, Shared: {SHARED}, In How many groups?: {NUM_MEMBERSHIP}, Group Size: {GROUP_SIZE}, Sims: {SIMS}")
plt.xlabel("Round")
plt.ylabel("Expected Round Contribution")
plt.plot(x, y, color ="green")
plt.show()

