#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script showcases the game-ai.
"""

import game_ai as ga

#%% Running a game of tictactoe human (player 1) vs. AI (player 2)

game = ga.games.Tictactoe
# game = ga.games.Nim
# game = ga.games.Crossout

p1 = ga.players.HumanPlayer()
# p1 = ga.players.AIPlayer()
# p1 = ga.players.RandomPlayer()

# p2 = ga.players.HumanPlayer()
p2 = ga.players.AIPlayer()
# p2 = ga.players.RandomPlayer()

s = ga.Session(game, p1, p2)
s.play()