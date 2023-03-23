"""
all funcitons necessary for playing the multi-group public goods game

:return: _description_
"""
import numpy as np
import random
from src.update_contribution import update_contributions_split_dict, update_contributions_shared_dict

#==========================================================================================
# Set up Parameters
#==========================================================================================

NUM_MEMBERSHIP = 2 # Number of groups each player interacts with
ENDOWMENT = 50 # The Endowment each player receives 
SHARED = 2 # 1 if the endowment is shared across groups | 0 if it is split
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
#
#==========================================================================================

def initailize_contribtions_with_player_types(NUM_PLAYERS: int, NUM_MEMBERSHIP: int, 
                                                ENDOWMENT: int, SHARED: bool, player_type_matrix: np.ndarray):
    """
    _summary_
    TODO all docstrings. Use autodcostring extension pls. ty
    :param NUM_PLAYERS: _description_
    :param NUM_MEMBERSHIP: _description_
    :param ENDOWMENT: _description_
    :param SHARED: _description_
    :param player_type_matrix: _description_
    :return: _description_
    """
    initial_contributions = np.zeros([NUM_PLAYERS,NUM_MEMBERSHIP]) 
    if SHARED:
        for player in range(NUM_PLAYERS):
            player_type = player_type_matrix[player]
            if player_type == 1: 
                #initial_contribution_first_group = random.randint(0, ENDOWMENT)
                initial_contribution_first_group =  int(np.random.normal(ENDOWMENT / NUM_MEMBERSHIP, ENDOWMENT / 5 )) # Trying out NORMAL DIST 
                initial_contribution_first_group = min(ENDOWMENT, initial_contribution_first_group)
                initial_contribution_first_group = max(0, initial_contribution_first_group ) # With normal DIST make sure it is within my bounds of feasibility

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
                    #initial_contributions[player][group_member] = random.randint(0,(ENDOWMENT / NUM_MEMBERSHIP))
                    initial_contributions[player][group_member] = int(np.random.normal(ENDOWMENT / NUM_MEMBERSHIP*2, ENDOWMENT / 5)) # Trying out NORMAL DIST 
                    initial_contributions[player][group_member] = min(ENDOWMENT, initial_contributions[player][group_member])
                    initial_contributions[player][group_member] = max(0, initial_contributions[player][group_member]) # when using normal DISt make sure within bounds
            if player_type == 2: # if they are an altruist
                initial_contributions[player][:] = ENDOWMENT / NUM_MEMBERSHIP
    return initial_contributions

def formed_groups_matrix(GROUP_SIZE, NUM_GROUPS):
  """
  Function to form groups in the form of a matrix in a NUM_PLAYERS x NUM_GROUPS
  sized matrix. Currently it is hard coded for NUM_PLAYERS = 16, NUM_GROUPS =8,
  and NUM_MEMBERSHIP = 2. I have drawn out on paper trends that the different 
  combinations results in, but I am unsure of how to append players in a reason-
  able about of time. Previously I was using a while loop, but ...
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

def calculuate_scaled_public_good(contributions, groups_matrix, NUM_PLAYERS, R):
  """
  Function to sum up the contributions in a given group and then scale it by the
  scale factor. Since it matters which contribution goes to which group I keep
  track of a contribution_index variable
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

def calculate_payoff_split(contributions, group_matrix, ENDOWMENT, scaled_public_good):
  """
  Calculates the payoff when the groups are economically independent (split endowment)
  this case is easier so I implemented it first
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


def initialize_player_types(NUM_PLAYERS, update_contributions_split_dict, METHOD):
    """
    initializes the player types based off of different global parameter specified mixes 
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

def update_contributions_split(player_type_matrix, contributions, payoff_matrix, group_matrix, ENDOWMENT, NUM_MEMBERSHIP):
    """
    utilizes the 'update_contributions_split_dict' to update the contributions for all players based off their player types 
    """
    for player in range(NUM_PLAYERS):
        player_type = int(player_type_matrix[player])
        update_contributions_split_use = update_contributions_split_dict[player_type]
        contributions = update_contributions_split_use(player, contributions, payoff_matrix, group_matrix, ENDOWMENT, NUM_MEMBERSHIP, NUM_GROUPS)
    return contributions

#==========================================================================================
#==========================================================================================

def calculate_payoff_shared(contributions, group_matrix, ENDOWMENT, scaled_public_good):
  """
  How to calculate the payoff for an indiivdal contributing to their groups
  The endowment is removed since it would be double counted
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

def update_contributions_shared(player_type_matrix, contributions, payoff_matrix, group_matrix, ENDOWMENT, NUM_MEMBERSHIP):
    """
    updates contribution for all players in the shared endowment regime. Uses the 'update_contributions_shared_dict' to access their player-type
    specific update function
    """
    for player in range(NUM_PLAYERS):
        player_type = int(player_type_matrix[player])
        update_contributions_shared_use = update_contributions_shared_dict[player_type]
        contributions = update_contributions_shared_use(player, contributions, payoff_matrix, group_matrix, ENDOWMENT, NUM_MEMBERSHIP, NUM_GROUPS)
    return contributions 