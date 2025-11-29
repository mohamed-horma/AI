# -*- coding: utf-8; mode: python -*-

# ENSICAEN
# École Nationale Supérieure d'Ingénieurs de Caen
# 6 Boulevard Maréchal Juin
# F-14050 Caen Cedex France
#
# Artificial Intelligence 2I1AE1

# @file agents.py
#
# @author Régis Clouard
# based on Mathias Broxvall's classes 

import reversistate
from reversiframe import ReversiFrame
from reversistate import ReversiState
import random
import copy
import re

class Strategy:
    """ This is a base class for implementing strategies. """

    def do_move(self, state):
        """Determines next move from list of available moves.
           Derived classes must implement this.

           player is the current player.  moves is a list of valid
           moves where each item is (x,y,boardState).
           This routine must return one of the moves from moves.  

           Note: if there is only one valid move (or no move in the case of a pass),
           this routine will not be called and the move will be made automatically.
        """
        raise Exception("Invalid Strategy class, do_move() not implemented")

class ReversiRandomAI( Strategy ):
    """ The naive version of the AI.

    This is a naive AI that just makes a random choice between
    the possible legal moves.
    """
    def __init__( self, maxply, evaluation_function ):
        pass

    def do_move( self, state ):
        moves = state.legal_moves()
        move = moves[random.randrange(0, len(moves))]
        state.move(move)

class ReversiGreedyAI( Strategy ):
    """ The greedy version of the AI.
    
    The best move is the one that flips the most disks.
    """
    def __init__( self, maxply, evaluation_function ):
        pass

    def do_move( self, state ):
        """
        Checks every move and picks the one with
        the most pieces belonging to player.
        """
        best_move = None
        best_count = -1
        for move in state.legal_moves():
            count = state.get_flips(move)
            if count > best_count:
                best_count = count
                best_move = move
        state.move(best_move)

 #  ______                               _                  __ 
 # |  ____|                             (_)                /_ |
 # | |__    __  __   ___   _ __    ___   _   ___    ___     | |
 # |  __|   \ \/ /  / _ \ | '__|  / __| | | / __|  / _ \    | |
 # | |____   >  <  |  __/ | |    | (__  | | \__ \ |  __/    | |
 # |______| /_/\_\  \___| |_|     \___| |_| |___/  \___|    |_|

class ReversiMinimaxAI( Strategy ):
    """ This is an implementation of the minimax search algorithm.

    Finds the best move in the game, looking ahead maxply moves.
    The best move is determined by an external evaluation function.
    """

    def __init__( self, maxply, evaluation_function ):
        self.maxply = maxply
        self.evaluation_function = evaluation_function
        print("Max ply =" , self.maxply)

    def do_move( self, state ):
        """
        Finds the best move in the game, looking ahead maxply moves.
        The best move is determined by an external evaluation function.

        Useful Methods:
        - state.legal_moves(): returns the list of all legal moves as pairs (x,y).
        - state.move(position): executes the specified move to the position (i.e. (x,y)).
        - state.get_player(): returns the number of the player at the specified state 
                       between 0 black and 1 white.
        - state.terminal_test(): returns true if the current state is a terminal state.
        - state_cpy=ReversiState(state): returns a deep copy the specified state.
        - self.evaluation_function.eval(state, player): returns the score (int) of the specified state
                       for the specified player. 
        """
        player = state.get_player()
        best_move = None
        best_count = float('-inf')
        for move in state.legal_moves():
            next_state = ReversiState(state)
            next_state.move(move)

            score = self.Max_value(next_state, 1, player)

            if score > best_count :
                best_count = score
                best_move = move

        state.move(best_move)
            


    def Max_value(self, state, depth , player):

        if state.terminal_test() or depth >= self.maxply:
            return self.evaluation_function.eval(state, player)
        
        v = float('-inf')
        
        for move in state.legal_moves():
            move_cpy = ReversiState(state)
            move_cpy.move(move)
            v = max(v, self.Min_value(move_cpy, depth+1, player)) 
        return v
    
