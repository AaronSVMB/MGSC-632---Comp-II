"""
all funcitons necessary for playing the multi-group public goods game
"""
import numpy as np
import pandas as pd
import random
import math
from src.update_contribution import update_contributions_split_stochastic_dict, update_contributions_stochastic_shared_dict

#==========================================================================================
# Set up Parameters
#==========================================================================================

NUM_MEMBERSHIP = 2 # Number of groups each player interacts with
ENDOWMENT = 160 # The Endowment each player receives 
SHARED = 1 # 1 if the endowment is shared across groups | 0 if it is split
GROUP_SIZE = 4 # size of each group
R = 1.6 # Scale factor
NUM_ROUNDS = 10 # Number of rounds that players will participate in the public good game

## When NUM_MEMBERSHIP == 2
NUM_GROUPS = GROUP_SIZE * 2 # number of groups
NUM_PLAYERS = GROUP_SIZE ** 2 # Number of players in the system

# Player type initialize 
METHOD = "conditional" # can take on values 'random', 'conditional', 'altruists', and 'mixed'

# For Monte Carlo Simulation
SIMS = 10000

# For gradient descent
# DELTA is now a function 

TREMBLE = [0.1, 0.1, 0.1] # 0 is F-R, 1 CC, 2 Alt
# How likely they are to deviate from their strategy (of their player type)


#==========================================================================================
# Functions used regardless of ENDOWMENT scheme
#==========================================================================================

def init_delta(player_type_matrix: np.ndarray, NUM_PLAYERS: int):
    """_summary_
    Endogenizing the learning rates (for gradient descent) of each player. This initializes player
    learning rates for each iteration of a simulation
    :param player_type_matrix: the types of each player: 0 F-r, 1 CC, 2, Alt
    :param NUM_PLAYERS: the number of players
    :return: returns a column vector of each player DELTA; increases stochasticity
    """
    DELTA = np.zeros([NUM_PLAYERS,1])
    for player in range(NUM_PLAYERS):
        player_type = player_type_matrix[player]
        if player_type == 1: # conditional cooperator
            DELTA[player] = np.random.normal(0.75, 0.25)
        else: # arguing that free-riders and altruists are less responsive (less likely to learn)
            DELTA[player] = abs(np.random.standard_normal()) * 0.7
        DELTA[player] = max(0.65,DELTA[player])
        DELTA[player] = min(1, DELTA[player])
    return DELTA

def update_delta(DELTA: np.ndarray, NUM_PLAYERS: int):
    """_summary_
    After each round, update the learning rate of the players. I have it assumed now that
    each player, regardless of player type and realized contribution, decreases their
    learning rates as the number of rounds increases
    :param DELTA: the learning rate of each player stored in np.ndarray NUM_PLAYERS x 1
    :param NUM_PLAYERS: the number of players
    :return: the updated DELTA values for each player as an np.ndarray
    """
    prob = 0.4
    for player in range(NUM_PLAYERS):
        if DELTA[player] > 0:
            if np.random.rand() < prob:
                DELTA[player] -= (DELTA[player]**2) *np.random.rand() # This might be too oppressive but we shall we
            else:
               if np.random.rand() < prob:
                  DELTA[player] += (DELTA[player]**2) *np.random.rand()
        DELTA[player] = max(0, DELTA[player])
        DELTA[player] = min(1, DELTA[player])
    return DELTA

