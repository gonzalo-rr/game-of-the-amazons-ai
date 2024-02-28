import random
import sys
import time
from copy import deepcopy

from amazons.AmazonsLogic import Board

sys.setrecursionlimit(2_000)
start = 0

max_depth = 10

n_nodes = 0

"""
white - max
black - min
"""


def make_move(board, player):
    global start
    best_score = player * float('-inf')
    best_move = None
    moves = board.get_legal_moves(player)
    random.shuffle(moves)

    new_board = Board(board.board)

    start = time.time()

    for move in moves:
        alpha = float('-inf')
        beta = float('inf')

        new_board.execute_move(move, player)
        score = minimax(new_board, -player, alpha, beta, 1)
        new_board.undo_move(move, player)

        if player == 1:
            if score > best_score:
                best_move = move
                best_score = score

            alpha = max(alpha, score)
            if beta <= alpha:
                print("pruning")
                break
        else:
            if score < best_score:
                best_move = move
                best_score = score

            beta = min(beta, score)
            if beta <= alpha:
                print("pruning")
                break

    return best_move


def minimax(board, player, alpha, beta, depth):
    if depth == max_depth or time.time() >= start + 5 or board.is_win(player) or board.is_win(-player):
        return evaluate(board)
    else:
        best_score = player * float('-inf')
        moves = board.get_legal_moves(player)
        random.shuffle(moves)
        for move in moves:
            board.execute_move(move, player)
            score = minimax(board, -player, alpha, beta, depth + 1)
            board.undo_move(move, player)

            best_score = max(best_score, score) if player == 1 else min(best_score, score)

            if player == 1:
                alpha = max(alpha, score)
                if beta <= alpha:
                    print("pruning")
                    break
            else:
                beta = min(beta, score)
                if beta <= alpha:
                    print("pruning")
                    break

        return best_score

#
#
#
# def make_move(board, player):
#     global start
#
#     start = round(time.time())
#     best_score = float('-inf') if player == 1 else float('inf')
#     best_move = None
#
#     moves = board.get_legal_moves(player)
#     depth = 0
#     for move in moves:
#         new_board = deepcopy(board)
#         new_board.execute_move(move, player)
#         score = get_score(new_board, -1 * player, depth + 1)
#
#         if player == 1:
#             if score > best_score:
#                 best_move = move
#                 best_score = score
#         else:
#             if score < best_score:
#                 best_move = move
#                 best_score = score
#     return best_move
#
#
# def get_score(board, player, depth):
#     global start
#
#     if round(time.time()) - start > 10:  # Time exceeded
#         return 0
#     if board.is_win(player):
#         return player * float('inf')
#     elif depth >= max_depth:
#         return evaluate(board)
#     else:
#         best_score = player * float('inf')
#         moves = board.get_legal_moves(player)
#         for move in moves:
#             new_board = deepcopy(board)
#             new_board.execute_move(move, player)
#             score = get_score(board, -1 * player, depth + 1)
#             if player == 1:
#                 if score < best_score:
#                     best_score = score
#             else:
#                 if score > best_score:
#                     best_score = score
#         return best_score


def evaluate(board):
    if board.is_win(1):
        return float('inf')
    if board.is_win(-1):
        return float('-inf')

    white_moves = board.get_legal_moves(1)
    black_moves = board.get_legal_moves(-1)
    return len(white_moves) - len(black_moves)
