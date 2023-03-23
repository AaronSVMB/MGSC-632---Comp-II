"""
seperate page to define the functions incorporated in the update_contributions_xxxxx_dictionaries
"""
import random
import numpy as np
import math

#==========================================================================================
# Decion rules for the SPLIT endowment regime
#==========================================================================================

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

#==========================================================================================
# Decion rules for the SHARED endowment regime
#==========================================================================================

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

#==========================================================================================
# builds functional dictionaries for the player types under both regimes. 
# Accessed by functions in public_goods_utils.py
#==========================================================================================

update_contributions_split_dict = {0: update_contributions_split_freeride,
                                   1: update_contributions_split_conditional,
                                   2: update_contributions_split_altruist
                                   }

update_contributions_shared_dict = {0: update_contributions_shared_freeride,
                                   1: update_contributions_shared_conditional,
                                   2: update_contributions_shared_altruist
                                   }
#==========================================================================================
#==========================================================================================