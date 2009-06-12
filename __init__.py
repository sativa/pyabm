"""
Part of Chitwan Valley agent-based model.

Sets up rc parameters so that they can be loaded and reused by other parts of 
the model.

Alex Zvoleff, azvoleff@mail.sdsu.edu
"""

import os
import sys
import warnings

import numpy as np

from rcsetup import get_rc_params

class IDError(Exception):
    pass

class IDGenerator(object):
    """A generator class for consecutive unique ID numbers. IDs can be assigned 
    externally by other code, and tracked in this class with the use_ID 
    function. The use_ID function will raise an error if called with an ID that has 
    already been assigned."""
    def __init__(self):
        # Start at -1 so the first ID will be 0
        self._last_ID = -1
        self._used_IDs = []

    def reset(self):
        self.__init__()

    def next(self):
        newID = self._last_ID + 1
        while newID in self._used_IDs:
            newID += 1
        self._last_ID = newID
        self._used_IDs.append(newID)
        return self._last_ID

    def use_ID(self, used_ID):
        # TODO: This will get very slow when dealing with large numbers of IDs. 
        # It might be better to just set _last_ID to the maximum value in 
        # _used_IDs whenever the use_ID function is called
        if used_ID in self._used_IDs:
            raise IDError("ID %s has already been used"%(used_ID))
        self._used_IDs.append(used_ID)

# this is the instance used by the model
rcParams = get_rc_params()

# Check if a RandomDate was loaded from the rcfile. If not (if 
# RandomState==None), then choose a random RandomState, and store it in 
# rcParams so that it can be written to a file at the end of model runs, and 
# saved for later reuse (for testing, etc.).
if rcParams['model.RandomState'] == None:
    # Seed the RandomState with a known random integer, and save the seed for 
    # later reuse (for testing, etc.).
    random_int = int(10**8 * np.random.random())
    rcParams['model.RandomState'] = random_int
random_state = np.random.RandomState(int(rcParams['model.RandomState']))

def boolean_choice(trueProb=.5):
    """A function that returns true or false depending on whether a randomly
    drawn float is less than trueProb"""
    if random_state.rand() < trueProb:
        return True
    else:
        return False
