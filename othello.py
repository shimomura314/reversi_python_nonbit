"""Python de Othello
"""

from collections import deque
import copy
import numpy as np
from collections import deque
import random


class OthelloGame:
    """Play othello.
    Black disk make the first move.
    White disk make the second move.
    """
    BLACK = 1
    WHITE = -1
    BLANK = 0
    WALL = 2
    BOARD_SIZE = 8

    def __init__(self, player_color='black'):
        # Set a board
        self.board = np.zeros((OthelloGame.BOARD_SIZE + 2, OthelloGame.BOARD_SIZE + 2), dtype=int)
        self.board[ 0,] = OthelloGame.WALL
        self.board[-1,] = OthelloGame.WALL
        self.board[:, 0] = OthelloGame.WALL
        self.board[:,-1] = OthelloGame.WALL
        self.board[OthelloGame.BOARD_SIZE//2, OthelloGame.BOARD_SIZE//2] = OthelloGame.WHITE
        self.board[OthelloGame.BOARD_SIZE//2+1, OthelloGame.BOARD_SIZE//2+1] = OthelloGame.WHITE
        self.board[OthelloGame.BOARD_SIZE//2, OthelloGame.BOARD_SIZE//2+1] = OthelloGame.BLACK
        self.board[OthelloGame.BOARD_SIZE//2+1, OthelloGame.BOARD_SIZE//2] = OthelloGame.BLACK

        # Black or white
        if player_color == "black":
            self._player_color = 1
        if player_color == "white":
            self._player_color = -1
        if player_color == "random":
            self._player_color = [1,-1][random.randint(0, 1)]
        self._game_turn = 1

        # Counter
        self.result = ""
        self.count_player = 2
        self.count_CPU = 2
        self.count_blank = 60
        self.count_pass = 0

        # Logger
        self.board_log = deque([])
        self.board_log.append(copy.deepcopy(self.board))
        self.board_log_redo = deque([])

        # Mode
        self.player_auto = False
        return

    def auto_mode(self, automode:bool):
        self.player_auto = automode

    def load_strategy(self, Strategy):
        """Set strategy class."""
        self._Strategy_player = Strategy(self)
        self._Strategy_player.set_strategy("random")
        self._Strategy_CPU = Strategy(self)
        self._Strategy_CPU.set_strategy("random")

    def choice_player(self, row:int, column:int):
        """Manual mode of player's selection."""
        self.reversible_area()
        if self.is_reversible(row, column):
            self.reverse(row, column)
            self.change_turn()
            self.count_pass = 0
        return

    def choice_CPU(self):
        """Auto mode of CPU's selection."""
        return self._Strategy_CPU.selecter(self)

    def change_strategy(self, strategy, is_player=False):
        """You can select AI strategy from candidates below.

        strategy : str
            random : Put disk randomly.
            maximize : Put disk to maximize number of one's disks.
            minimize : Put disk to minimize number of one's disks.
            openness : Put disk based on openness theory.
            evenness : Put disk based on evenness theory.

        is_player : bool
            Default is True.
        """
        if is_player:
            self._Strategy_player.set_strategy(strategy)
        else:
            self._Strategy_CPU.set_strategy(strategy)
        return

    def count_disks(self):
        """Count number of black and white disks and number of blank squares."""
        self.count_player = np.count_nonzero(self.board==self._player_color)
        self.count_CPU    = np.count_nonzero(self.board==self._player_color*-1)
        self.count_blank  = np.count_nonzero(self.board==OthelloGame.BLANK)

    def change_turn(self):
        self._game_turn *= -1
        self.count_disks()
        self.reversible_area()
        return

    def reversible_area(self):
        """Select reversible area."""
        self.reversible = {}
        dx = (-1, 0, 1)
        dy = (-1, 0, 1)
        for row in range(1, OthelloGame.BOARD_SIZE+1):
            for column in range(1, OthelloGame.BOARD_SIZE+1):
                if self.board[row, column] != 0:
                    continue
                for x in dx:
                    for y in dy:
                        if self._game_turn+self.board[row+x,column+y] == 0:
                            coefficient = 2
                            while True:
                                if self.board[row+x*coefficient, column+y*coefficient] == self._game_turn:
                                    if (row, column) not in self.reversible.keys():
                                        self.reversible[(row, column)] = []
                                    for coefficient_ in range(1, coefficient):
                                        self.reversible[(row, column)].append((row+x*coefficient_, column+y*coefficient_))
                                    break
                                elif self.board[row+x*coefficient, column+y*coefficient] == self._game_turn*-1:
                                    pass
                                else:
                                    break
                                coefficient += 1
        return self.reversible

    def is_reversible(self, row:int, column:int):
        """Return wheather you can put disk on (x,y) or not."""
        return (row, column) in self.reversible.keys()

    def reverse(self, row:int, column:int):
        """Put a disk and reverse disks."""
        self.board[row, column] = self._game_turn
        for x, y in self.reversible[(row, column)]:
            self.board[x, y] *= -1
        self.board_log_redo = deque([])
        return

    def turn_playable(self):
        """Return wheather you can put disk or not."""
        return self.reversible != {}

    def process_game(self):
        self.reversible_area()
        if self._game_turn == self._player_color:
            if self.turn_playable():
                if self.player_auto:
                    self.choice_player(*self._Strategy_player.selecter(self))
                    pass
                else:
                    pass
            else:
                self.change_turn()
                self.count_pass += 1
        else:
            if self.turn_playable():
                self.reverse(*self.choice_CPU())
                self.change_turn()
                self.count_pass = 0
            else:
                self.change_turn()
                self.count_pass += 1
            self.log_turn()
        if self.game_judgement():
            return True
        else:
            return False

    def log_turn(self):
        """Append data to board_log."""
        return self.board_log.append(copy.deepcopy(self.board))

    def undo_turn(self):
        if self.board_log != deque([]):
            self.board_log_redo.append(self.board_log.pop())
            self.board = copy.deepcopy(self.board_log[-1])
        return

    def redo_turn(self):
        if self.board_log_redo != deque([]):
            self.board_log.append(self.board_log_redo.pop())
            self.board = copy.deepcopy(self.board_log[-1])
        return

    def display_board(self):
        """Show the game board."""
        return self.board[1:-1,1:-1]

    def game_judgement(self):
        """Judgement of game."""
        if self.count_pass >= 2 or self.count_blank == 0:
            if self.count_player == self.count_CPU:
                self.result = "DRAW"
            if self.count_player > self.count_CPU:
                self.result = "WIN"
            if self.count_player < self.count_CPU:
                self.result = "LOSE"
            return True
        return False