def initialize_contributions_with_distribution(NUM_PLAYERS: int, NUM_MEMBERSHIP: int, 
                                               ENDOWMENT: int, SHARED: bool, player_type_matrix: np.ndarray, DELTA: np.ndarray):
    initial_contributions = np.zeros([NUM_PLAYERS, NUM_MEMBERSHIP])
    if SHARED == 1:
        for player in range(NUM_PLAYERS):
            player_type = player_type_matrix[player]
            if player_type == 0:
                if np.random.rand() < TREMBLE[0]: # chance for free-rider to deviate in initial round
                    initial_contributions[player][0] = np.random.randint(0, ENDOWMENT * 0.15)
                for member in range(1, NUM_MEMBERSHIP):
                    initial_contributions[player][member] = np.random.randint(0, ENDOWMENT * 0.15)
            if player_type == 1:
                initial_contribution_first_group = max(0, np.random.normal(ENDOWMENT * 0.5, ENDOWMENT * 0.25))
                initial_contribution_first_group = min(ENDOWMENT, initial_contribution_first_group)
                initial_contributions[player][0] = int(initial_contribution_first_group)
                for member in range(1, NUM_MEMBERSHIP):
                    successive_contribution = max(0, np.random.normal(ENDOWMENT * 0.5, ENDOWMENT * 0.25))
                    successive_contribution = min(successive_contribution, ENDOWMENT - initial_contribution_first_group)
                    initial_contributions[player][member] = int(successive_contribution)
                    initial_contribution_first_group += successive_contribution
            if player_type == 2: # chance for altruist to deviate from player type in initial contribution
                if np.random.rand() > TREMBLE[2]:
                    initial_contributions[player][:] = np.random.randint((ENDOWMENT / NUM_MEMBERSHIP) * 0.85,
                                                                         ENDOWMENT / NUM_MEMBERSHIP)
                else:
                    initial_contributions[player][:] = np.random.randint((ENDOWMENT / NUM_MEMBERSHIP) * 0.5,
                                                                         ENDOWMENT / NUM_MEMBERSHIP)
    else:
        for player in range(NUM_PLAYERS):
            player_type = player_type_matrix[player]
            for group_member in range(NUM_MEMBERSHIP):
                contribution_amount = np.random.randint(0, ENDOWMENT / NUM_MEMBERSHIP)
                if player_type == 0:
                    initial_contributions[player][group_member] = np.random.randint(0, contribution_amount* 0.15)
                if player_type == 1:
                     initial_contributions[player][group_member] = contribution_amount 
                if player_type == 2:
                    initial_contributions[player][group_member] =  np.random.randint((ENDOWMENT / NUM_MEMBERSHIP) * 0.75, ENDOWMENT / NUM_MEMBERSHIP)
    for player in range(NUM_PLAYERS):
        initial_contributions[player][:] *= DELTA[player]
    initial_contributions = np.round(initial_contributions)
    initial_contributions = initial_contributions.astype(int)
    return initial_contributions # avg contribution is a little high, but workable (can make better later, but at least I have stochasticity here now)


def formed_groups_matrix(GROUP_SIZE: int, NUM_GROUPS: int):
  """_summary_
  Function to form groups in the form of a matrix in a NUM_PLAYERS x NUM_GROUPS sized matrix. 
  :param GROUP_SIZE: the size of each group
  :param NUM_GROUPS: the total number of each group
  :return: matrix NUM_PLAYERS x NUM_GROUPS : displays 1 or 0 in cells whether or not a player is in that group
  """
  groups_matrix = np.zeros([NUM_PLAYERS, NUM_GROUPS])
  if NUM_MEMBERSHIP == 2 and GROUP_SIZE == 4:
    for i in range(4):
      groups_matrix[i][0] = 1
      groups_matrix[i][i+1] = 1
    for i in range(4,7):
      groups_matrix[i][1] = 1
      groups_matrix[i][i+1] = 1
    for i in range(7,10):
      groups_matrix[i][2] = 1
      groups_matrix[i][i-2] = 1
    for i in range(10,13):
      groups_matrix[i][3] = 1
      groups_matrix[i][i-5] = 1
    for i in range(13,16):
      groups_matrix[i][4] = 1
      groups_matrix[i][i-8] = 1
  return groups_matrix

