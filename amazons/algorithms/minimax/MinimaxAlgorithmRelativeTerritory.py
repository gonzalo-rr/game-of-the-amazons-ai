import random
import sys
import time

from amazons.algorithms.minimax.MinimaxAlgorithm import MinimaxAlgorithm, evaluate_territory, \
    difference_relative_territory
from amazons.logic.AmazonsLogic import Board

sys.setrecursionlimit(2_000)

"""
white - max
black - min
"""


class MinimaxAlgorithmRelativeTerritory(MinimaxAlgorithm):

    def __init__(self, max_depth, max_time):
        super().__init__(max_depth, max_time)

    def __str__(self):
        return 'MinimaxRelTer'

    def make_move(self, board, player):
        new_board = Board(board)
        best_move = new_board.get_legal_moves(player)[0]

        self._end = time.time() + self._max_time
        for depth in range(1, self._max_depth + 1):
            self._max_depth = depth
            if time.time() >= self._end:
                break
            _, new_best_move = self.__minimax(new_board, player, float('-inf'), float('inf'), 0)
            if new_best_move is not None:
                best_move = new_best_move

        return best_move

    def _minimax(self, board, player, alpha, beta, depth):
        if board.is_win(player) or board.is_win(-player) or depth == self._max_depth:
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
                score, _ = self._minimax(board, -player, alpha, beta, depth + 1)
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
