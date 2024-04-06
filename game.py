""""""

import wx

import gui
import othello
from strategy import Strategy

if __name__ == "__main__":
    game = othello.OthelloGame()
    game.load_strategy(Strategy)

    application = wx.App()
    frame = gui.MyFrame(title="Othello Game", othello=game)

    frame.Center()
    frame.Show()
    application.MainLoop()
    wx.Exit()