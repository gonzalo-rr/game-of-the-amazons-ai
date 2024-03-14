import random
import sys
import time
from copy import deepcopy

from amazons.AmazonsLogic import Board

sys.setrecursionlimit(2_000)
start = 0

max_depth = 1

n_nodes = 0

"""
white - max
black - min
"""


def make_move(board, player):
    global start

    start = time.time()
    new_board = Board(board.board)

    best_score, best_move = minimax(new_board, player, float('-inf'), float('inf'), 0)

    return best_move


def minimax(board, player, alpha, beta, depth):
    if board.is_win(player) or board.is_win(-player) or depth == max_depth:
        return evaluate_mobility(board), None
    else:
        best_score = player * float('-inf')
        best_move = None

        moves = board.get_legal_moves(player)
        random.shuffle(moves)

        for move in moves:
            board.execute_move(move, player)
            score, _ = minimax(board, -player, alpha, beta, depth + 1)
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


def evaluate_mobility(board):
    if board.is_win(1):
        return float('inf')
    if board.is_win(-1):
        return float('-inf')

    white_moves = board.get_legal_moves(1)
    black_moves = board.get_legal_moves(-1)
    return len(white_moves) - len(black_moves)

