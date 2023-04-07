from src.public_goods_utils import *
import math
#==========================================================================================
# New Parameter
#==========================================================================================

TREMBLE = [0.1, 0.1, 0.1] # 0 is F-R, 1 CC, 2 Alt
# How likely they are to deviate from their strategy (of their player type)

#==========================================================================================
# NEW DELTA
#==========================================================================================

def init_delta(player_type_matrix: np.ndarray, NUM_PLAYERS: int):
    """_summary_
    Endogenizing the learning rates (for gradient descent) of each player. This initializes player
    learning rates for each iteration of a simulation
    :param player_type_matrix: the types of each player: 0 F-r, 1 CC, 2, Alt
    :param NUM_PLAYERS: the number of players
    :return: returns a column vector of each player DELTA; increases stochasticity
    """
    DELTA = np.zeros([NUM_PLAYERS,1])
    for player in range(NUM_PLAYERS):
        player_type = player_type_matrix[player]
        if player_type == 1: # conditional cooperator
            DELTA[player] = np.random.normal(0.75, 0.25)
        else: # arguing that free-riders and altruists are less responsive (less likely to learn)
            DELTA[player] = abs(np.random.standard_normal()) * 0.7
        DELTA[player] = max(0.65,DELTA[player])
        DELTA[player] = min(1, DELTA[player])
    return DELTA

def update_delta(DELTA: np.ndarray, NUM_PLAYERS: int):
    """_summary_
    After each round, update the learning rate of the players. I have it assumed now that
    each player, regardless of player type and realized contribution, decreases their
    learning rates as the number of rounds increases
    :param DELTA: the learning rate of each player stored in np.ndarray NUM_PLAYERS x 1
    :param NUM_PLAYERS: the number of players
    :return: the updated DELTA values for each player as an np.ndarray
    """
    prob = 0.5
    for player in range(NUM_PLAYERS):
        if DELTA[player] > 0:
            if np.random.rand() < prob:
                DELTA[player] -= (DELTA[player]**2) *np.random.rand() # This might be too oppressive but we shall we
        DELTA[player] = max(0, DELTA[player])
    return DELTA

#==========================================================================================
# Initialize player Contributions with new distribution 
#==========================================================================================

def initialize_contributions_with_distribution(NUM_PLAYERS: int, NUM_MEMBERSHIP: int, 
                                               ENDOWMENT: int, SHARED: bool, player_type_matrix: np.ndarray, DELTA: np.ndarray):
    initial_contributions = np.zeros([NUM_PLAYERS, NUM_MEMBERSHIP])
    if SHARED == 1:
        for player in range(NUM_PLAYERS):
            player_type = player_type_matrix[player]
            if player_type == 0:
                if np.random.rand() < TREMBLE[0]: # chance for free-rider to deviate in initial round
                    initial_contributions[player][0] = np.random.randint(0, ENDOWMENT * 0.15)
                for member in range(1, NUM_MEMBERSHIP):
                    initial_contributions[player][member] = np.random.randint(0, ENDOWMENT * 0.15)
            if player_type == 1:
                initial_contribution_first_group = max(0, np.random.normal(ENDOWMENT * 0.5, ENDOWMENT * 0.25))
                initial_contribution_first_group = min(ENDOWMENT, initial_contribution_first_group)
                initial_contributions[player][0] = int(initial_contribution_first_group)
                for member in range(1, NUM_MEMBERSHIP):
                    successive_contribution = max(0, np.random.normal(ENDOWMENT * 0.5, ENDOWMENT * 0.25))
                    successive_contribution = min(successive_contribution, ENDOWMENT - initial_contribution_first_group)
                    initial_contributions[player][member] = int(successive_contribution)
                    initial_contribution_first_group += successive_contribution
            if player_type == 2: # chance for altruist to deviate from player type in initial contribution
                if np.random.rand() > TREMBLE[2]:
                    initial_contributions[player][:] = np.random.randint((ENDOWMENT / NUM_MEMBERSHIP) * 0.85,
                                                                         ENDOWMENT / NUM_MEMBERSHIP)
                else:
                    initial_contributions[player][:] = np.random.randint((ENDOWMENT / NUM_MEMBERSHIP) * 0.5,
                                                                         ENDOWMENT / NUM_MEMBERSHIP)
    else:
        for player in range(NUM_PLAYERS):
            player_type = player_type_matrix[player]
            for group_member in range(NUM_MEMBERSHIP):
                contribution_amount = np.random.randint(0, ENDOWMENT / NUM_MEMBERSHIP)
                if player_type == 0:
                    initial_contributions[player][group_member] = np.random.randint(0, contribution_amount* 0.15)
                if player_type == 1:
                     initial_contributions[player][group_member] = contribution_amount 
                if player_type == 2:
                    initial_contributions[player][group_member] =  np.random.randint((ENDOWMENT / NUM_MEMBERSHIP) * 0.75, ENDOWMENT / NUM_MEMBERSHIP)
    for player in range(NUM_PLAYERS):
        initial_contributions[player][:] *= DELTA[player]
    initial_contributions = np.round(initial_contributions)
    initial_contributions = initial_contributions.astype(int)
    return initial_contributions # avg contribution is a little high, but workable (can make better later, but at least I have stochasticity here now)


#==========================================================================================
# Adding TREMBLE and new DELTA to Decion rules for the SPLIT endowment regime
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

update_contributions_split_stochastic_dict = {0: update_contributions_split_stochastic_freerider,
                                   1: update_contributions_split_stochastic_conditional,
                                   2: update_contributions_split_stochastic_altruist
                                   }

def update_contributions_stochastic_split(player_type_matrix: np.ndarray, contributions: np.ndarray, payoff_matrix: np.ndarray,
                                group_matrix: np.ndarray, ENDOWMENT: int,
                                  NUM_MEMBERSHIP: int, DELTA: np.ndarray, TREMBLE: list):
    for player in range(NUM_PLAYERS):
        player_type = int(player_type_matrix[player])
        update_contributions_split_use = update_contributions_split_stochastic_dict[player_type]
        contributions = update_contributions_split_use(player, contributions, payoff_matrix, group_matrix, ENDOWMENT, NUM_MEMBERSHIP, NUM_GROUPS, DELTA, TREMBLE)
    return contributions


#==========================================================================================
# Decion rules for the SHARED endowment regime with TREMBLE and new DELTA
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

update_contributions_stochastic_shared_dict = {0: update_contributions_stochastic_shared_freeride,
                                   1: update_contributions_stochastic_shared_conditional,
                                   2: update_contributions_stochastic_shared_altruist
                                   }


def update_contributions_stochastic_shared(player_type_matrix: np.ndarray, contributions: np.ndarray, payoff_matrix: np.ndarray,
                                 group_matrix: np.ndarray, ENDOWMENT: int, NUM_MEMBERSHIP: int, DELTA: np.ndarray, TREMBLE: list):
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
    update_contributions_shared_use = update_contributions_stochastic_shared_dict[player_type]
    contributions = update_contributions_shared_use(player, contributions, payoff_matrix, group_matrix, ENDOWMENT, NUM_MEMBERSHIP, NUM_GROUPS, DELTA, TREMBLE)
  return contributions 