def calculuate_scaled_public_good(contributions: np.ndarray, groups_matrix: np.ndarray, NUM_PLAYERS: int, R: float):
  """_summary_
  Function to sum up the contributions in a given group and then multiply it by the scale factor. Since it matters which 
  contribution goes to which group I keep track of a contribution_index variable.
  :param contributions: matrix that displays a palyers contributions to their group: NUM_PLAYERS x NUM_MEMBERSHIP
  :param groups_matrix: matrix that displays what groups a player is in: NUM_PLAYERS x NUM_GROUPS
  :param NUM_PLAYERS: the total number of players 
  :param R: the scale factor
  :return: the total public good that each group has at the end of a round
  """
  public_good_matrix = np.zeros(NUM_GROUPS)
  for player in range(NUM_PLAYERS): # NUM_PLAYER x NUM_GROUPS
    contribution_index = 0 
    for group in range(NUM_GROUPS):
      if contribution_index > (NUM_MEMBERSHIP - 1):
        break
      if groups_matrix[player][group] == 1 and contribution_index < NUM_MEMBERSHIP:
        public_good_matrix[group] += contributions[player][contribution_index]
        contribution_index +=1
  scaled_public_good = R * public_good_matrix
  return scaled_public_good

"""def calculuate_scaled_public_good_new(contributions: np.ndarray, groups_matrix: np.ndarray, NUM_PLAYERS: int, R: float):
  new_public_goods_matrix = np.zeros(NUM_GROUPS)
  player_contributions_1_groups = player_group_lookup[0,:] # player_group_lookup 2 x NUM_PLAYERS 
  new_public_goods_matrix[player_contributions_1_groups]  += contributions[:,0].T

  player_contributions_2_groups = player_group_lookup[1,:] # player_group_lookup 2 x NUM_PLAYERS 
  new_public_goods_matrix[player_contributions_2_groups]  += contributions[:,1].T
  scaled_public_good = R * new_public_goods_matrix
  return scaled_public_good"""

#==========================================================================================
# Functions for Split Endowment
#==========================================================================================

def calculate_payoff_split(contributions: np.ndarray, group_matrix: np.ndarray, ENDOWMENT: int, scaled_public_good: np.ndarray):
  """_summary_ 
  Calculates the payoff when the groups are economically independent (split endowment).
  :param contributions: matrix that displays a palyers contributions to their group: NUM_PLAYERS x NUM_MEMBERSHIP
  :param group_matrix: matrix that displays what groups a player is in: NUM_PLAYERS x NUM_GROUPS
  :param ENDOWMENT: the amount of resources given at the start of each round to players
  :param scaled_public_good: the total public good that each group has at the end of a round: NUM_GROUPS x 1
  :return: the payoff that each individual gets from participating in their group
  """
  payoffs_matrix = np.zeros([NUM_PLAYERS,NUM_GROUPS])
  for player in range(NUM_PLAYERS):
    contribution_index = 0 
    for group in range(NUM_GROUPS):
      if contribution_index > (NUM_MEMBERSHIP - 1):
        break
      if group_matrix[player][group] == 1:
        payoffs_matrix[player][group] = (ENDOWMENT / NUM_MEMBERSHIP) - contributions[player][contribution_index] + (scaled_public_good[group] / GROUP_SIZE)
        contribution_index += 1
  return payoffs_matrix


def initialize_player_types(NUM_PLAYERS: int, update_contributions_split_dict: dict, METHOD: str):
  """_summary_
  initializes player types based off of prespecified scenerios 
  :param NUM_PLAYERS: the total number of players
  :param update_contributions_split_dict: dictionary containing the relevant playertypes
  :param METHOD: specifies desired population 'mix'
  :return: matrix of size NUM_PLAYERS x 1 that displays each players type
  """
  player_type_matrix = np.zeros([NUM_PLAYERS,1])
  if METHOD == "random":
    player_type_matrix = np.random.randint(len(update_contributions_split_dict), size=(NUM_PLAYERS,1))
  elif METHOD == "conditional":
    player_type_matrix = np.ones([NUM_PLAYERS,1])
  elif METHOD == "altruists":
    player_type_matrix.fill(2) 
  elif METHOD == "mixed": # 2ccs per group, 1 fr, 1 al
    player_type_matrix[0], player_type_matrix[3], player_type_matrix[6], player_type_matrix[8:12], player_type_matrix[13] = 1, 1, 1, 1, 1
    player_type_matrix[1], player_type_matrix[4], player_type_matrix[12],player_type_matrix[14] = 2, 2, 2, 2
  return player_type_matrix

