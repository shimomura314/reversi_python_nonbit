"""Various strategies for othello.
"""

from collections import deque
import copy
import numpy as np
import random

import othello
from othello import OthelloGame

from .evenness import Evenness
from .maximize import Maximize
from .minimize import Minimize
from .minmax import Minmax
from .openness import Openness
from .random import Random

class Strategy(OthelloGame):
    """You can select AI strategy from candidates below.

    Strategies
    ----------
    random : Put disk randomly.
    maximize : Put disk to maximize number of one's disks.
    minimize : Put disk to minimize number of one's disks.
    openness : Put disk based on openness theory.
    evenness : Put disk based on evenness theory.
    """
    
    def __init__(self, othello):
        self._othello = othello
        self._player_color = othello._player_color
        self._strategy = Random()
        return

    def set_strategy(self, strategy:str):
        if strategy == "random":
            self._strategy = Random()
        if strategy == "maximize":
            self._strategy = Maximize()
        if strategy == "minimize":
            self._strategy = Minimize()
        if strategy == "openness_theory":
            self._strategy = Openness()
        if strategy == "evenness_theory":
            self._strategy = Evenness()
        if strategy == "min-max":
            self._strategy = Minmax()
        return

    def selecter(self, othello):
        return self._strategy.put_disk(othello)