import sys
import time
from collections import deque
from copy import copy

from amazons.AmazonsLogic import Board
from amazons.assets.HistoryTable import HistoryTable

sys.setrecursionlimit(2_000)

"""
white - max
black - min
"""


class MinimaxAlgorithmMobility:

    def __init__(self, max_depth, max_time):
        self.max_depth = max_depth
        self.max_time = max_time
        self.end = 0

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

        return best_move

    def minimax(self, board, player, alpha, beta, depth):
        if board.is_win(player) or board.is_win(-player) or depth == self.max_depth:
            return evaluate_mobility(board), None
        else:
            best_score = player * float('-inf')
            best_move = None

            moves = board.get_legal_moves(player)
            if len(moves) == 1:
                best_move = moves[0]

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
                        break
                else:
                    if score < best_score:
                        best_move = move
                        best_score = score

                    beta = min(beta, score)
                    if beta <= alpha:
                        break

            return best_score, best_move


def sort_moves(moves, rating):
    combi = zip(moves, rating)
    combi = sorted(combi, key=lambda c: c[1], reverse=True)
    return [item[0] for item in combi]


def weight(depth):
    return depth * depth


def evaluate_mobility(board):
    if board.is_win(1):
        return float('inf')
    if board.is_win(-1):
        return float('-inf')

    white_moves = board.get_legal_moves(1)
    black_moves = board.get_legal_moves(-1)
    return len(white_moves) - len(black_moves)