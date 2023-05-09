"""
Runs the public goods game for simulation number of times. Using the monte carlo method to derive
expected contributions at the player, groun, round, and simulation level.
"""

from src.public_goods_utils import *

#==========================================================================================
# Monte Carlo Simulation 
#==========================================================================================

def monte_carlo_simulation(SIMS: int):
  """
  Run game with same parameters simulation number of times. Stores as a data frame currently.

  :param SIMS: the number of simulations to run
  :return: Tuple - two dfs that store metrics on the MGPGG
  """
  current_round_avg_contribution, all_metrics_of_interest_df  = simulate_game(NUM_MEMBERSHIP, ENDOWMENT, SHARED, 
                                           GROUP_SIZE, R, NUM_GROUPS, NUM_PLAYERS, NUM_ROUNDS, METHOD, 0, TREMBLE)
  # Easy to access expected round contribution 
  all_round_avg_contribution_df = pd.DataFrame(current_round_avg_contribution).T
  

  for current_sim in range(1, SIMS):
    current_round_avg_contribution, current_metrics_of_interest_df  = simulate_game(NUM_MEMBERSHIP, ENDOWMENT, SHARED, 
                                           GROUP_SIZE, R, NUM_GROUPS, NUM_PLAYERS, NUM_ROUNDS, METHOD, current_sim, TREMBLE)
    
    #easy to aaccess expected round contribution
    current_round_contribution_df = pd.DataFrame(current_round_avg_contribution).T
    to_combine = [all_round_avg_contribution_df, current_round_contribution_df]
    all_round_avg_contribution_df = pd.concat(to_combine)

    ## MOI_DF
    to_merge = [all_metrics_of_interest_df, current_metrics_of_interest_df]
    all_metrics_of_interest_df = pd.concat(to_merge)

  col_dict, row_dict = {}, {}
  for a_round in range(NUM_ROUNDS):
    col_dict[a_round] = f"Round{a_round}"
  for a_sim in range(SIMS):
    row_dict[a_sim] = f"Simulation{a_sim}"

  all_round_avg_contribution_df.rename(columns = col_dict, index = row_dict, inplace = True)
  #TODO index = row_dict is not saving properly. all rows are called "Simulaton0" for now idk why
  all_round_avg_contribution_df['Simulation Mean'] = all_round_avg_contribution_df.mean(axis=1)
  all_round_avg_contribution_df.loc['Round Mean'] = all_round_avg_contribution_df.mean()

  all_metrics_of_interest_df.to_csv(f'metrics_of_interest_{SHARED}.csv')

  return all_round_avg_contribution_df