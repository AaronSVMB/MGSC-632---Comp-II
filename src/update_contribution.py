"""
Seperate page to define the functions incorporated in the update_contributions_xxx_dictionaries.
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
    """
    Takes in the contribution for a free-rider in the split endowment regime, implements stochasticity, and updates their
    contributions based on priors. 

    :param player: the player that has the type of being a free-rider
    :param contributions: their contributions to their groups in a round
    :param payoff_matrix: the payoff they received from their and their groups decisions in the previous round
    :param group_matrix: matrix regarding the group that each player is part of 
    :param ENDOWMENT: the points that, in this case, the player receives for groups in each round: since split 2 endowments
    :param NUM_MEMBERSHIP: the number of groups each player is a part of 
    :param NUM_GROUPS: the total number of groups
    :param DELTA: the players learning rate
    :param TREMBLE: the players chance of deviating from their player type
    :return: a free-riders updated contributions stored in the contributions matrix
    """
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
                contributions[player][group] += DELTA[player] * np.random.randint(0, math.floor(ENDOWMENT / NUM_MEMBERSHIP * DELTA[player]))
        contribution_index += 1
    return contributions 

def update_contributions_split_stochastic_conditional(player: int, contributions: np.ndarray, payoff_matrix: np.ndarray, 
                                        group_matrix: np.ndarray, ENDOWMENT: int, NUM_MEMBERSHIP: int, 
                                        NUM_GROUPS: int, DELTA: np.ndarray, TREMBLE: list):
    """
    Updated the contribution with stochasticity for a conditional cooperator in the  split endowment regime

    :param player: player who has the type of conditional cooperator
    :param contributions: their contribution 
    :param payoff_matrix: their payoff for their previous round choice
    :param group_matrix: what groups this player is involved with
    :param ENDOWMENT: the points that, in this case, the player receives for groups in each round: since split 2 endowments 
    :param NUM_MEMBERSHIP: the number of groups each player is part of 
    :param NUM_GROUPS: the total number of groups
    :param DELTA: the learning rates for each player
    :param TREMBLE: the chance each player has to deviate from their assigned strategy
    :return: returns the updated contributions for the conditional cooperator in the contribution matrix
    """
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
    """
    Updates the contributions with stochasticity for a player who is the type of being an 'altruist'

    :param player: the player who has the type of altruist
    :param contributions: the matrix of contributions in the previous round
    :param payoff_matrix: the matrix of payoffs for players in the previous round based off of the realized decisions in their groups
    :param group_matrix: matrix showing the group structure
    :param ENDOWMENT: the 2 separate endowments that each player receives and decides to allocate with
    :param NUM_MEMBERSHIP: the number of groups each player is part of 
    :param NUM_GROUPS: the total number of groups
    :param DELTA: the learning rate for each player 
    :param TREMBLE: the chance to deviate from their player type 
    :return: returns the updated contribution for one player of the altruist type via the full contribution matrix
    """
    contribution_index = 0
    for group in range(NUM_GROUPS):
        if contribution_index >= NUM_MEMBERSHIP:
            break
        if np.random.rand() > TREMBLE[2]:
            if group_matrix[player][group] == 1:
                contributions[player][group] = np.random.randint(contributions[player][group], ENDOWMENT / NUM_MEMBERSHIP)
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
    """
    Function to update the contributions under the shared endowment regime for a player who is a conditional cooperator. 
    Conditional cooperators compare their within-group analysis (their payoff based on their contribution) and features
    a between-group analysis (their payoff between/among their groups).

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
    """
    Updates contribution in the shared endowment for a player who is a freerider. 
    This player type is static at 0 contribution ATM.

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
                contributions[player][group] += np.random.randint(0, contributions[player][group] + 1) * DELTA[player]
        contribution_index += 1
    return contributions

def update_contributions_stochastic_shared_altruist(player: int, contributions: np.ndarray, payoff_matrix: np.ndarray, 
                                         group_matrix: np.ndarray, ENDOWMENT: int, NUM_MEMBERSHIP: int, 
                                         NUM_GROUPS: int, DELTA: np.ndarray, TREMBLE: list):
    """
    Updates contribution in shared endowment for a player who is an altruist. Not exactly an altruist. But seen as a person who values 'fairness'
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
# Builds functional dictionaries for the player types under both regimes. 
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