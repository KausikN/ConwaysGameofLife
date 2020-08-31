'''
State Generation Methods
'''

# Imports
import numpy as np

# Main Functions
def RandomState(size, values):
    State = np.random.choice(values, size)
    return State

# Driver Code