def update_contributions_stochastic_split(player_type_matrix: np.ndarray, contributions: np.ndarray, payoff_matrix: np.ndarray,
                                group_matrix: np.ndarray, ENDOWMENT: int,
                                  NUM_MEMBERSHIP: int, DELTA: np.ndarray, TREMBLE: list):
    for player in range(NUM_PLAYERS):
        player_type = int(player_type_matrix[player])
        update_contributions_split_use = update_contributions_split_stochastic_dict[player_type]
        contributions = update_contributions_split_use(player, contributions, payoff_matrix, group_matrix, ENDOWMENT, NUM_MEMBERSHIP, NUM_GROUPS, DELTA, TREMBLE)
    return contributions

#==========================================================================================
# Functions for Shared Endowment
#==========================================================================================

def calculate_payoff_shared(contributions: np.ndarray, group_matrix: np.ndarray, ENDOWMENT: int, scaled_public_good: np.ndarray):
  """_summary_
  How to calculate the payoff for an indiivdal contributing to their groups. The endowment is removed since it would be double counted
  :param contributions: matrix that displays a palyers contributions to their group: NUM_PLAYERS x NUM_MEMBERSHIP
  :param group_matrix: matrix that displays what groups a player is in: NUM_PLAYERS x NUM_GROUPS
  :param ENDOWMENT: the amount of resources given at the start of each round to players
  :param scaled_public_good: he total public good that each group has at the end of a round
  :return: the payoffs individuals get for being in their groups
  """
  payoffs_matrix = np.zeros([NUM_PLAYERS,NUM_GROUPS])
  for player in range(NUM_PLAYERS):
    contribution_index = 0 
    for group in range(NUM_GROUPS):
      if contribution_index > (NUM_MEMBERSHIP - 1):
        break
      if group_matrix[player][group] == 1:
        payoffs_matrix[player][group] = - contributions[player][contribution_index] + (scaled_public_good[group] / GROUP_SIZE) 
        contribution_index += 1
  return payoffs_matrix
  # removed endowment for now since it is a little confusing with the endowment in both groups since it would double count

def update_contributions_stochastic_shared(player_type_matrix: np.ndarray, contributions: np.ndarray, payoff_matrix: np.ndarray,
                                 group_matrix: np.ndarray, ENDOWMENT: int, NUM_MEMBERSHIP: int, DELTA: np.ndarray, TREMBLE: list):
  """_summary_
  updates contribution for all players in the shared endowment regime. Uses the 'update_contributions_shared_dict' 
  to access their player-type specific update function
  :param player_type_matrix: matrix of size NUM_PLAYERS x 1 that displays each players type
  :param contributions: matrix that displays a palyers contributions to their group: NUM_PLAYERS x NUM_MEMBERSHIP
  :param payoff_matrix: the payoffs individuals get for being in their groups
  :param group_matrix: matrix that displays what groups a player is in: NUM_PLAYERS x NUM_GROUPS
  :param ENDOWMENT: the amount of resources given at the start of each round to players
  :param NUM_MEMBERSHIP: the number of groups each player is in 
  :param DELTA: gradient descent learning rate
  :return: the updated contributions for players to give in the current round based on their previous rounds experience
  """
  for player in range(NUM_PLAYERS):
    player_type = int(player_type_matrix[player])
    update_contributions_shared_use = update_contributions_stochastic_shared_dict[player_type]
    contributions = update_contributions_shared_use(player, contributions, payoff_matrix, group_matrix, ENDOWMENT, NUM_MEMBERSHIP, NUM_GROUPS, DELTA, TREMBLE)
  return contributions 

#==========================================================================================
# Functions to store relevant data from rounds of the public goods game
#==========================================================================================

