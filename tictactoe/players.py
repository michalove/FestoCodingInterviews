#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Different players that can be used in sessions:
    - RandomPlayer, makes random moves
    - HumanPlayer, lets the user make moves
    - AIPlayer, picks optimal moves based on exhaustive tree search
"""

import random
from math import nan, isnan

class RandomPlayer:    
    name = 'Random Player'
    @staticmethod
    def select_move(table):
        print("Random player's turn")
        move_list = table.move_list()
        return random.randrange(len(move_list))
        
class HumanPlayer:
    name = 'Human Player'
    @staticmethod
    def select_move(table):
        input_list = table.input_list()
        while True:
            human_input = input("Human player's turn. Input move: ")
            if human_input in input_list:
                return input_list.index(human_input)
            print('Invalid input. Possible inputs: {}'.format(input_list))
        
class AIPlayer:
    name = 'AI Player'
    
    def __init__(self):
        self.cache = {}

    def cached_evaluate(self, position):
        key = self.game.representation(position)
        if key in self.cache:
            return self.cache[key]
        else:
            output = self.evaluate(position)
            self.cache[key] = output
            return output
                
    def evaluate(self, position):
        # evaluates a state
        # returns (outcome, list_of_optimal_moves)
        #
        # outcome is
        #   1 if current player wins
        #  -1 if opponent wins
        #   0 if game will be drawn
        
        # Evaluation by complete tree search
        # shortcut: if win can be forced in one move, don't look any further
        # possible improvement: if one winning move is found, stop search
        
        position_list = self.game.move_list(position)
        outcome_list = [self.game.check_winner(pos) for pos in position_list]
        
        if -1 in outcome_list:
            move_list = [i for i,v in enumerate(outcome_list) if v == -1]
            return (1, move_list)
            
        for i, (outcome, next_pos) in enumerate(zip(outcome_list, position_list)):
            if isnan(outcome):
                real_outcome, _ = self.cached_evaluate(next_pos)
                outcome_list[i] = real_outcome

        for o in [-1,0,1]:
            if o in outcome_list:
                move_list = [i for i,v in enumerate(outcome_list) if v == o]
                return (-o, move_list)
        
    def select_move(self, table):
        print("AI player's turn")
        self.game = table.game
        position = table.position
        _ , move_list = self.cached_evaluate(position)
        move = random.choice(move_list)
        return move
