import random
import sys
import time

from amazons.AmazonsLogic import Board
from amazons.assets.UtilityFunctions import sort_moves, evaluate_mobility

sys.setrecursionlimit(2_000)

"""
white - max
black - min
"""


class MinimaxAlgorithm:

    def __init__(self, max_depth, max_time):
        self.max_depth = max_depth
        self.max_time = max_time
        self.end = 0
        self.ratings = [{} for _ in range(max_depth)]

    def make_move(self, board, player):
        new_board = Board(board.board)
        best_move = None
        self.ratings = [{} for _ in range(self.max_depth)]

        self.end = time.time() + self.max_time
        for depth in range(1, self.max_depth + 1):
            self.max_depth = depth
            if time.time() >= self.end:
                break
            _, best_move = self.minimax(new_board, player, float('-inf'), float('inf'), 0)

        return best_move

    def minimax(self, board, player, alpha, beta, depth):
        if board.is_win(player) or board.is_win(-player) or depth == self.max_depth:
            return evaluate_mobility(board), None
        else:
            best_score = player * float('-inf')
            best_move = None

            moves = board.get_legal_moves(player)
            if len(self.ratings[depth]) != 0:
                moves = sort_moves(moves, self.ratings[depth])
            else:
                random.shuffle(moves)

            for move in moves:
                board.execute_move(move, player)
                score, _ = self.minimax(board, -player, alpha, beta, depth + 1)
                self.ratings[depth][hash(move)] = score  # Give a rating to the move
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