###################################################################################################""""""""
    
    def Min_value(self, state, depht, player ):
            
        if state.terminal_test():
            return self.evaluation_function.eval(state, player)
        v = float('inf')

        for move in state.legal_moves():
            move_cpy = ReversiState(state)
            move_cpy.move(move)
            v = min(v, self.Max_value(move_cpy,depht+1, player))
        return v       

 
 
 #  ______                               _                  ___  
 # |  ____|                             (_)                |__ \ 
 # | |__    __  __   ___   _ __    ___   _   ___    ___       ) |
 # |  __|   \ \/ /  / _ \ | '__|  / __| | | / __|  / _ \     / / 
 # | |____   >  <  |  __/ | |    | (__  | | \__ \ |  __/    / /_ 
 # |______| /_/\_\  \___| |_|     \___| |_| |___/  \___|   |____|
  
class EvaluationStrategy:
    """ 
    This strategy pattern defines the evaluation function used to evaluate a situation.
    """

    def eval( state, max_player ):
        """  Returns the evaluation for the max_player w.r.t the state. """
        raise Exception("Invalid Strategy class, EvaluationStrategy::eval() not implemented")

class SimpleEvaluationFunction( EvaluationStrategy ):
    """ Evaluation function based only on the score. """

    def eval( self, state, max_player ):
        return state.score()[max_player] - state.score()[1 - max_player]

class MyEvaluationFunction( EvaluationStrategy ):
    """ Evaluation function.

    """

    def eval( self, state, max_player ):

        """
        @param the current state
        @param max_player correspond to max player whilst 1-max_player corresponds to adversarial.

        Useful methods:
        - state.terminal_test(): returns true if the state is terminal.
        - state.score(): returns the current score as a tuple (s1,s2)
                         where s1 is the score of the player #1 and s2 the score of the player #2.
        - state.legal_moves(): returns the list of all legal moves as pairs (x,y).        
        - state.grid[y][x]: returns the current value in the cell (x,y)
        """

        # *** YOUR CODE HERE ***"

        sum = 0 
        Weight = [ [4,-3,2,2,2,2,-3,4],
                    [-3,-4,-1,-1,-1,-1,-4,-3],
                    [2,-1,1,0,0,1,-1,2],
                    [2,-1,0,1,1,0,-1,2],
                    [2,-1,0,1,1,0,-1,2],
                    [2,-1,1,0,0,1,-1,2],
                    [-3,-4,-1,-1,-1,-1,-4,-3],
                    [4,-3,2,2,2,2,-3,4]
                    ]

        for i in range(8):
            for j in range(8):
                sum = sum + Weight[i][j] * (state.grid[i][j] == state.score()[max_player]) - Weight[i][j] * (state.grid[i][j] == state.score()[1 - max_player])
        return sum
    

 #  ______                               _                  ____  
 # |  ____|                             (_)                |___ \ 
 # | |__    __  __   ___   _ __    ___   _   ___    ___      __) |
 # |  __|   \ \/ /  / _ \ | '__|  / __| | | / __|  / _ \    |__ < 
 # | |____   >  <  |  __/ | |    | (__  | | \__ \ |  __/    ___) |
 # |______| /_/\_\  \___| |_|     \___| |_| |___/  \___|   |____/ 

class ReversiAlphaBetaAI( Strategy ):
    """
    This is an implementation of the alpha-beta search algorithm.
    """

    def __init__( self, maxply, evaluation_function ):
        self.maxply = maxply
        self.evaluation_function = evaluation_function
        print("Max ply =" , self.maxply)

    def do_move( self, state ):
        """
        Finds the best move in the game, looking ahead maxply moves.
        The best move is determined by an external evaluation function.

        Useful Methods:
        - state.legal_moves(): returns the list of all legal moves as pairs (x,y).
        - state.move(position): executes the specified move to the position (i.e. (x,y)).
        - state.get_player(): returns the number of the player at the specified state 
                       between 0 black and 1 white.
        - state.terminal_test(): returns true if the current state is a terminal state.
        - state_cpy=ReversiState(state): returns a deep copy the specified state.
        - self.evaluation_function.eval(state, player): returns the score (int) of the specified state
                       for the specified player. 
        """

        # *** YOUR CODE HERE ***"
        player = state.get_player()
        best_move = None
        best_score = float('-inf')

        alpha = float('-inf')
        beta = float('inf')

        for move in state.legal_moves():
            next_state = ReversiState(state)
            next_state.move(move)
            score = self.Min_value(next_state, 1, player, alpha, beta)
            if score > best_score:
                best_score = score
                best_move = move

        state.move(best_move)
            
