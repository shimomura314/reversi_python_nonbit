"""Various strategies for othello.
"""

from collections import deque
import copy
import numpy as np
import pickle
import random

from othello import OthelloGame

class Minmax:
    """Find a better move by min-max method.
    """
    __all__ = ["put_disk"]

    def __init__(self):
        try:
            with open('./non_bit_othello/strategy/minmax_hash.pkl', 'rb') as file_:
                self._hash_log = pickle.load(file_)
        except:
            self._hash_log = {}
        for color in ["1", "-1"]:
            for turn in ['1', '-1']:
                for depth in ["0", "1", "2", "3", "4", "5"]:
                    key = "".join([color, turn, depth])
                    if key not in self._hash_log.keys():
                        self._hash_log[key] = {}

        self._EVALUATION_FIRST = np.array([
            [ 30,-12,  0, -1, -1,  0,-12, 30],
            [-12,-15, -3, -3, -3, -3,-15,-12],
            [  0, -3,  0, -1, -1,  0, -3,  0],
            [ -1, -3, -1, -1, -1, -1, -3, -1],
            [ -1, -3, -1, -1, -1, -1, -3, -1],
            [  0, -3,  0, -1, -1,  0, -3,  0],
            [-12,-15, -3, -3, -3, -3,-15,-12],
            [ 30,-12,  0, -1, -1,  0,-12, 30],
        ])
        self._EVALUATION_MIDDLE = np.array([
            [120,-20, 20,  5,  5, 20,-20,120],
            [-20,-40, -5, -5, -5, -5,-40,-20],
            [ 20, -5, 15,  3,  3, 15, -5, 20],
            [  5, -5,  3,  3,  3,  3, -5,  5],
            [  5, -5,  3,  3,  3,  3, -5,  5],
            [ 20, -5, 15,  3,  3, 15, -5, 20],
            [-20,-40, -5, -5, -5, -5,-40,-20],
            [120,-20, 20,  5,  5, 20,-20,120],
        ])
        return

    def hashing(self, board):
        hashed_board = [None for _ in range(len(board))]
        for row in range(len(board)):
            hashed_board[row] = "".join(map(str, board[row]))
        return "".join(hashed_board)

    def count_disks(self, board:list, player_color:int):
        """Count number of black and white disks and number of blank squares.
        Returns
        ----------
        count_player, count_CPU, count_blank = int
        """
        return np.count_nonzero(board==player_color), np.count_nonzero(board==player_color*-1), np.count_nonzero(board==OthelloGame.BLANK)

    def reversible_area(self, board:list, game_turn:int):
        """Select reversible area."""
        reversible = {}
        dx = (-1, 0, 1)
        dy = (-1, 0, 1)
        for row in range(1, OthelloGame.BOARD_SIZE+1):
            for column in range(1, OthelloGame.BOARD_SIZE+1):
                if board[row, column] != 0:
                    continue
                for x in dx:
                    for y in dy:
                        if game_turn+board[row+x,column+y] == 0:
                            coefficient = 2
                            while True:
                                if board[row+x*coefficient, column+y*coefficient] == game_turn:
                                    if (row, column) not in reversible.keys():
                                        reversible[(row, column)] = []
                                    for coefficient_ in range(1, coefficient):
                                        reversible[(row, column)].append((row+x*coefficient_, column+y*coefficient_))
                                    break
                                elif board[row+x*coefficient, column+y*coefficient] == game_turn*-1:
                                    pass
                                else:
                                    break
                                coefficient += 1
        return reversible

    def is_reversible(self, reversible:dict, row:int, column:int):
        """Return wheather you can put disk on (x,y) or not."""
        return (row, column) in reversible.keys()

    def reverse(self, board:list, reversible:dict, row:int, column:int, game_turn:int):
        """Put a disk and reverse disks."""
        new_board = copy.deepcopy(board)
        new_board[row, column] = game_turn
        for x, y in reversible[(row, column)]:
            new_board[x, y] *= -1
        return new_board

    def turn_playable(self, reversible:dict):
        """Return wheather you can put disk or not."""
        return reversible != {}

    def process_game(self):
        self.reversible_area()
        if self._game_turn == self._player_color:
            if self.turn_playable():
                if self.user_auto:
                    pass
                else:
                    pass
            else:
                self.change_turn()
                self._count_pass += 1
        else:
            if self.turn_playable():
                self.reverse(*self.choice_CPU())
                self.change_turn()
                self._count_pass = 0
            else:
                self.change_turn()
                self._count_pass += 1
            self.log_turn()
        if self.game_judgement():
            return True
        else:
            return False

    def game_judgement(self, count_player:int, count_CPU:int, count_blank:int):
        """Judgement of game."""
        if self._count_pass >= 2 or count_blank == 0:
            if count_player == count_CPU:
                self._result = "DRAW"
            if count_player > count_CPU:
                self._result = "WIN"
            if count_player < count_CPU:
                self._result = "LOSE"
            return True
        return False

    def touch_border(self, board:list):
        if np.count_nonzero(board[[1, -2], 1:-1] != 0):
            return True
        if np.count_nonzero(board[1:-1, [1, -2]] != 0):
            return True
        return False

    def evaluate_value(self, board:list, game_turn:int):
        if not self.touch_border(board):
            return np.sum(self._EVALUATION_FIRST*board[1:-1,1:-1])*game_turn
        else:
            return np.sum(self._EVALUATION_MIDDLE*board[1:-1,1:-1])*game_turn

    def check_hash_table(self, hashed_board, key):
        if hashed_board in self._hash_log[key].keys():
            return True, self._hash_log[key][hashed_board]
        return False, None

    def save_hash_table(self, hashed_board, key, evaluation, selected):
        self._hash_log[key][hashed_board] = (evaluation, selected)
        return

    def update_file(self):
        with open('./non_bit_othello/strategy/minmax_hash.pkl', 'wb') as file_:
            pickle.dump(self._hash_log, file_)
        return

    def min_max(self, board, game_turn, depth, pre_evaluation=-1*float('inf')):
        # If the board is known, return value.
        hashed_board = self.hashing(board)
        hash_key = "".join([str(self._player_color) + str(game_turn) + str(depth)])
        is_exist, saved = self.check_hash_table(hashed_board, hash_key)
        if is_exist:
            evaluation, selected = saved
            return evaluation, selected

        # Calculate evaluation.
        evaluation = self.evaluate_value(board, self._player_color)
        if depth == 0:
            self.save_hash_table(hashed_board, hash_key, evaluation, (1,1))
            return evaluation, (1,1)

        if game_turn == self._player_color:
            max_evaluation = -1*float('inf')
        else:
            min_evaluation = float('inf')

        reversible = self.reversible_area(board, game_turn)
        if self.turn_playable(reversible):
            for (row, column) in reversible.keys():
                new_board = self.reverse(board, reversible, row, column, game_turn)
                if self.game_judgement(*self.count_disks(new_board, game_turn)):
                    if self._result == 'WIN':
                        next_evaluation = 10**10
                    elif self._result == 'LOSE':
                        next_evaluation = -10**10
                    else:
                        next_evaluation = 0
                else:
                    if game_turn == self._player_color:
                        next_evaluation = self.min_max(new_board, game_turn*-1, depth-1, max_evaluation)[0]
                    else:
                        next_evaluation = self.min_max(new_board, game_turn*-1, depth-1, min_evaluation)[0]

                # alpha-bata method(pruning)
                if game_turn == self._player_color:
                    if next_evaluation < pre_evaluation:
                        return next_evaluation, (row, column)
                else:
                    if pre_evaluation < next_evaluation:
                        return next_evaluation, (row, column)
                    pass

                if game_turn == self._player_color:
                    if max_evaluation < next_evaluation:
                        max_evaluation = next_evaluation
                        selected = (row, column)
                else:
                    if next_evaluation < min_evaluation:
                        min_evaluation = next_evaluation
                        selected = (row, column)
        else:
            return self.min_max(board, game_turn*-1, depth-1)
        if game_turn == self._player_color:
            self.save_hash_table(hashed_board, hash_key, max_evaluation, selected)
            return max_evaluation, selected
        else:
            self.save_hash_table(hashed_board, hash_key, min_evaluation, selected)
            return min_evaluation, selected

    def put_disk(self, othello, depth=5):
        board = copy.deepcopy(othello.board)
        game_turn = othello._game_turn
        self._player_color = othello._game_turn
        self._count_pass = 0
        return self.min_max(board, game_turn, depth)[1]