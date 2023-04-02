from src.update_contribution import update_contributions_split_conditional, update_contributions_split_altruist
import numpy as np 

def test_update_contributions_split_conditional():
    player = 0
    contributions = np.zeros([16, 2])
    contributions[0,0] = 1
    result = update_contributions_split_conditional(player, contributions, payoff_matrix, group_matrix, ENDOWMENT, 
                                           NUM_MEMBERSHIP, NUM_GROUPS, DELTA)
    assert result[0,0] == 2
    assert result[1,0] == 0