"""Various strategies for othello.
"""

import random

class Random:
    """Put disk randomly."""
    def __init__(self):
        return

    def put_disk(self, othello):
        """Put disk randomly."""
        return random.choice(list(othello.reversible.keys()))