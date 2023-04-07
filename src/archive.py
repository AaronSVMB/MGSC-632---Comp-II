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
# Big Archive Additions – Pre-stochasticity functions April 6th 5:25 pm 2023
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
            if player_type == 2: # if they are an altruist
                initial_contributions[player][:] = ENDOWMENT / NUM_MEMBERSHIP
    return initial_contributions

def update_contributions_split_freeride(player: int, contributions: np.ndarray, payoff_matrix: np.ndarray, 
                                        group_matrix: np.ndarray, ENDOWMENT: int, NUM_MEMBERSHIP: int, 
                                        NUM_GROUPS: int, DELTA: float):
    """_summary_
    updates the contributions of a free-rider (does not update)
    :param player: individual player from NUM_PLAYERS
    :param contributions: matrix that displays the contribution of an individual
    :param payoff_matrix: matrix that dispalys the payoff a player gets from their group
    :param group_matrix: matrix that displays the groups that a player is a part of 
    :param ENDOWMENT: the resources each player gets at the start of the round 
    :param NUM_MEMBERSHIP: the number of groups each player is in
    :param NUM_GROUPS: the total number of groups
    :param DELTA: the learning rate from gradient descent
    :return: the updated contributions for a free-rider
    """
    contribution_index = 0
    for group in range(NUM_GROUPS):
        if contribution_index >= NUM_MEMBERSHIP:
            break
        if group_matrix[player][group] == 1:
            contributions[player][group] == 0 
        contribution_index +=1
    return contributions

def update_contributions_split_conditional(player: int, contributions: np.ndarray, payoff_matrix: np.ndarray,
                                           group_matrix: np.ndarray, ENDOWMENT: int, NUM_MEMBERSHIP: int, 
                                           NUM_GROUPS: int, DELTA: float):
    """_summary_
    Calculates the changes in contributions for a player who is of type 'conditional cooperator'. 
    This player type bases their decisions off of their payoff in the previous round to their
    endowment (what could of been their personal account)
    :param player: individual player from NUM_PLAYERS
    :param contributions: matrix that displays the contribution of an individual
    :param payoff_matrix: matrix that dispalys the payoff a player gets from their group
    :param group_matrix: matrix that displays the groups that a player is a part of 
    :param ENDOWMENT: the resources each player gets at the start of the round 
    :param NUM_MEMBERSHIP: the number of groups each player is in
    :param NUM_GROUPS: the total number of groups
    :param DELTA: the learning rate from gradient descent
    :return: the update contributions for a conditional cooperator
    """
    contribution_index = 0
    for group in range(NUM_GROUPS):
        if contribution_index >= NUM_MEMBERSHIP:
            break
        if group_matrix[player][group] == 1:
            if payoff_matrix[player][group] > (ENDOWMENT / NUM_MEMBERSHIP):
                if contributions[player][contribution_index] < ( ENDOWMENT / NUM_MEMBERSHIP):
                    increase_contribution = random.randint(0, (ENDOWMENT / NUM_MEMBERSHIP) - contributions[player][contribution_index])
                    contributions[player][contribution_index] += math.floor(increase_contribution * DELTA)
            else:
                if contributions[player][contribution_index] > 0:
                    decrease_contribution = random.randint(0, contributions[player][contribution_index])
                    contributions[player][contribution_index] -=  math.floor(decrease_contribution * DELTA)
            contributions[player][contribution_index] = min((ENDOWMENT / NUM_MEMBERSHIP), contributions[player][contribution_index] )
            contribution_index += 1 
    return contributions

