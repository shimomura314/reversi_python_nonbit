"""Various strategies for othello.
"""

from collections import deque
import random

from othello import OthelloGame

class Evenness:
    """Put disk based on evenness theory."""
    def __init__(self):
        return

    def put_disk(self, othello):
        """Put disk based on evenness theory."""
        even_strategy = []
        dxy = ((1, 0), (-1, 0), (0, 1), (0, -1))

        for candidate in self._reversible.keys():
            set_adjacent = [candidate]
            que = deque([])
            que.append(candidate)
            while que:
                x, y = que.pop()
                for dx, dy in dxy:
                    if self._board[x+dx][y+dy] == OthelloGame.BLANK:
                        if (x+dx, y+dy) not in set_adjacent:
                            set_adjacent.append((x+dx, y+dy))
                            que.append((x+dx, y+dy))
                if len(set_adjacent)%2 != 0:
                    even_strategy.append(candidate)

        if even_strategy != []:
            return random.choice(even_strategy)
        else:
            return random.choice(list(othello.reversible.keys()))