def metrics_of_interest_array_builder(NUM_GROUPS: int, GROUP_SIZE: int, NUM_PLAYERS: int, 
current_round: int, current_sim: int):
  """_summary_
  Builds an array to store information from each round of the public goods game
  :param NUM_GROUPS: the total number of groups
  :param GROUP_SIZE: the size of each group
  :return: a blank matrix of size GROUP_SZIE x (NUM_GROUPS + 2) to store relevant information
  the first column stores the player IDs and the second column stores the round ID
  """
  metrics_of_interest_array = formed_groups_matrix(GROUP_SIZE, NUM_GROUPS)
  metrics_of_interest_array[metrics_of_interest_array==0] = 'nan'
  sim_id = np.array([f'{current_sim}' for i in range(NUM_PLAYERS)])
  round_id = np.array([f'{current_round}' for i in range(NUM_PLAYERS)])
  metrics_of_interest_array = np.insert(metrics_of_interest_array, 0, round_id, axis = 1)
  metrics_of_interest_array = np.insert(metrics_of_interest_array, 0, sim_id, axis = 1)

  return metrics_of_interest_array

def update_metrics_of_interest(metrics_of_interest_array: np.ndarray, contributions_matrix: np.ndarray,
 groups_matrix: np.ndarray):
  """_summary_
  Stores contribution information for a round. Stores players contribution to their groups, their average 
  contribution across their groups, stores group average contribution, and round average contribution
  :param metrics_of_interest_array: Space to add data / rows / columns to store round information
  :param contributions_matrix: relevant round information to insert into our round information matrix
  :return: relevant round information described in _summary_
  """
  for player in range(NUM_PLAYERS):
      contribution_index = 0
      for group in range(NUM_GROUPS):
        if contribution_index == NUM_MEMBERSHIP:
          break
        if groups_matrix[player][group] == 1:
          metrics_of_interest_array[player][group + 2] = contributions_matrix[player][contribution_index]
          contribution_index += 1
  group_means = np.nanmean(metrics_of_interest_array, axis = 0, keepdims = True) # sum of columns
  group_means[0][0], group_means[0][1] = np.nan, np.nan
  metrics_of_interest_array = np.append(metrics_of_interest_array, group_means, axis = 0)
    
  player_means = np.nanmean(metrics_of_interest_array[:,2:], axis = 1, keepdims= True) # sum of rows
  metrics_of_interest_array = np.append(metrics_of_interest_array, player_means, axis = 1)

  metrics_of_interest_df = pd.DataFrame(metrics_of_interest_array)
  column_dict, row_dict = {0: "SimulationID", 1: "RoundID"}, {}
  for group in range(2, NUM_GROUPS + 2):
    column_dict[group] = f"group{group - 2}"
  for player in range(NUM_PLAYERS):
    row_dict[player] = f"player{player}"
  column_dict[NUM_GROUPS + 2] = 'playeravg'
  row_dict[NUM_PLAYERS] = 'groupavg'
  metrics_of_interest_df.rename(columns = column_dict, index = row_dict, inplace=True) 
  return metrics_of_interest_df

