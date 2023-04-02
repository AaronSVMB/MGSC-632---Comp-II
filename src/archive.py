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

test_game = simulate_game(NUM_MEMBERSHIP, ENDOWMENT, SHARED, GROUP_SIZE, R, NUM_GROUPS, NUM_PLAYERS, NUM_ROUNDS, METHOD, 0)
print(SHARED)
print(test_game[0])
print(test_game[1])

test_mc = monte_carlo_simulation(SIMS)
print(test_mc)

x = [i for i in range(NUM_ROUNDS)]
y = example_MC[1][:-1]
plt.title(f"Endowment: {ENDOWMENT}, Shared: {SHARED}, In How many groups?: {NUM_MEMBERSHIP}, Group Size: {GROUP_SIZE}, Sims: {SIMS}")
plt.xlabel("Round")
plt.ylabel("Expected Round Contribution")
plt.plot(x, y, color ="green")
plt.show()

#==========================================================================================
# March 26th
#==========================================================================================

example_round_avg = player_round_average_contributions(metrics_of_interest, SIMS, NUM_PLAYERS, NUM_ROUNDS)

player_round_avg_contribution_graph(example_round_avg)


player_avg_bar_chart(example_round_avg)

x = group_round_average_contribution(metrics_of_interest, NUM_GROUPS, NUM_ROUNDS, SIMS)
print(x)

#Did Once I do the above, I can make better graphs that show (1) average group level cooperation, (2) average player level coop, (3) average round level coop, etc.

#==========================================================================================
# March 30th (sent to archive)
#==========================================================================================

metrics_of_interest = pd.read_csv('metrics_of_interest.csv', index_col = 0)

example_round_avg = player_round_average_contributions(metrics_of_interest, SIMS, NUM_PLAYERS, NUM_ROUNDS)

player_round_avg_contribution_graph(example_round_avg)


player_avg_bar_chart(example_round_avg)

x = group_round_average_contribution(metrics_of_interest, NUM_GROUPS, NUM_ROUNDS, SIMS)
print(x)


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

"""def simulate_game_old(NUM_MEMBERSHIP, ENDOWMENT, SHARED, GROUP_SIZE, R, NUM_GROUPS, NUM_PLAYERS, NUM_ROUNDS, METHOD):
    #Simulate multiple rounds of the multi-group public goods game. The different cases are for which endowment regime is in place, SHARED or SPLIT
    #for which there exists two distinct function families
    player_types_matrix = initialize_player_types(NUM_PLAYERS, update_contributions_split_dict, METHOD)
    contributions_matrix = initailize_contribtions_with_player_types(NUM_PLAYERS, NUM_MEMBERSHIP, ENDOWMENT, SHARED, player_types_matrix)
    groups_matrix = formed_groups_matrix(GROUP_SIZE, NUM_GROUPS)

    metrics_of_interest_array = metrics_of_interest_array_builder(NUM_GROUPS, GROUP_SIZE)
    metrics_of_interest_array = update_metrics_of_interest(metrics_of_interest_array, contributions_matrix)
    if SIMS == 1:
        np.savetxt('moi.csv', metrics_of_interest_array, delimiter=',') 
    with open('moi.csv', 'a',  newline = '\n') as f:
        f.write(f"Round Number INIT\n")
        np.savetxt(f, metrics_of_interest_array, delimiter=',')

    round_avg_contribution = np.zeros(NUM_ROUNDS+1) # keeping for now. Stores the round level average contribution across all groups & players
    round_avg_contribution[0] = np.sum(contributions_matrix) / (NUM_MEMBERSHIP*NUM_PLAYERS) # the bottom right most cell of m_o_i_a stores this also

    if SHARED == 1:
        for round in range(NUM_ROUNDS):
            scaled_public_good_matrix = calculuate_scaled_public_good(contributions_matrix, groups_matrix, NUM_PLAYERS, R)
            payoff_matrix = calculate_payoff_shared(contributions_matrix, groups_matrix, ENDOWMENT, scaled_public_good_matrix)
            contributions_matrix = update_contributions_shared(player_types_matrix, contributions_matrix, payoff_matrix, groups_matrix, ENDOWMENT, NUM_MEMBERSHIP)

            round_avg_contribution[round+1] = np.sum(contributions_matrix) / (NUM_MEMBERSHIP*NUM_PLAYERS)

            metrics_of_interest_array = metrics_of_interest_array_builder(NUM_GROUPS, GROUP_SIZE)
            metrics_of_interest_array = update_metrics_of_interest(metrics_of_interest_array, contributions_matrix)
            with open('moi.csv', 'a',  newline = '\n') as f:
                f.write(f"Round Number {round}\n")
                np.savetxt(f, metrics_of_interest_array, delimiter=',')

    else:
        for round in range(NUM_ROUNDS):
            scaled_public_good_matrix = calculuate_scaled_public_good(contributions_matrix, groups_matrix, NUM_PLAYERS, R)
            payoff_matrix = calculate_payoff_split(contributions_matrix, groups_matrix, ENDOWMENT, scaled_public_good_matrix)
            contributions_matrix = update_contributions_split(player_types_matrix, contributions_matrix, payoff_matrix, groups_matrix, ENDOWMENT, NUM_MEMBERSHIP)
            
            round_avg_contribution[round+1] = np.sum(contributions_matrix) / (NUM_MEMBERSHIP*NUM_PLAYERS)

            metrics_of_interest_array = metrics_of_interest_array_builder(NUM_GROUPS, GROUP_SIZE)
            metrics_of_interest_array = update_metrics_of_interest(metrics_of_interest_array, contributions_matrix)
            with open('moi.csv', 'a', newline= '\n') as f:
                f.write(f"Round Number {round}\n")
                np.savetxt(f, metrics_of_interest_array, delimiter=',')
                
    return  round_avg_contribution"""

#==========================================================================================
# Completed TODOs
#==========================================================================================

# Added specified player type proportions (population wide / or within groups if I am staying with group_size == 4 num_membership == 2)

#DID Add player types and improved decision rule(s) for shared endowment case 
# Started on. The current decison rule works. Want to improve it even more
# M-20 Improved on it even more. Added between-group comparison for SHARED endowment.

#DID Initialize contributions for SHARED endowment case with player types
# Completed

#DID Fix Simulate Game Function for Shared Endowment Case
# Completed

#DID Improve the way my csv file looks and make sure it works with the monte carlo simulation portion (I think I am only saving the final iterations data as it stands)
# Completed. It now saves data from all iterations of the Simulation. HOWEVER !!!

## Completed Switch from numpyarray for MOI ==> Pandas DF. to_csv, as well as naming the rows/columns will be of
# great importance for my capacity to use the data in the future 
# Did, but now I cannot open the CSV FILE PROPERLY