###################################################################################################""""""""

    def Max_value(self, state, depth, player, alpha, beta):
        if state.terminal_test() or depth >= self.maxply:
            return self.evaluation_function.eval(state, player)

        v = float('-inf')
        for move in state.legal_moves():
            next_state = ReversiState(state)
            next_state.move(move)
            v = max(v, self.Min_value(next_state, depth+1, player, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v
    
###################################################################################################""""""""
    
    def Min_value(self, state, depth, player, alpha, beta):
        if state.terminal_test() or depth >= self.maxply:
            return self.evaluation_function.eval(state, player)

        v = float('inf')
        for move in state.legal_moves():
            next_state = ReversiState(state)
            next_state.move(move)
            v = min(v, self.Max_value(next_state, depth+1, player, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v    

 #  ______                               _                  _  _   
 # |  ____|                             (_)                | || |  
 # | |__    __  __   ___   _ __    ___   _   ___    ___    | || |_ 
 # |  __|   \ \/ /  / _ \ | '__|  / __| | | / __|  / _ \   |__   _|
 # | |____   >  <  |  __/ | |    | (__  | | \__ \ |  __/      | |  
 # |______| /_/\_\  \___| |_|     \___| |_| |___/  \___|      |_|  
    
class ReversiIterativeAlphaBetaAI( Strategy ):
    """ 
    This is an implementation of the alpha-beta search algorithm with iterative deepening.
    """

    def __init__( self, maxply, evaluation_function ):
        self.maxply = maxply
        self.evaluation_function = evaluation_function
        print("Max ply =" , self.maxply)
        self.__iterative_dictionary = {}

    def __hash(self, state):
        # TODO: Prefer the Zobrist hash?
        return re.sub('\ |\[|\]|\,', '', str(state.grid))

    def get_value(self, state, default_value ):
        key = self.__hash(state)
        if key in self.__iterative_dictionary:
            return self.__iterative_dictionary[key]
        else:
            return default_value

    def set_value( self, state, value ):
        key = self.__hash(state)
        self.__iterative_dictionary[key] = value

    def do_move( self, state ):
        """
        Keep track of children of a node in a companion data structure.

        Useful Methods:
        - self.set_value(state): Stores a value in the state.
        - self.get_value(state, default_value): Gets the value of the state.
                              If no value has been stored before, the default_value is returned.
        """
        # *** YOUR CODE HERE ***"
        player = state.get_player()
        best_move = None
        for depth in range(1, self.maxply + 1):
            best_score, move = self.alpha_beta_search(state, player, depth)
            if move is not None:
                best_move = move
        state.move(best_move)        


    def alpha_beta_search(self, state, player, depth_limit):
        """
        Returns (best_score, best_move) for the current state.
        """
        best_score = float('-inf')
        best_move = None
  
        for move in state.legal_moves():
            next_state = ReversiState(state)
            next_state.move(move)
            
            score = self.Min_value(next_state, player, depth=1, alpha=float('-inf'), beta=float('inf'), depth_limit=depth_limit)
            
            self.set_value(next_state, score)  # store value for move ordering
            
            if score > best_score:
                best_score = score
                best_move = move

        return best_score, best_move    

    def Max_value(self, state, player, depth, alpha, beta, depth_limit):
        if state.terminal_test() or depth >= depth_limit:
            return self.evaluation_function.eval(state, player)

        v = float('-inf')
        moves = state.legal_moves()

        for move in moves:
            next_state = ReversiState(state)
            next_state.move(move)
            v = max(v, self.Min_value(next_state, player, depth+1, alpha, beta, depth_limit))
            if v >= beta:
                return v
            alpha = max(alpha, v)

        return v
    
    def Min_value(self, state, player, depth, alpha, beta, depth_limit):
        if state.terminal_test() or depth >= depth_limit:
            return self.evaluation_function.eval(state, player)

        v = float('inf')
        moves = state.legal_moves()
       
        for move in moves:
            next_state = ReversiState(state)
            next_state.move(move)
            v = min(v, self.Max_value(next_state, player, depth+1, alpha, beta, depth_limit))
            if v <= alpha:
                return v
            beta = min(beta, v)

        return v