def update_contributions_split_altruist(player: int, contributions: np.ndarray, payoff_matrix: np.ndarray, 
                                        group_matrix: np.ndarray, ENDOWMENT: int, NUM_MEMBERSHIP: int, 
                                        NUM_GROUPS: int, DELTA: float):
    """_summary_
    updates the contributions for a player who is of type altruist in the split endowment regime. I might change this function to add some variance
    to the contributions of an altruist rather than having a static player, but we will see.
    :param player: individual player from NUM_PLAYERS
    :param contributions: matrix that displays the contribution of an individual
    :param payoff_matrix: matrix that dispalys the payoff a player gets from their group
    :param group_matrix: matrix that displays the groups that a player is a part of 
    :param ENDOWMENT: the resources each player gets at the start of the round 
    :param NUM_MEMBERSHIP: the number of groups each player is in
    :param NUM_GROUPS: the total number of groups
    :param DELTA: the learning rate from gradient descent
    :return: updated contribution for an altruist in the split endowment
    """
    contribution_index = 0
    for group in range(NUM_GROUPS):
        if contribution_index >= NUM_MEMBERSHIP: 
            break
        if group_matrix[player][group] == 1:
            contributions[player][group] == ENDOWMENT / NUM_MEMBERSHIP
        contribution_index +=1
    return contributions

update_contributions_split_dict = {0: update_contributions_split_freeride,
                                   1: update_contributions_split_conditional,
                                   2: update_contributions_split_altruist
                                   }

def update_contributions_split(player_type_matrix: np.ndarray, contributions: np.ndarray, payoff_matrix: np.ndarray,
                                group_matrix: np.ndarray, ENDOWMENT: int, NUM_MEMBERSHIP: int, DELTA: float):
  """_summary_
  utilizes the 'update_contributions_split_dict' to update the contributions for all players based off their player types 
  :param player_type_matrix: matrix of size NUM_PLAYERS x 1 that displays each players type
  :param contributions: matrix that displays a palyers contributions to their group: NUM_PLAYERS x NUM_MEMBERSHIP
  :param payoff_matrix: the payoff that each individual gets from participating in their group
  :param group_matrix:  matrix that displays what groups a player is in: NUM_PLAYERS x NUM_GROUPS
  :param ENDOWMENT: the amount of resources given at the start of each round to players
  :param NUM_MEMBERSHIP: the number of groups each player is in 
  :param DELTA: gradient descent learning rate 
  :return: the updated contributions matrix for individuals to contribute in the current round based off their last rounds experience
  """
  for player in range(NUM_PLAYERS):
    player_type = int(player_type_matrix[player])
    update_contributions_split_use = update_contributions_split_dict[player_type]
    contributions = update_contributions_split_use(player, contributions, payoff_matrix, group_matrix, ENDOWMENT, NUM_MEMBERSHIP, NUM_GROUPS, DELTA)
  return contributions

def update_contributions_shared_conditional(player: int, contributions: np.ndarray, payoff_matrix: np.ndarray, 
                                            group_matrix: np.ndarray, ENDOWMENT: int, NUM_MEMBERSHIP: int,
                                              NUM_GROUPS: int, DELTA: float):
    """_summary_
    function to update the contributions under the shared endowment regime for a player who is a conditional cooperator. 
    Conditional cooperators compare their within-group analysis (their payoff based on their contribution) and features
    a between-group analysis (their payoff between/among their groups)
    :param player: individual player from NUM_PLAYERS
    :param contributions: matrix that displays the contribution of an individual
    :param payoff_matrix: matrix that dispalys the payoff a player gets from their group
    :param group_matrix: matrix that displays the groups that a player is a part of 
    :param ENDOWMENT: the resources each player gets at the start of the round 
    :param NUM_MEMBERSHIP: the number of groups each player is in
    :param NUM_GROUPS: the total number of groups
    :param DELTA: the learning rate from gradient descent
    :return: the updated contribution for a conditional cooperator in the shared endowment regime
    """
    contribution_index = 0
    in_group = []
    for group in range(NUM_GROUPS): # within-group analysis of gains/losses
        if contribution_index > NUM_MEMBERSHIP - 1:
            break
        if group_matrix[player][group] == 1:
            in_group.append(group)
            if payoff_matrix[player][group] >= 0: # checks if the player gained from cooperation
                current_players_total_contributions = contributions[player].sum()
                if current_players_total_contributions < ENDOWMENT:
                    increase_contribution = random.randint(0, ENDOWMENT - current_players_total_contributions)
                    contributions[player][contribution_index] += math.floor(increase_contribution * DELTA)
            else: # if player lost from cooperation in a group
                if contributions[player][contribution_index] > 0: 
                    decrease_contribution = random.randint(0, contributions[player][contribution_index])
                    contributions[player][contribution_index] -= math.floor(decrease_contribution * DELTA)
            contributions[player][contribution_index] = min(ENDOWMENT, contributions[player][contribution_index])
            contribution_index += 1
    for member in range(NUM_MEMBERSHIP - 1): # check between-group analysis of comparative gains/losses
        if contributions[player][member] > 0 and contributions[player][member + 1] > 0:
            difference = int(abs(contributions[player][member] - contributions[player][member + 1]))
            transfer = math.floor(random.randint(0, difference) * DELTA)
            if payoff_matrix[player][in_group[member]] > payoff_matrix[player][in_group[member + 1]] :
                contributions[player][member] += transfer
                contributions[player][member + 1] -= transfer
            else:   
                contributions[player][member] -= transfer
                contributions[player][member + 1] += transfer
    return contributions

