"""Class of menu bar."""
import copy
import wx

import othello
from strategy import Strategy

class MenuBar(wx.MenuBar):
    """Set menu bar."""
    def __init__(self, frame):
        super().__init__()
        self._frame = frame

        menu_file = wx.Menu()
        menu_file.Append(wx.ID_SAVE, "Save")
        menu_file.Append(wx.ID_REPLACE, "Load")
        menu_file.Append(wx.ID_RESET, "Initialize")
        menu_file.AppendSeparator()
        menu_file.Append(wx.ID_EXIT, "Exit")

        menu_edit = wx.Menu()
        menu_edit.Append(wx.ID_UNDO, "Undo")
        menu_edit.Append(wx.ID_REDO, "Redo")

        menu_procedure = wx.Menu()
        self._id_color_black = menu_procedure.Append(wx.ID_ANY, "black").GetId()
        self._id_color_white = menu_procedure.Append(wx.ID_ANY, "white").GetId()
        self._id_color_random = menu_procedure.Append(wx.ID_ANY, "random").GetId()

        menu_CPU = wx.Menu()
        self._id_random = menu_CPU.AppendRadioItem(wx.ID_ANY, "random").GetId()
        self._id_maximize = menu_CPU.AppendRadioItem(wx.ID_ANY, "maximize").GetId()
        self._id_minimize = menu_CPU.AppendRadioItem(wx.ID_ANY, "minimize").GetId()
        self._id_openness = menu_CPU.AppendRadioItem(wx.ID_ANY, "openness").GetId()
        self._id_evenness = menu_CPU.AppendRadioItem(wx.ID_ANY, "evenness").GetId()
        self._id_minmax = menu_CPU.AppendRadioItem(wx.ID_ANY, "min-max").GetId()

        self.Bind(wx.EVT_MENU, self.event_manager)

        self.Append(menu_file, "File")
        self.Append(menu_edit, "Edit")
        self.Append(menu_procedure, "Procedure")
        self.Append(menu_CPU, "CPU strategy")
    
    def save_board(self):
        """Save current board."""
        self._save = copy.deepcopy(self._frame.othello._board)
        self._board_log = copy.deepcopy(self._frame.othello.board_log)
        self._board_log_redo = copy.deepcopy(self._frame.othello.board_log_redo)
        return

    def load_board(self):
        """Load saved board."""
        self._frame.othello._board = copy.deepcopy(self._save)
        self._frame.othello.board_log = copy.deepcopy(self._board_log)
        self._frame.othello.board_log_redo = copy.deepcopy(self._board_log_redo)
        return

    def initialize_game(self):
        """Initialize board."""
        game = othello.OthelloGame()
        game.load_strategy(Strategy)
        self._frame.othello = game
        return

    def close_game(self):
        """Game over."""
        return self._frame.Close()

    def undo_turn(self):
        """Return to the previous board."""
        return self._frame.othello.undo_turn()

    def redo_turn(self):
        """Redo the last select."""
        return self._frame.othello.redo_turn()

    def change_settings(self, event):
        """Change settings."""
        # Change procedure.
        if event.GetId() == self._id_color_black:
            game = othello.OthelloGame(player_color='black')
            game.load_strategy(Strategy)
            self._frame.othello = game
        if event.GetId() == self._id_color_white:
            game = othello.OthelloGame(player_color='white')
            game.load_strategy(Strategy)
            self._frame.othello = game
        if event.GetId() == self._id_color_random:
            game = othello.OthelloGame(player_color='random')
            game.load_strategy(Strategy)
            self._frame.othello = game

        # Change_strategy.  
        if event.GetId() == self._id_random:
            return self._frame.othello.change_strategy("random", False)
        if event.GetId() == self._id_maximize:
            return self._frame.othello.change_strategy("maximize", False)
        if event.GetId() == self._id_minimize:
            return self._frame.othello.change_strategy("minimize", False)
        if event.GetId() == self._id_openness:
            return self._frame.othello.change_strategy("openness_theory", False)
        if event.GetId() == self._id_evenness:
            return self._frame.othello.change_strategy("evenness_theory", False)
        if event.GetId() == self._id_minmax:
            return self._frame.othello.change_strategy("min-max", False)

    def event_manager(self, event):
        if event.GetId() == wx.ID_SAVE:
            return self.save_board()
        if event.GetId() == wx.ID_REPLACE:
            return self.load_board()
        if event.GetId() == wx.ID_RESET:
            return self.initialize_game()
        if event.GetId() == wx.ID_EXIT:
            return self.close_game()
        if event.GetId() == wx.ID_UNDO:
            return self.undo_turn()
        if event.GetId() == wx.ID_REDO:
            return self.redo_turn()
        return self.change_settings(event)