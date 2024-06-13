import sys
import time

from amazons.logic.AmazonsLogic import Board
from amazons.algorithms.minimax.history_table.HistoryTable10 import HistoryTable10
from assets.utilities.UtilityFunctions import weight, sort_moves, difference_relative_territory_10, evaluate_territory

sys.setrecursionlimit(2_000)

"""
white - max
black - min
"""


class MinimaxAlgorithmRelativeTerritory:

    def __init__(self, max_depth, max_time):
        self.max_depth = max_depth
        self.max_time = max_time
        self.history_table = HistoryTable10()
        self.end = 0

    def __str__(self):
        return 'Minimax Territory'

    def make_move(self, board, player):
        new_board = Board(board)
        best_move = new_board.get_legal_moves(player)[0]

        self.end = time.time() + self.max_time
        for depth in range(1, self.max_depth + 1):
            self.max_depth = depth
            if time.time() >= self.end:
                break
            _, new_best_move = self.minimax(new_board, player, float('-inf'), float('inf'), 0)
            if new_best_move is not None:
                best_move = new_best_move

        self.history_table.save_table()
        return best_move

    def minimax(self, board, player, alpha, beta, depth):
        if board.is_win(player) or board.is_win(-player) or depth == self.max_depth:
            return evaluate_territory(board, difference_relative_territory_10, player), None
        else:
            best_score = player * float('-inf')
            best_move = None

            moves = board.get_legal_moves(player)
            if len(moves) == 1:
                best_move = moves[0]

            rating = [0 for _ in range(len(moves))]

            for i, move in enumerate(moves):  # Rating all moves
                rating[i] = self.history_table.get_rating(move) / 4  # ??

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
                        self.history_table.update_rating(best_move, weight(self.max_depth - depth))
                        break
                else:
                    if score < best_score:
                        best_move = move
                        best_score = score

                    beta = min(beta, score)
                    if beta <= alpha:
                        self.history_table.update_rating(best_move, weight(self.max_depth - depth))
                        break

            return best_score, best_move
