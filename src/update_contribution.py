"""
seperate page to define the functions incorporated in the update_contributions_xxxxx_dictionaries
"""
import random
import numpy as np
import math

#==========================================================================================
# Decion rules for the SPLIT endowment regime
#==========================================================================================

def update_contributions_split_stochastic_freerider(player: int, contributions: np.ndarray, payoff_matrix: np.ndarray, 
                                        group_matrix: np.ndarray, ENDOWMENT: int, NUM_MEMBERSHIP: int, 
                                        NUM_GROUPS: int, DELTA: np.ndarray, TREMBLE: list):
    contribution_index = 0
    for group in range(NUM_GROUPS):
        if contribution_index >- NUM_MEMBERSHIP:
            break
        if group_matrix[player][group] == 1:
            if np.random.rand() > TREMBLE[0]: # behaving normally
                if contributions[player][group] > 0:
                    new_contribution = max(0, np.random.randint(0, contributions[player][group])) * DELTA[player]
                    contributions[player][group] -= new_contribution
                    contributions[player][group] = max(0, contributions[player][group] )
            else: # behaving abnormally
                contributions[player][group] += DELTA[player] * np.random.randint(0, ENDOWMENT - sum(contributions[player][:]))
        contribution_index += 1
    return contributions 

def update_contributions_split_stochastic_conditional(player: int, contributions: np.ndarray, payoff_matrix: np.ndarray, 
                                        group_matrix: np.ndarray, ENDOWMENT: int, NUM_MEMBERSHIP: int, 
                                        NUM_GROUPS: int, DELTA: np.ndarray, TREMBLE: list):
    contribution_index = 0
    for group in range(NUM_GROUPS):
        if contribution_index >= NUM_MEMBERSHIP:
            break
        if group_matrix[player][group] == 1:
            if np.random.rand() > TREMBLE[1]:
                if group_matrix[player][group] == 1:
                    if payoff_matrix[player][group] > (ENDOWMENT / NUM_MEMBERSHIP):
                        if contributions[player][contribution_index] < ( ENDOWMENT / NUM_MEMBERSHIP):
                            increase_contribution = random.randint(0, (ENDOWMENT / NUM_MEMBERSHIP) - contributions[player][contribution_index])
                            contributions[player][contribution_index] += math.floor(increase_contribution * DELTA[player])
                else:
                    if contributions[player][contribution_index] > 0:
                        decrease_contribution = random.randint(0, contributions[player][contribution_index])
                        contributions[player][contribution_index] -=  math.floor(decrease_contribution * DELTA[player])
                contributions[player][contribution_index] = min((ENDOWMENT / NUM_MEMBERSHIP), contributions[player][contribution_index] )
                contribution_index += 1 
    return contributions

def update_contributions_split_stochastic_altruist(player: int, contributions: np.ndarray, payoff_matrix: np.ndarray, 
                                        group_matrix: np.ndarray, ENDOWMENT: int, NUM_MEMBERSHIP: int, 
                                        NUM_GROUPS: int, DELTA: np.ndarray, TREMBLE: list):
    contribution_index = 0
    for group in range(NUM_GROUPS):
        if contribution_index >= NUM_MEMBERSHIP:
            break
        if np.random.rand() > TREMBLE[2]:
            if group_matrix[player][group] == 1:
                contributions[player][group] = np.random.randint(contributions[player][group], ENDOWMENT // NUM_MEMBERSHIP)
        else:
            contributions[player][group] -= max(0, np.random.randint(0, contributions[player][group] )) * DELTA[player]
        contribution_index += 1
    return contributions

#==========================================================================================
# Decion rules for the SHARED endowment regime
#==========================================================================================

def update_contributions_stochastic_shared_conditional(player: int, contributions: np.ndarray, payoff_matrix: np.ndarray, 
                                            group_matrix: np.ndarray, ENDOWMENT: int, NUM_MEMBERSHIP: int,
                                              NUM_GROUPS: int, DELTA: np.ndarray, TREMBLE: list):
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
                    contributions[player][contribution_index] += math.floor(increase_contribution * DELTA[player])
            else: # if player lost from cooperation in a group
                if contributions[player][contribution_index] > 0: 
                    decrease_contribution = random.randint(0, contributions[player][contribution_index])
                    contributions[player][contribution_index] -= math.floor(decrease_contribution * DELTA[player])
            contributions[player][contribution_index] = min(ENDOWMENT, contributions[player][contribution_index])
            contribution_index += 1
    for member in range(NUM_MEMBERSHIP - 1): # check between-group analysis of comparative gains/losses
        if contributions[player][member] > 0 and contributions[player][member + 1] > 0:
            difference = int(abs(contributions[player][member] - contributions[player][member + 1]))
            transfer = math.floor(random.randint(0, difference) * DELTA[player])
            if payoff_matrix[player][in_group[member]] > payoff_matrix[player][in_group[member + 1]] :
                contributions[player][member] += transfer
                contributions[player][member + 1] -= transfer
            else:   
                contributions[player][member] -= transfer
                contributions[player][member + 1] += transfer
    if np.random.rand() < TREMBLE[1]:
        swap_one = contributions[player][0]
        swap_two =  contributions[player][1]
        contributions[player][0] = swap_one
        contributions[player][1] = swap_two
    contributions[player][0] = max(0,contributions[player][0])
    contributions[player][1] = max(0,contributions[player][1])
    return contributions

def update_contributions_stochastic_shared_freeride(player: int, contributions: np.ndarray, payoff_matrix: np.ndarray, 
                                         group_matrix: np.ndarray, ENDOWMENT: int, NUM_MEMBERSHIP: int, 
                                         NUM_GROUPS: int, DELTA: np.ndarray, TREMBLE: list):
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
            if np.random.rand() > TREMBLE[0]:
                if contributions[player][group] > 0:
                    contributions[player][group] -= np.random.randint(0, contributions[player][group])
            else:
                contributions[player][group] += np.random.randint(0, contributions[player][group]) * DELTA[player]
        contribution_index += 1
    return contributions

def update_contributions_stochastic_shared_altruist(player: int, contributions: np.ndarray, payoff_matrix: np.ndarray, 
                                         group_matrix: np.ndarray, ENDOWMENT: int, NUM_MEMBERSHIP: int, 
                                         NUM_GROUPS: int, DELTA: np.ndarray, TREMBLE: list):
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
            if np.random.rand() > TREMBLE[2]:
                if contributions[player][group] < ENDOWMENT / NUM_MEMBERSHIP:
                    contributions[player][group] = np.random.randint(contributions[player][group], ENDOWMENT / NUM_MEMBERSHIP)
            else:
                contributions[player][group] -= np.random.randint(0, ENDOWMENT / NUM_MEMBERSHIP) * DELTA[player]
        contribution_index += 1
    return contributions

#==========================================================================================
# builds functional dictionaries for the player types under both regimes. 
# Accessed by functions in public_goods_utils.py
#==========================================================================================

update_contributions_split_stochastic_dict = {0: update_contributions_split_stochastic_freerider,
                                   1: update_contributions_split_stochastic_conditional,
                                   2: update_contributions_split_stochastic_altruist
                                   }

update_contributions_stochastic_shared_dict = {0: update_contributions_stochastic_shared_freeride,
                                   1: update_contributions_stochastic_shared_conditional,
                                   2: update_contributions_stochastic_shared_altruist
                                   }
#==========================================================================================
#==========================================================================================