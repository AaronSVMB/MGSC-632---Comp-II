"""_summary_
Tests various functions from the public_goods_utils.py. 
"""
from src.monte_carlo_sim import *

#==========================================================================================
# Currently Working on: Data Visualization Part 2

# Goal: access the data stored in metrics_of_interest.csv, use this to create meaningful visuals
#==========================================================================================

metrics_of_interest = pd.read_csv('metrics_of_interest.csv')