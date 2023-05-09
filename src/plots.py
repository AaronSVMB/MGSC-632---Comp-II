"""
Runs the public goods game for simulation number of times. Using the monte carlo method to derive
expected contributions at the player, groun, round, and simulation level.
"""

from src.monte_carlo_sim import *

import matplotlib.pyplot as plt

#==========================================================================================
# Function to make plots and other visuals from data generated in the MC simulation
#==========================================================================================

def avg_contribution_graph(all_round_avg_contribution_df: pd.DataFrame):
    """
    Creates a simple line graph of num rounds by avg round contribution.

    :param all_round_avg_contribution_df: avg contribution DF from monte_carlo_sim (output)
    """
    x = [i for i in range(NUM_ROUNDS)]
    y = all_round_avg_contribution_df.iloc[-1][:-1].tolist()
    plt.title(f"Endowment: {ENDOWMENT}, Shared: {SHARED}, In How many groups?: {NUM_MEMBERSHIP}, Group Size: {GROUP_SIZE}, Sims: {SIMS}")
    plt.xlabel("Round")
    plt.ylabel("Expected Round Contribution")
    plt.plot(x, y, color ="green")
    plt.show()

#==========================================================================================
# Function to make plots and other visuals from data generated in the MC simulation
#==========================================================================================

def player_round_average_contributions(metrics_of_interest: pd.DataFrame, SIMS: int, NUM_PLAYERS: int, NUM_ROUNDS: int):
    """
    Creates an np.ndarray that has access to the player average contribution for each round across all simulations
    :param metrics_of_interest: pandas dataframe containing information from MC sim.

    :param SIMS: the number of simulations
    :param NUM_PLAYERS: the total number of players
    :param NUM_ROUNDS: the number of rounds played
    :return: array NUM_PLAYERS x NUM_ROUNDS + 1 ; stores avg round contribution for each player & avg contribution in last column
    """
    player_round_average_contribution_array = np.zeros([NUM_PLAYERS, NUM_ROUNDS + 1])
    for player in range(NUM_PLAYERS):
        for rnd in range(NUM_ROUNDS):
            player_one_round_contribution_loc = metrics_of_interest.loc[(metrics_of_interest.index == f'player{player}') & (metrics_of_interest['RoundID'] == float(rnd)),
             'playeravg']
            player_one_round_contributions_values = player_one_round_contribution_loc.values
            avg_player_round_contribution = player_one_round_contributions_values.mean()
            player_round_average_contribution_array[player][rnd] = avg_player_round_contribution
        player_round_average_contribution_array[player][NUM_ROUNDS] = player_round_average_contribution_array[player][:-2].mean()
    return player_round_average_contribution_array

#TODO Make this look nicer. Also isn't that informative right now
def player_round_avg_contribution_graph(player_round_average_contribution_array: np.ndarray, NUM_ROUNDS: int, NUM_PLAYERS: int):
    """
    Line graph with NUM_PLAYER number of lines displaying player level contribution across rounds.

    :param player_round_average_contribution_array: array built to have the data necessary for this plot
    :param NUM_ROUNDS: the number of rounds
    :param NUM_PLAYERS: the number of players
    """
    x = [i for i in range(NUM_ROUNDS)]
    for player in range(NUM_PLAYERS):
        y = player_round_average_contribution_array[player][:-1]
        plt.plot(x, y)

    plt.title(f"Each Players average contribution in rounds across simulations")
    plt.xlabel("Round")
    plt.ylabel("Expected Round Contribution")
    plt.show()

def player_avg_bar_chart(player_round_average_contribution_array: np.ndarray, NUM_PLAYERS: int):
    """
    Bar chart displaying player average contributions across all rounds.

    :param player_round_average_contribution_array: array built to have the data necessary for this plot
    :param NUM_PLAYERS: the number of players
    """
    players = [player for player in range(NUM_PLAYERS)]
    values = [player_round_average_contribution_array[player][-1] for player in range(NUM_PLAYERS)]
    fig = plt.figure(figsize = (10,5))
    plt.bar(players, values, color = 'navy', width = 0.4 )

    plt.xlabel("PlayerID")
    plt.ylabel("Expected Contribution")
    plt.title("Expected Contribution across Rounds & Simulations for all Players")
    plt.show()

def group_round_average_contribution(metrics_of_interest: pd.DataFrame, NUM_GROUPS: int, NUM_ROUNDS: int, SIMS: int):
    """
    Creates an np.ndarray from the moi dataframe that stores group level information: contribution across rounds, and overall avg contribution.

    :param metrics_of_interest: principle output of the MC sim -> read in from csv
    :param NUM_GROUPS: the total number of groups
    :param NUM_ROUNDS: the number of rounds
    :param SIMS: the number of simulations
    :return: np.ndarray that stores group level avg contribution information (round-and game-wise)
    """
    subset = metrics_of_interest.loc[metrics_of_interest.index == 'groupavg']
    cell_values = subset.values

    group_round_average_contribution_array = np.zeros([NUM_GROUPS, NUM_ROUNDS + 1])

    for group in range(NUM_GROUPS):
        for rnd in range(NUM_ROUNDS):
            group_rnd_sum = 0
            for sim in range(SIMS):
                group_rnd_sum += cell_values[rnd + (NUM_ROUNDS * sim)][group + 2]
            group_round_average_contribution_array[group][rnd] = group_rnd_sum / SIMS
        group_round_average_contribution_array[group][-1] = group_round_average_contribution_array[group][:-1].mean()

    return group_round_average_contribution_array

#TODO make it look nicer. Currently not very informative
def group_round_avg_contribution_graph(group_round_average_contribution_array: np.ndarray, NUM_ROUNDS: int, NUM_GROUPS: int):
    """
    Generates a line graph with NUM_GROUPS number of lines. x-axis number of rounds, y-axis avg contribution.

    :param group_round_average_contribution_array: np.ndarray that stores group level avg contribution information (round-and game-wise)
    :param NUM_ROUNDS: the number of rounds
    :param NUM_GROUPS: the number of groups
    """
    x = [i for i in range(NUM_ROUNDS)]
    for group in range(NUM_GROUPS):
        y = group_round_average_contribution_array[group][:-1]
        plt.plot(x, y)

    plt.title(f"Each Groups average contribution in rounds across simulations")
    plt.xlabel("Round")
    plt.ylabel("Expected Round Contribution")
    plt.show()

def group_avg_bar_chart(group_round_average_contribution_array: np.ndarray, NUM_GROUPS: int):
    """
    Creates a bar chart for group-level average contribution across all rounds.

    :param group_round_average_contribution_array: np.ndarray that stores group level avg contribution information (round-and game-wise)
    :param NUM_GROUPS: the number of groups 
    """
    groups = [group for group in range(NUM_GROUPS)]
    values = [group_round_average_contribution_array[group][-1] for group in range(NUM_GROUPS)]
    fig = plt.figure(figsize = (10, 5))
    plt.bar(groups, values, color = 'navy', width = 0.4 )

    plt.xlabel("GroupID")
    plt.ylabel("Expected Contribution")
    plt.title("Expected Contribution across Rounds & Simulations for all Groups")
    plt.show()