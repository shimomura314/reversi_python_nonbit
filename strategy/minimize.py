"""Various strategies for othello.
"""

import random


class Minimize:
    """Put disk to minimize number of one's disks."""
    def __init__(self):
        return

    def put_disk(self, othello):
        """Put disk to minimize number of one's disks."""
        min_strategy = []
        min_merit = float('inf')
        for candidate in othello.reversible.keys():
            if min_merit > len(othello.reversible[candidate]):
                min_strategy = [candidate]
                min_merit = len(othello.reversible[candidate])
            elif min_merit == len(othello.reversible[candidate]):
                min_strategy.append(candidate)
        return random.choice(min_strategy)