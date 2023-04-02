"""_summary_
Tests various functions from the public_goods_utils.py. 
"""
from src.public_goods_utils import *

#==========================================================================================
# Currently Working on: Incorrect behavior when scale factor is defined correctly. Going to re-analyze the central
# functions to the PGG

# it is weird, all of my calculuate functions work as intended. So that leads me to believe that there is an issue
# with either, the initial contributions being too high (maybe they should be scaled down? more accurately reflect
# what we expect to occur in the lab) OR that there is a significant error in my decision rules for both of my 
# simulations which could also be possible 
#==========================================================================================

def test_hello_world():
  print("Hello World!")

#==========================================================================================
# For now, moving on to looking at utilizing a vectorized lookup table
#==========================================================================================

player_types_example = initialize_player_types(NUM_PLAYERS, update_contributions_split_dict, METHOD='conditional')
contributions_example = initailize_contribtions_with_player_types(NUM_PLAYERS,NUM_MEMBERSHIP,ENDOWMENT,SHARED,player_types_example)
group_matrix_example = formed_groups_matrix(GROUP_SIZE,NUM_GROUPS)

print(contributions_example)
print(group_matrix_example)

def calculuate_scaled_public_good_vectorized(contributions: np.ndarray, groups_matrix: np.ndarray, NUM_PLAYERS: int, R: float):
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

