"""
TODO write a summary of what these functions do and what they're for
"""
import random

def update_contributions_split_freeride(player, contributions, payoff_matrix, group_matrix, ENDOWMENT, NUM_MEMBERSHIP, NUM_GROUPS):
    """
    eventually this can just be simply: return 0,0 (once I change the initialize function to be player type based)
    """
    contribution_index = 0
    for group in range(NUM_GROUPS):
        if contribution_index >= NUM_MEMBERSHIP:
            break
        if group_matrix[player][group] == 1:
            contributions[player][group] == 0 
        contribution_index +=1
    return contributions

def update_contributions_split_conditional(player, contributions, payoff_matrix, group_matrix, ENDOWMENT, NUM_MEMBERSHIP, NUM_GROUPS):
    """
    calculates the changes in contributions for a player who is of type 'conditional cooperator'. This player type bases their decisions off
    of their payoff in the previous round to their endowment (what could of been their personal account)
    """
    contribution_index = 0
    for group in range(NUM_GROUPS):
        if contribution_index >= NUM_MEMBERSHIP:
            break
        if group_matrix[player][group] == 1:
            if payoff_matrix[player][group] > (ENDOWMENT / NUM_MEMBERSHIP):
                if contributions[player][contribution_index] < ( ENDOWMENT / NUM_MEMBERSHIP):
                    increase_contribution = random.randint(0, (ENDOWMENT / NUM_MEMBERSHIP) - contributions[player][contribution_index])
                    contributions[player][contribution_index] += increase_contribution
            else:
                if contributions[player][contribution_index] > 0:
                    decrease_contribution = random.randint(0, contributions[player][contribution_index])
                    contributions[player][contribution_index] -=  decrease_contribution
            contributions[player][contribution_index] = min((ENDOWMENT / NUM_MEMBERSHIP), contributions[player][contribution_index] )
            contribution_index += 1 
    return contributions

#==========================================================================================
#==========================================================================================
def update_contributions_split_altruist(player, contributions, payoff_matrix, group_matrix, ENDOWMENT, NUM_MEMBERSHIP, NUM_GROUPS):
    """
    updates the contributions for a player who is of type altruist in the split endowment regime. I might change this function to add some variance
    to the contributions of an altruist rather than having a static player, but we will see
    """
    contribution_index = 0
    for group in range(NUM_GROUPS):
        if contribution_index >= NUM_MEMBERSHIP: 
            break
        if group_matrix[player][group] == 1:
            contributions[player][group] == ENDOWMENT / NUM_MEMBERSHIP
        contribution_index +=1
    return contributions

def update_contributions_shared_conditional(player, contributions, payoff_matrix, group_matrix, ENDOWMENT, NUM_MEMBERSHIP, NUM_GROUPS):
    """
    function to update the contributions under the shared endowment regime for a player who is a conditional cooperator. 
    Conditional cooperators compare their within-group analysis (their payoff based on their contribution) and features
    a between-group analysis (their payoff between/among their groups)
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
                    contributions[player][contribution_index] += increase_contribution
            else: # if player lost from cooperation in a group
                if contributions[player][contribution_index] > 0: 
                    decrease_contribution = random.randint(0, contributions[player][contribution_index])
                    contributions[player][contribution_index] -= decrease_contribution
            contributions[player][contribution_index] = min(ENDOWMENT, contributions[player][contribution_index])
            contribution_index += 1
    for member in range(NUM_MEMBERSHIP - 1): # check between-group analysis of comparative gains/losses
        if contributions[player][member] > 0 and contributions[player][member + 1] > 0:
            difference = int(abs(contributions[player][member] - contributions[player][member + 1]))
            transfer = random.randint(0, difference)
            if payoff_matrix[player][in_group[member]] > payoff_matrix[player][in_group[member + 1]] :
                contributions[player][member] += transfer
                contributions[player][member + 1] -= transfer
            else:   
                contributions[player][member] -= transfer
                contributions[player][member + 1] += transfer
    return contributions

def update_contributions_shared_freeride(player, contributions, payoff_matrix, group_matrix, ENDOWMENT, NUM_MEMBERSHIP, NUM_GROUPS):
    """
    updates contribution in the shared endowment for a player who is a freerider. This player type is static at 0 contribution ATM 
    """
    contribution_index = 0
    for group in range(NUM_GROUPS):
        if contribution_index > NUM_MEMBERSHIP - 1:
            break
        if group_matrix[player][group] == 1:
            contributions[player][group] == 0
        contribution_index += 1
    return contributions

def update_contributions_shared_altruist(player, contributions, payoff_matrix, group_matrix, ENDOWMENT, NUM_MEMBERSHIP, NUM_GROUPS):
    """
    updates contribution in shared endowment for a player who is an altruist. Not exactly an altruist. But seen as a person who values 'fairness'
    I am not sure how altruism would be defiend when constrained to giving to multiple groups. 
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