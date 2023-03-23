"""
all funcitons necessary for playing the multi-group public goods game
"""
import numpy as np
import pandas as pd
import random
from src.update_contribution import update_contributions_split_dict, update_contributions_shared_dict

#==========================================================================================
# Set up Parameters
#==========================================================================================

NUM_MEMBERSHIP = 2 # Number of groups each player interacts with
ENDOWMENT = 50 # The Endowment each player receives 
SHARED = 1 # 1 if the endowment is shared across groups | 0 if it is split
GROUP_SIZE = 4 # size of each group
R = 0.5 # Scale factor
NUM_ROUNDS = 10 # Number of rounds that players will participate in the public good game

## When NUM_MEMBERSHIP == 2
NUM_GROUPS = GROUP_SIZE * 2 # number of groups
NUM_PLAYERS = GROUP_SIZE ** 2 # Number of players in the system

# Player type initialize 
METHOD = "conditional" # can take on values 'random', 'conditional', 'altruists', and 'mixed'

# For Monte Carlo Simulation
SIMS = 10000


#==========================================================================================
# Functions used regardless of ENDOWMENT scheme
#==========================================================================================

def initailize_contribtions_with_player_types(NUM_PLAYERS: int, NUM_MEMBERSHIP: int, 
                                                ENDOWMENT: int, SHARED: bool, player_type_matrix: np.ndarray):
    """
    _summary_
    Initializes contributions matrix. Different playertypes startoff giving different amounts. Initial contributions
    also differs between endowment schemes.
    :param NUM_PLAYERS: the number of players in the public goods game
    :param NUM_MEMBERSHIP: the number of groups each player is in 
    :param ENDOWMENT: the amount of resources given at the start of each round to players
    :param SHARED: boolean: 1 if the endowment is shared | 0 if the endowment is split
    :param player_type_matrix: NUM_PLAYERS x 1 - displays the type of the player
    :return: contributions_matrix size NUM_PLAYERS x NUM_MEMBERSHIP. cells are the contributions to that group
    """
    initial_contributions = np.zeros([NUM_PLAYERS,NUM_MEMBERSHIP]) 
    if SHARED == 1:
        for player in range(NUM_PLAYERS):
            player_type = player_type_matrix[player]
            if player_type == 1: 
                initial_contribution_first_group = random.randint(0, ENDOWMENT)
                #initial_contribution_first_group =  int(np.random.normal(ENDOWMENT / NUM_MEMBERSHIP, ENDOWMENT / 5 )) # Trying out NORMAL DIST 
                #initial_contribution_first_group = min(ENDOWMENT, initial_contribution_first_group)
                #initial_contribution_first_group = max(0, initial_contribution_first_group ) # With normal DIST make sure it is within my bounds of feasibility

                initial_contributions[player][0] = initial_contribution_first_group
                for member in range(1, NUM_MEMBERSHIP):
                    successive_initial_contributions = random.randint(0,ENDOWMENT - initial_contribution_first_group)
                    initial_contributions[player][member] = successive_initial_contributions
                    initial_contribution_first_group += successive_initial_contributions
            if player_type == 2: # if altruist : this more so resembles "fairness" not altruism 
                initial_contributions[player][:] = ENDOWMENT / NUM_MEMBERSHIP
    else:
        for player in range(NUM_PLAYERS):
            player_type = player_type_matrix[player]
            if player_type == 1: # if they are a conditional cooperator
                for group_member in range(NUM_MEMBERSHIP):
                    initial_contributions[player][group_member] = random.randint(0,(ENDOWMENT / NUM_MEMBERSHIP))
                    #initial_contributions[player][group_member] = int(np.random.normal(ENDOWMENT / NUM_MEMBERSHIP*2, ENDOWMENT / 5)) # Trying out NORMAL DIST 
                    #initial_contributions[player][group_member] = min(ENDOWMENT, initial_contributions[player][group_member])
                    #initial_contributions[player][group_member] = max(0, initial_contributions[player][group_member]) # when using normal DISt make sure within bounds
            if player_type == 2: # if they are an altruist
                initial_contributions[player][:] = ENDOWMENT / NUM_MEMBERSHIP
    return initial_contributions

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

