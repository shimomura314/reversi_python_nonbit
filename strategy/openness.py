"""Various strategies for othello.
"""

import copy
import random

from othello import OthelloGame

class Openness:
    """Put disk based on openness theory."""
    def __init__(self):
        return

    def put_disk(self, othello):
        """Put disk based on openness theory."""
        min_strategy = []
        min_openness = float('inf')
        dx = (-1, 0, 1)
        dy = (-1, 0, 1)

        for candidate in othello.reversible.keys():
            set_openness = []
            for return_disk in othello.reversible[candidate]:
                for x in dx:
                    for y in dy:
                        if othello.board[return_disk[0]+x, return_disk[1]+y] == OthelloGame.BLANK:
                            if (return_disk[0]+x, return_disk[1]+y) not in set_openness:
                                set_openness.append((return_disk[0]+x, return_disk[1]+y))
            if len(set_openness) < min_openness:
                min_openness = len(set_openness)
                min_strategy = [candidate]
            elif len(set_openness) == min_openness:
                min_strategy.append(candidate)
        return random.choice(min_strategy)