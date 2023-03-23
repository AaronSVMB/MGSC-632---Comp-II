"""_summary_
Old code that I did not yet want to delete. Mostly code that I did not want to lose, butno longer want in 
my 'working space' of my Jupyter notebook file.
"""

#==========================================================================================
# Old tests
#==========================================================================================

player_types_matrix = initialize_player_types(NUM_PLAYERS,update_contributions_split_dict, METHOD = 'conditional')
player_types_matrix

contributions_example = initailize_contribtions_with_player_types(NUM_PLAYERS, NUM_MEMBERSHIP, ENDOWMENT, SHARED, player_types_matrix)
groups_example = formed_groups_matrix(GROUP_SIZE, NUM_GROUPS)
scaled_good_example = calculuate_scaled_public_good(contributions_example, groups_example, NUM_PLAYERS, R)
payoff_split_example = calculate_payoff_split(contributions_example, groups_example, ENDOWMENT, scaled_good_example)

print(contributions_example)
updated_contributions = update_contributions_split(player_types_matrix, contributions_example, payoff_split_example, groups_example, ENDOWMENT, NUM_MEMBERSHIP)
print("New")
updated_contributions

player_types_matrix = initialize_player_types(NUM_PLAYERS, update_contributions_split_dict, METHOD = 'conditional')
contributions_example = initailize_contribtions_with_player_types(NUM_PLAYERS, NUM_MEMBERSHIP, ENDOWMENT, SHARED, player_types_matrix)
scaled_public_good = calculuate_scaled_public_good(contributions_example, groups_example, NUM_PLAYERS, R)
shared_payoff_example = calculate_payoff_shared(contributions_example, groups_example, ENDOWMENT, scaled_public_good)
print(shared_payoff_example)
print(contributions_example)
print('New')

updated_contributions = update_contributions_shared(player_types_matrix, contributions_example, shared_payoff_example, groups_example, ENDOWMENT, NUM_MEMBERSHIP)
updated_contributions
#updated_contributions = update_contributions_shared_conditional(1, contributions_example, shared_payoff_example, groups_example, ENDOWMENT, NUM_MEMBERSHIP)
#updated_contributions[1]

contributions_example
metrics_example = metrics_of_interest_array_builder(NUM_GROUPS, GROUP_SIZE)
print(metrics_example)
metrics_example = update_metrics_of_interest(metrics_example, contributions_example)
print('New')
metrics_example

#==========================================================================================
# Old functional forms
#==========================================================================================

#def initailize_contribtions_with_player_types(NUM_PLAYERS, NUM_MEMBERSHIP, ENDOWMENT, SHARED, player_type_matrix):
   # initial_contributions = np.zeros([NUM_PLAYERS,NUM_MEMBERSHIP]) 
   # if SHARED:
""" for i in range(NUM_PLAYERS):
            initial_contribution_first_group = random.randint(0, ENDOWMENT)
            initial_contributions[i][0] = initial_contribution_first_group
            for j in range(1, NUM_MEMBERSHIP):
                successive_initial_contributions = random.randint(0,ENDOWMENT - initial_contribution_first_group)
                initial_contributions[i][j] = successive_initial_contributions
                initial_contribution_first_group += successive_initial_contributions"""