def update_contributions_shared_freeride(player: int, contributions: np.ndarray, payoff_matrix: np.ndarray, 
                                         group_matrix: np.ndarray, ENDOWMENT: int, NUM_MEMBERSHIP: int, 
                                         NUM_GROUPS: int, DELTA: float):
    """_summary_
    updates contribution in the shared endowment for a player who is a freerider. 
    This player type is static at 0 contribution ATM
    :param player: individual player from NUM_PLAYERS
    :param contributions: matrix that displays the contribution of an individual
    :param payoff_matrix: matrix that dispalys the payoff a player gets from their group
    :param group_matrix: matrix that displays the groups that a player is a part of 
    :param ENDOWMENT: the resources each player gets at the start of the round 
    :param NUM_MEMBERSHIP: the number of groups each player is in
    :param NUM_GROUPS: the total number of groups
    :param DELTA: the learning rate from gradient descent
    :return: updated contribution for a free-rider under the shared endowment
    """
    contribution_index = 0
    for group in range(NUM_GROUPS):
        if contribution_index > NUM_MEMBERSHIP - 1:
            break
        if group_matrix[player][group] == 1:
            contributions[player][group] == 0
        contribution_index += 1
    return contributions

def update_contributions_shared_altruist(player: int, contributions: np.ndarray, payoff_matrix: np.ndarray, 
                                         group_matrix: np.ndarray, ENDOWMENT: int, NUM_MEMBERSHIP: int, 
                                         NUM_GROUPS: int, DELTA: float):
    """_summary_
    updates contribution in shared endowment for a player who is an altruist. Not exactly an altruist. But seen as a person who values 'fairness'
    I am not sure how altruism would be defiend when constrained to giving to multiple groups. 
    :param player: individual player from NUM_PLAYERS
    :param contributions: matrix that displays the contribution of an individual
    :param payoff_matrix: matrix that dispalys the payoff a player gets from their group
    :param group_matrix: matrix that displays the groups that a player is a part of 
    :param ENDOWMENT: the resources each player gets at the start of the round 
    :param NUM_MEMBERSHIP: the number of groups each player is in
    :param NUM_GROUPS: the total number of groups
    :param DELTA: the learning rate from gradient descent
    :return: updates the contribution for an altruist in the shared endowment regime
    """
    contribution_index = 0
    for group in range(NUM_GROUPS):
        if contribution_index > NUM_MEMBERSHIP - 1:
            break
        if group_matrix[player][group] == 1:
            contributions[player][group] == ENDOWMENT / NUM_MEMBERSHIP
        contribution_index += 1
    return contributions

update_contributions_shared_dict = {0: update_contributions_shared_freeride,
                                   1: update_contributions_shared_conditional,
                                   2: update_contributions_shared_altruist
                                   }

def update_contributions_shared(player_type_matrix: np.ndarray, contributions: np.ndarray, payoff_matrix: np.ndarray,
                                 group_matrix: np.ndarray, ENDOWMENT: int, NUM_MEMBERSHIP: int, DELTA: float):
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
    update_contributions_shared_use = update_contributions_shared_dict[player_type]
    contributions = update_contributions_shared_use(player, contributions, payoff_matrix, group_matrix, ENDOWMENT, NUM_MEMBERSHIP, NUM_GROUPS, DELTA)
  return contributions 

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