#==========================================================================================
# Simulate public goods game for one simulation, round number of times
#==========================================================================================
#TODO Update simulate game to correspond and work with the new update decion functions, and initialization functions
# for both DELTA and for contributions, player types, etc. 
def simulate_game(NUM_MEMBERSHIP: int, ENDOWMENT: int, SHARED: bool, 
                      GROUP_SIZE: int, R: float, NUM_GROUPS: int, NUM_PLAYERS: int,
                        NUM_ROUNDS: int, METHOD: str, current_sim: int):
  """_summary_
  Simulate multiple rounds of the multi-group public goods game. The different cases are for which endowment regime is in place, SHARED or SPLIT
  for which there exists two distinct function families
  :param NUM_MEMBERSHIP: the number of groups each player is in
  :param ENDOWMENT: the resources each agent has at the start of each round
  :param SHARED: shared or split endowment regime
  :param GROUP_SIZE: the size of each group
  :param R: the scale factor for the public good of each group
  :param NUM_GROUPS: the total number of groups
  :param NUM_PLAYERS: the total number of participating players
  :param NUM_ROUNDS: the number of rounds
  :param METHOD: method used to construct the player types 
  :param current_sim: the number of the current simulation that the program is executing
  :return: Tuple - [0] easy access to round average contribution [1] MOI_df that stores [0] & more information
  """
  player_types_matrix = initialize_player_types(NUM_PLAYERS, update_contributions_split_dict, METHOD)
  contributions_matrix = initailize_contribtions_with_player_types(NUM_PLAYERS, NUM_MEMBERSHIP, ENDOWMENT, SHARED, player_types_matrix)
  groups_matrix = formed_groups_matrix(GROUP_SIZE, NUM_GROUPS)

  metrics_of_interest_array_all_rounds = metrics_of_interest_array_builder(NUM_GROUPS, GROUP_SIZE, NUM_PLAYERS, 0, current_sim)
  metrics_of_interest_array_all_rounds = update_metrics_of_interest(metrics_of_interest_array_all_rounds, contributions_matrix, groups_matrix)
    
  round_avg_contribution = np.zeros(NUM_ROUNDS) # keeping for now. Stores the round level average contribution across all groups & players
  round_avg_contribution[0] = np.sum(contributions_matrix) / (NUM_MEMBERSHIP*NUM_PLAYERS) # the bottom right most cell of m_o_i_a stores this also

  if SHARED == 1:
    for current_round in range(1, NUM_ROUNDS):
      scaled_public_good_matrix = calculuate_scaled_public_good(contributions_matrix, groups_matrix, NUM_PLAYERS, R)
      payoff_matrix = calculate_payoff_shared(contributions_matrix, groups_matrix, ENDOWMENT, scaled_public_good_matrix)
      contributions_matrix = update_contributions_shared(player_types_matrix, contributions_matrix, payoff_matrix, groups_matrix, ENDOWMENT, NUM_MEMBERSHIP, DELTA)

      round_avg_contribution[current_round] = np.sum(contributions_matrix) / (NUM_MEMBERSHIP*NUM_PLAYERS)

      metrics_of_interest_array_current = metrics_of_interest_array_builder(NUM_GROUPS, GROUP_SIZE, NUM_PLAYERS, current_round, current_sim)
      metrics_of_interest_array_current = update_metrics_of_interest(metrics_of_interest_array_current, contributions_matrix, groups_matrix)
      to_merge = [metrics_of_interest_array_all_rounds, metrics_of_interest_array_current]
      metrics_of_interest_array_all_rounds = pd.concat(to_merge)

  else:
    for current_round in range(1, NUM_ROUNDS):
      scaled_public_good_matrix = calculuate_scaled_public_good(contributions_matrix, groups_matrix, NUM_PLAYERS, R)
      payoff_matrix = calculate_payoff_split(contributions_matrix, groups_matrix, ENDOWMENT, scaled_public_good_matrix)
      contributions_matrix = update_contributions_split(player_types_matrix, contributions_matrix, payoff_matrix, groups_matrix, ENDOWMENT, NUM_MEMBERSHIP, DELTA)
            
      round_avg_contribution[current_round] = np.sum(contributions_matrix) / (NUM_MEMBERSHIP*NUM_PLAYERS)

      metrics_of_interest_array_current = metrics_of_interest_array_builder(NUM_GROUPS, GROUP_SIZE, NUM_PLAYERS, current_round, current_sim)
      metrics_of_interest_array_current = update_metrics_of_interest(metrics_of_interest_array_current, contributions_matrix, groups_matrix)
      to_merge = [metrics_of_interest_array_all_rounds, metrics_of_interest_array_current]
      metrics_of_interest_array_all_rounds = pd.concat(to_merge)

  return round_avg_contribution, metrics_of_interest_array_all_rounds