"""
MiniMax Player
"""
from players.AbstractPlayer import AbstractPlayer
import time
from SearchAlgos import MiniMax
import random
import numpy as np

class Player(AbstractPlayer):

    def heuristic(self):
        return self.counter

    def is_goal_state(self):
        player1 = False
        player2 = False
        pos1 = np.where(self.board == 1)
        # convert pos to tuple of ints
        pos1_tuple = tuple(ax[0] for ax in pos1)
        for d in self.directions:
            i = pos1_tuple[0] + d[0]
            j = pos1_tuple[1] + d[1]

            # check legal move
            if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and (self.board[i][j] not in [-1, 1, 2]):
                player1 = True

        pos2 = np.where(self.board == 2)
        # convert pos to tuple of ints
        pos2_tuple = tuple(ax[0] for ax in pos2)
        for d in self.directions:
            i = pos2_tuple[0] + d[0]
            j = pos2_tuple[1] + d[1]

            # check legal move
            if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and (self.board[i][j] not in [-1, 1, 2]):
                player2 = True

        return not(player1) or not(player2)

    def succ(self, player_number):
        pos = np.where(self.board == player_number)
        # convert pos to tuple of ints
        all_moves = []
        pos_tuple = tuple(ax[0] for ax in pos)
        for d in self.directions:
            i = pos_tuple[0] + d[0]
            j = pos_tuple[1] + d[1]

            # check legal move
            if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and (self.board[i][j] not in [-1, 1, 2]):
                all_moves.append((d[0], d[1]))
        return all_moves

    def perform_move(self, move, player_number, to_add, players_list_score):
        pos = np.where(self.board == player_number)
        pos_tuple = tuple(ax[0] for ax in pos)
        if to_add:
            self.board[pos_tuple] = -1
            i = pos_tuple[0] + move[0]
            j = pos_tuple[1] + move[1]
            if player_number == 1:
                self.pos = (i, j)
            val = self.board[i][j]
            if val > 2:
                players_list_score[player_number - 1].append(self.board[i][j])
                # players_score[player_number - 1] += self.board[self.pos]
            self.board[i][j] = player_number
        else:
            self.board[pos_tuple] = 0
            i = pos_tuple[0] - move[0]
            j = pos_tuple[1] - move[1]
            if player_number == 1:
                self.pos = (i, j)
            val = self.board[i][j]
            if (val > 2):
                players_list_score[player_number - 1].pop()
                # players_score[player_number - 1] -= self.board[self.pos]
            self.board[i][j] = player_number

    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time,
                                penalty_score)  # keep the inheritance of the parent's (AbstractPlayer) __init__()

        self.board = None
        self.minimax = MiniMax(self.heuristic, self.succ, self.perform_move, self.is_goal_state)
        # self.player_score=(0,0)

    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, a 2D matrix of the board.
        No output is expected.
        """
        self.board = board
        self.counter = min(len(self.board), len(self.board[0]))
        pos = np.where(board == 1)
        # convert pos to tuple of ints
        self.pos = tuple(ax[0] for ax in pos)

    def make_move(self, time_limit, players_score):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        self.counter -= 1
        start = time.time()
        end = start
        limit = 1
        num_player = 1
        lst1 = []
        lst2 = []
        lst1.append(players_score[0])
        lst2.append(players_score[1])
        players_score_list = [lst1, lst2]
        while end - start < time_limit:
            lst1 = []
            lst2 = []
            lst1.append(players_score[0])
            lst2.append(players_score[1])
            players_score_list = [lst1, lst2]
            # TODO: interrumpted in minimax??, last iteration
            ret = self.minimax.search((num_player, players_score_list), limit, True)
            limit += 1
            #end = time.time()
            end+=20

        i = self.pos[0] + ret[1][0]
        j = self.pos[1] + ret[1][1]
        if (self.board[i][j] > 2):
            players_score[num_player - 1] += self.board[i][j]

        self.perform_move(ret[1], num_player, True,players_score_list)
        return ret[1]

    def set_rival_move(self, pos):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        rival_old_pos = np.where(self.board == 2)
        self.board[rival_old_pos] = -1
        # val=self.board[pos]
        # if (val > 2):
        #     self.player_score[rival_number-1]+=val
        self.board[pos] =2


    def update_fruits(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        if self.counter == 0:
            for i in range(0,len(self.board)):
                for j in range(0, len(self.board[0])):
                    if self.board[i][j] > 2:
                        self.board[i][j] = 0
