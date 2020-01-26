#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
package for game ai

Note: The actual AI-Code is in player.py

Contains two helper-classes to manage games and players:
    - Table consists of everything on the table during play:
        1) The game rules (one of the objects define in games.py)
        2) The current game state (= position)
    - Session consists of 
        1) The game rules (from games.py))
        2) Two players (from players.py)

The user will interact with Session.

Example call for a game of tictactoe Human again AI:
  import game_ai as ga
  game = ga.games.Tictactoe()
  player1 = ga.players.HumanPlayer()
  player2 = ga.players.AIPlayer()
  s = ga.Session(game, player1, player2)
  s.play()
"""

import players
import games
from math import nan, isnan


class Table:
    # class for tracking a game (gamestate).
    # consists of board position and rules
    
    def __init__(self, game):
        self.game = game
        self.new_game()
        
    def new_game(self):
        self.position = self.game.starting_position()

    def make_move(self, move):
        self.position = self.move_list()[move]

        outcome = self.check_winner()
        return outcome
        
    def move_list(self):
        return self.game.move_list(self.position)
    
    def input_list(self):
        return self.game.input_list(self.position)
        
    def show(self):
        self.game.show(self.position)
        
    def check_winner(self):
        return self.game.check_winner(self.position)
    
    def current_player(self):
        return self.game.current_player(self.position)
    
    def state_from_board(self, position):
        new_state = Table(self.game)
        new_state.position = position
        return new_state
    
    
class Session:
    # class for managing matches of the game.
    # needs games rules and two players
    # On calling play(), starts one match and lets the two players make their
    # moves
    
    def __init__(self, game, player1, player2):
        self.game = game
        self.players = [player1, player2]
        self.game.print_instructions()
        
    def play(self, position = None):
        print('\nStarting new game\n')
        self.table = Table(self.game)
        if not position is None:
            self.table.position = position
        
        move_count = 0
        outcome = nan
        
        while isnan(outcome):
            self.table.show()
            
            current_player = self.players[move_count % 2]
            next_move = current_player.select_move(self.table)
            outcome = self.table.make_move(next_move)      

            move_count += 1
        
        opponent = self.players[(move_count) % 2]
        if outcome == -1:
            result = '{} wins.'.format(current_player.name)
        elif outcome == 1:
            result = '{} wins.'.format(opponent.name)
        else:
            result = 'Draw'
        
        self.table.show()               
        print('\nGame Over\n{}'.format(result))
                
        return result
    