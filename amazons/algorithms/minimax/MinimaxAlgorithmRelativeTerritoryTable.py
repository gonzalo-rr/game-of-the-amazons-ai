import sys
import time
from collections import deque
from copy import copy

from amazons.AmazonsLogic import Board
from amazons.algorithms.minimax.history_table.HistoryTableRT import HistoryTableRT
from amazons.assets.UtilityFunctions import weight, sort_moves, evaluate_territory, difference_relative_territory

sys.setrecursionlimit(2_000)

"""
white - max
black - min
"""


class MinimaxAlgorithmRelativeTerritoryTable:

    def __init__(self, max_depth, max_time):
        self.__max_depth = max_depth
        self.__max_time = max_time
        self.__history_table = HistoryTableRT()
        self.__end = 0

    def __str__(self):
        return 'MinimaxRelTerTab'

    def make_move(self, board, player):
        new_board = Board(board)
        best_move = new_board.get_legal_moves(player)[0]

        self.__end = time.time() + self.__max_time
        for depth in range(1, self.__max_depth + 1):
            self.__max_depth = depth
            if time.time() >= self.__end:
                break
            _, new_best_move = self.minimax(new_board, player, float('-inf'), float('inf'), 0)
            if new_best_move is not None:
                best_move = new_best_move

        self.__history_table.save_table()
        return best_move

    def minimax(self, board, player, alpha, beta, depth):
        if board.is_win(player) or board.is_win(-player) or depth == self.__max_depth:
            return evaluate_territory(board, difference_relative_territory, player), None
        else:
            best_score = player * float('-inf')
            best_move = None

            moves = board.get_legal_moves(player)
            if len(moves) == 1:
                best_move = moves[0]

            rating = [0 for _ in range(len(moves))]

            for i, move in enumerate(moves):  # Rating all moves
                rating[i] = self.__history_table.get_rating(move) / 4

            moves = sort_moves(moves, rating)

            for move in moves:
                board.execute_move(move, player)
                score, _ = self.minimax(board, -player, alpha, beta, depth + 1)
                board.undo_move(move, player)

                if player == 1:
                    if score > best_score:
                        best_move = move
                        best_score = score

                    alpha = max(alpha, score)
                    if beta <= alpha:
                        self.__history_table.update_rating(best_move, weight(self.__max_depth - depth))
                        break
                else:
                    if score < best_score:
                        best_move = move
                        best_score = score

                    beta = min(beta, score)
                    if beta <= alpha:
                        self.__history_table.update_rating(best_move, weight(self.__max_depth - depth))
                        break

            return best_score, best_move
