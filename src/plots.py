"""_summary_
Runs the public goods game for simulation number of times. Using the monte carlo method to derive
expected contributions at the player, groun, round, and simulation level.
"""

from src.monte_carlo_sim import *
import matplotlib.pyplot as plt

#==========================================================================================
# Function to make plots and other visuals from data generated in the MC simulation
#==========================================================================================

def avg_contribution_graph(all_round_avg_contribution_df: pd.DataFrame):
    """_summary_
    Creates a simple line graph of num rounds by avg round contribution 
    :param all_round_avg_contribution_df: avg contribution DF from monte_carlo_sim (output)
    """
    x = [i for i in range(NUM_ROUNDS)]
    y = all_round_avg_contribution_df.iloc[-1][:-1].tolist()
    plt.title(f"Endowment: {ENDOWMENT}, Shared: {SHARED}, In How many groups?: {NUM_MEMBERSHIP}, Group Size: {GROUP_SIZE}, Sims: {SIMS}")
    plt.xlabel("Round")
    plt.ylabel("Expected Round Contribution")
    plt.plot(x, y, color ="green")
    plt.show()