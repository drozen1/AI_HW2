"""Search Algos: MiniMax, AlphaBeta
"""
from utils import ALPHA_VALUE_INIT, BETA_VALUE_INIT
#TODO: you can import more modules, if needed
import numpy as np
import utils


class SearchAlgos:
    def __init__(self, utility, succ, perform_move, goal=None):
        """The constructor for all the search algos.
        You can code these functions as you like to, 
        and use them in MiniMax and AlphaBeta algos as learned in class
        :param utility: The utility function.
        :param succ: The succesor function.
        :param perform_move: The perform move function.
        :param goal: function that check if you are in a goal state.
        """
        self.utility = utility
        self.succ = succ
        self.perform_move = perform_move
        self.goal = goal

    def search(self, state, depth, maximizing_player):
        pass



class MiniMax(SearchAlgos):

    def search(self, state, depth, maximizing_player):
        """Start the MiniMax algorithm.
        :param state: The state to start from. # = (num player of maximum,players_score)
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        if self.goal() or depth==0:
            return (self.utility(), None)
        if maximizing_player == True:
            cur_max = float('-inf')
            for move in self.succ(1):
                self.perform_move(move, 1,True,state[1])
                val= self.search(state,depth-1,False)
                if val[0]>cur_max:
                    cur_max=val[0]
                    best_move=move
                self.perform_move(move, 1, False,state[1])
            return (cur_max, best_move)
        if maximizing_player == False:
            cur_min = float('inf')
            for move in self.succ(2):
                self.perform_move(move, 2,True,state[1])
                val= self.search(state,depth-1,True)
                if val[0]<cur_min:
                    cur_min=val[0]
                    best_move=move
                self.perform_move(move, 2, False, state[1])
            return (cur_min, best_move)


class AlphaBeta(SearchAlgos):

    def search(self, state, depth, maximizing_player, alpha=ALPHA_VALUE_INIT, beta=BETA_VALUE_INIT):
        """Start the AlphaBeta algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :param alpha: alpha value
        :param: beta: beta value
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        #TODO: erase the following line and implement this function.
        raise NotImplementedError
