#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Different games that can be played:
    - Tictactoe
    - Nim
    - Crossout
    
A Game object essentially encodes the rules of a game.
That is:
    - Starting position
    - Function to list all possible moves from a position
    - Function to check if a position in an end position
    
For better user interaction, it also includes:
    - Text output of instructions
    - A function to manage user input
    - A function to display the game state
"""
from math import nan

class AbstractGame:
    name = 'Abstract Game'
    
    @staticmethod
    def print_instructions():
        return
    
    @staticmethod
    def starting_position():
        pass
    
    @staticmethod
    def representation(position):
        return position
    
    @classmethod
    def move_list(cls, position):
        pass
    
    @classmethod
    def input_list(cls, position):
        pass
    
    @classmethod
    def check_winner(cls, position):
        pass
    
    @staticmethod
    def show(position):
        pass
    

class Tictactoe(AbstractGame):
    name = 'tictactoe'    
    
    @staticmethod
    def print_instructions():
        print('This is Tictactoe\n')
        print('How to input a move:')
        print('Each cell is assigned to a button on the keyboard:')
        print('')
        print(' +---+\n |qwe|\n |asd|\n |yxc|\n +---+\n')
        print('Example: lower left corner is "y"\n')
    
    @staticmethod
    def starting_position():
        return '         '
    
    @staticmethod
    def current_player(position):
        if position.count('X') > position.count('O'):
            return 'O', 'X'
        else:
            return 'X', 'O'
    
    @classmethod    
    def move_list(cls,position):
        l = []
        curr_player, _ = cls.current_player(position)
        
        for i, field in enumerate(position):
            if field == ' ':
                new_position = '{}{}{}'.format(position[0:i], curr_player, position[i+1:])
                l.append(new_position)
        return l
    
    @classmethod
    def input_list(cls, position):
        l = []
        buttons = 'qweasdyxc'
        for i,field in enumerate(position):
            if field == ' ':
                l.append(buttons[i])
        return l
    
    @staticmethod
    def punch(pos, mask):
        new_str = ''
        for i in range(len(pos)):
            if mask[i] == "1":
                new_str += pos[i]
        return new_str
    
    @classmethod
    def check_winner(cls, board):
        # returns: 'X' or 'O' if someone wins, '-' if its a draw and 
        # '' if game still goes on
        winner = ''
        player, opponent = cls.current_player(board)
        
        masks = ['111000000','000111000','000000111',
                 '100100100','010010010','001001001',
                 '100010001','001010100']
        potential_lines = [cls.punch(board, mask) for mask in masks]
        if any([line == 'XXX' for line in potential_lines]):
            winner = 'X'
        if any([line == 'OOO' for line in potential_lines]):
            winner = 'O'
        
        if winner == player:
            return 1
        if winner == opponent:
            return -1
        
        if not ' ' in board:
            return 0
        
        return nan
    
    @staticmethod
    def show(board):
        print('+---+')
        print('|{}|'.format(board[0:3]))
        print('|{}|'.format(board[3:6]))
        print('|{}|'.format(board[6:9]))
        print('+---+')
        
        
class Nim(AbstractGame):
    name = 'Nim'
    
    @staticmethod
    def print_instructions():
        print('This is the game Nim\n')
        print('RULES: The game board consists of a number of piles of objects')
        print('On your turn you may choose one of the piles and remove')
        print('as many objects from this pile as you like.')
        print('If you cannot move on your turn (because all piles are empty),\nyou lose.')
        print('You win by moving to the terminal state [0, 0, ...] so the opponent cannot move.\n')
        print('How to input a move:')
        print('The command "n,m" will remove m objects from stack n.\n')
        print('EXAMPLE: Three piles with 5 objects each = [5, 5, 5]')
        print('To remove 2 objects from the first pile, type "1,2"')
        print('The new state will be [3,5,5]\n\n')
    
    @staticmethod
    def starting_position():
        return [20,19,7]

    @staticmethod
    def representation(position):
        return str(position)[1:-1].strip('[]').replace(" ", "")  
    
    @classmethod
    def move_list(cls, position):
        l = []
        for i, height in enumerate(position):
            if height > 0:
                for new_height in range(height):
                    new_pos = position.copy()
                    new_pos[i] = new_height
                    l.append(new_pos)
        return l
    
    @classmethod
    def input_list(cls, position):
        l = []
        for i, height in enumerate(position):
              if height > 0:
                  for new_height in range(height):
                      new_input = '{},{}'.format(i+1,height-new_height)
                      l.append(new_input)
        return l
    
    @classmethod
    def check_winner(cls, position):
        if all([entry == 0 for entry in position]):
            return -1
        else:
            return nan
    
    @staticmethod
    def show(position):
        print(position)
        
class Crossout(AbstractGame):
    name = 'Cross Out'
    
    @staticmethod
    def print_instructions():
        print('This is the game CrossOut\n')
        print('The game board consists of a number of objects in a row')
        print('On your turn, you can remove either one object or two')
        print('neighboring objects.')
        print('If you cannot make a move, because all objects are gone,')
        print('you lose. Win by removing the last object from the board.')
        print('How to input a move:')
        print('The command "n" will remove object at position n')
        print('The command "n-" will remove object at position n and its right neighbor\n')
        print('EXAMPLEs:')
        print('Move "3"  will remove object 3.')
        print('Move "3-" will remove object 3 and 4.:')
        
    
    @staticmethod
    def starting_position():
        return 'OO OOO OOOOOOOO'
    
    
    @classmethod
    def move_list(cls, position):
        l = []
        for i, field in enumerate(position):
            if field == 'O':
                new_pos = '{} {}'.format(position[:i], position[i+1:])
                l.append(" ".join(new_pos.split()))
                
                if i+1 < len(position) and position[i+1] == 'O':
                    new_pos = '{}  {}'.format(position[:i], position[i+2:])
                    l.append(" ".join(new_pos.split()))
        return l
    
    @classmethod
    def input_list(cls, position):
        l = []
        for i, field in enumerate(position):
            if field == 'O':
                new_input = '{}'.format(i+1)
                l.append(new_input)
                if i+1 < len(position) and position[i+1] == 'O':
                    new_input = '{}-'.format(i+1)
                    l.append(new_input)
        return l
    
    @classmethod
    def check_winner(cls, position):
        if 'O' in position:
            return nan
        else:
            return -1
    
    @staticmethod
    def show(position):
        print('')
        #ruler = ''
        #for i,_ in enumerate(position):
        #    ruler+= str((i+1)%10)
        #    
        #print(ruler)
        outstring = '[ '
        for i,field in enumerate(position):
            if field == 'O':
                outstring += '({:2d}) '.format(i+1)
            else:
                outstring += '     '
        #print(position)      
        outstring += ' ]'
        print(outstring)
        print('')
    