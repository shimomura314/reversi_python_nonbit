"""Various strategies for othello.
"""

import random


class Maximize:
    """Put disk to maximize number of one's disks."""
    def __init__(self):
        return

    def put_disk(self, othello):
        """Put disk to maximize number of one's disks."""
        max_strategy = []
        max_merit = 0
        for candidate in othello.reversible.keys():
            if max_merit < len(othello.reversible[candidate]):
                max_strategy = [candidate]
                max_merit = len(othello.reversible[candidate])
            elif max_merit == len(othello.reversible[candidate]):
                max_strategy.append(candidate)
        return random.choice(max_strategy)