def update_contributions_split(player_type_matrix: np.ndarray, contributions: np.ndarray, payoff_matrix: np.ndarray,
                                group_matrix: np.ndarray, ENDOWMENT: int, NUM_MEMBERSHIP: int):
  """_summary_
  utilizes the 'update_contributions_split_dict' to update the contributions for all players based off their player types 
  :param player_type_matrix: matrix of size NUM_PLAYERS x 1 that displays each players type
  :param contributions: matrix that displays a palyers contributions to their group: NUM_PLAYERS x NUM_MEMBERSHIP
  :param payoff_matrix: the payoff that each individual gets from participating in their group
  :param group_matrix:  matrix that displays what groups a player is in: NUM_PLAYERS x NUM_GROUPS
  :param ENDOWMENT: the amount of resources given at the start of each round to players
  :param NUM_MEMBERSHIP: the number of groups each player is in 
  :return: the updated contributions matrix for individuals to contribute in the current round based off their last rounds experience
  """
  for player in range(NUM_PLAYERS):
    player_type = int(player_type_matrix[player])
    update_contributions_split_use = update_contributions_split_dict[player_type]
    contributions = update_contributions_split_use(player, contributions, payoff_matrix, group_matrix, ENDOWMENT, NUM_MEMBERSHIP, NUM_GROUPS)
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

def update_contributions_shared(player_type_matrix: np.ndarray, contributions: np.ndarray, payoff_matrix: np.ndarray,
                                 group_matrix: np.ndarray, ENDOWMENT: int, NUM_MEMBERSHIP: int):
  """_summary_
  updates contribution for all players in the shared endowment regime. Uses the 'update_contributions_shared_dict' 
  to access their player-type specific update function
  :param player_type_matrix: matrix of size NUM_PLAYERS x 1 that displays each players type
  :param contributions: matrix that displays a palyers contributions to their group: NUM_PLAYERS x NUM_MEMBERSHIP
  :param payoff_matrix: the payoffs individuals get for being in their groups
  :param group_matrix: matrix that displays what groups a player is in: NUM_PLAYERS x NUM_GROUPS
  :param ENDOWMENT: the amount of resources given at the start of each round to players
  :param NUM_MEMBERSHIP: the number of groups each player is in 
  :return: the updated contributions for players to give in the current round based on their previous rounds experience
  """
  for player in range(NUM_PLAYERS):
    player_type = int(player_type_matrix[player])
    update_contributions_shared_use = update_contributions_shared_dict[player_type]
    contributions = update_contributions_shared_use(player, contributions, payoff_matrix, group_matrix, ENDOWMENT, NUM_MEMBERSHIP, NUM_GROUPS)
  return contributions 

#==========================================================================================
# Functions to store relevant data from rounds of the public goods game
#==========================================================================================

def metrics_of_interest_array_builder(NUM_GROUPS: int, GROUP_SIZE: int):
  """_summary_
  Builds an array to store information from each round of the public goods game
  :param NUM_GROUPS: the total number of groups
  :param GROUP_SIZE: the size of each group
  :return: a blank matrix of size GROUP_SZIE x NUM_GROUPS to store relevant information
  """
  metrics_of_interest_array = formed_groups_matrix(GROUP_SIZE, NUM_GROUPS)
  metrics_of_interest_array[metrics_of_interest_array==0] = 'nan'
  return metrics_of_interest_array

def update_metrics_of_interest(metrics_of_interest_array: np.ndarray, contributions_matrix: np.ndarray):
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
        if metrics_of_interest_array[player][group] == 1:
          metrics_of_interest_array[player][group] = contributions_matrix[player][contribution_index]
          contribution_index += 1
  group_means = np.nanmean(metrics_of_interest_array, axis = 0, keepdims = True) # sum of columns
  metrics_of_interest_array = np.append(metrics_of_interest_array, group_means, axis = 0)
    
  player_means = np.nanmean(metrics_of_interest_array, axis = 1, keepdims = True) # sum of rows
  metrics_of_interest_array = np.append(metrics_of_interest_array, player_means, axis = 1)

  metrics_of_interest_df = pd.DataFrame(metrics_of_interest_array)
  column_dict, row_dict = {}, {}
  for group in range(NUM_GROUPS):
    column_dict[group] = f"group{group}"
  for player in range(NUM_PLAYERS):
    row_dict[player] = f"player{player}"
  column_dict[NUM_GROUPS] = 'playeravg'
  row_dict[NUM_PLAYERS] = 'groupavg'
  metrics_of_interest_df.rename(columns = column_dict, index = row_dict, inplace=True) 
    # Rather than write to csv each time. Append each to a pandas df and only call the csv to write to it once at the end. 
    # this will make it so I don't have to call the csv file, and it doesn't slow down the code 
    # create a column called player ID, create a column for Round ID
    #TODO Add a column for Player ID and for Round #
  return metrics_of_interest_df