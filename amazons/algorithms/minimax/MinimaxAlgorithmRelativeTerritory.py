import random
import sys
import time

from amazons.logic.AmazonsLogic import Board
from assets.utilities.UtilityFunctions import difference_relative_territory, evaluate_territory

sys.setrecursionlimit(2_000)

"""
white - max
black - min
"""


class MinimaxAlgorithmRelativeTerritory:

    def __init__(self, max_depth, max_time):
        self.__max_depth = max_depth
        self.__max_time = max_time
        self.__end = 0

    def __str__(self):
        return 'MinimaxRelTer'

    def make_move(self, board, player):
        new_board = Board(board)
        best_move = new_board.get_legal_moves(player)[0]

        self.__end = time.time() + self.__max_time
        for depth in range(1, self.__max_depth + 1):
            self.__max_depth = depth
            if time.time() >= self.__end:
                break
            _, new_best_move = self.__minimax(new_board, player, float('-inf'), float('inf'), 0)
            if new_best_move is not None:
                best_move = new_best_move

        return best_move

    def __minimax(self, board, player, alpha, beta, depth):
        if board.is_win(player) or board.is_win(-player) or depth == self.__max_depth:
            return evaluate_territory(board, difference_relative_territory, player), None
        else:
            best_score = player * float('-inf')
            best_move = None

            moves = board.get_legal_moves(player)
            if len(moves) == 1:
                best_move = moves[0]

            random.shuffle(moves)

            for move in moves:
                board.execute_move(move, player)
                score, _ = self.__minimax(board, -player, alpha, beta, depth + 1)
                board.undo_move(move, player)

                if player == 1:
                    if score > best_score:
                        best_move = move
                        best_score = score

                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
                else:
                    if score < best_score:
                        best_move = move
                        best_score = score

                    beta = min(beta, score)
                    if beta <= alpha:
                        break

            return best_score, best_move
