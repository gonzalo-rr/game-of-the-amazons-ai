import sys
import time

from amazons.logic.AmazonsLogic import Board
from amazons.algorithms.minimax.history_table.HistoryTableTM import HistoryTableTM
from assets.utilities.UtilityFunctions import sort_moves, weight, calculate_queen_boards, evaluate_territory, \
    evaluate_individual_mobility, difference_territory

sys.setrecursionlimit(2_000)

"""
white - max
black - min
"""


class MinimaxAlgorithmTerritoryMobilityTable:

    def __init__(self, max_depth, max_time):
        self.__max_depth = max_depth
        self.__max_time = max_time
        self.__history_table = HistoryTableTM()
        self.__end = 0

    def __str__(self):
        return 'MinimaxTerMobTab'

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

        self.__history_table.save_table()
        return best_move

    def __minimax(self, board, player, alpha, beta, depth):
        if board.is_win(player) or board.is_win(-player) or depth == self.__max_depth:
            if board.is_win(1):
                return 9999, None
            if board.is_win(-1):
                return -9999, None

            queen_board_white, queen_board_black = calculate_queen_boards(board)
            t1 = evaluate_territory(board, difference_territory, player, queen_board_white, queen_board_black)
            m = evaluate_individual_mobility(board, queen_board_white, queen_board_black)

            return (t1 + m), None
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
                score, _ = self.__minimax(board, -player, alpha, beta, depth + 1)
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


# def calculate_king_boards(board):
#     board_white = [float('inf')] * board.n  # white territory evaluation for king moves
#     board_black = [float('inf')] * board.n  # black territory evaluation for king moves
#
#     for i in range(board.n):
#         board_white[i] = [float('inf')] * board.n
#         board_black[i] = [float('inf')] * board.n
#
#     n_moves = 1
#     reached_squares = []
#     for amazon in board.white_positions:  # White amazons
#         squares = get_free_squares_around(board, amazon)  # Get squares reached from an amazon in a king move
#         for square in squares:  # Mark those squares with the number of moves (1)
#             if square not in reached_squares:
#                 board_white[square[0]][square[1]] = n_moves
#                 reached_squares.append(square)
#
#     new_squares = copy(reached_squares)
#     all_reached = False
#     while not all_reached:
#         n_moves += 1
#         new_squares_in_iteration = []
#         for square in new_squares:
#             reachable_squares = get_free_squares_around(board, square)
#
#             for new_square in reachable_squares:
#                 if new_square not in reached_squares:
#                     board_white[new_square[0]][new_square[1]] = n_moves
#                     reached_squares.append(new_square)
#                     new_squares_in_iteration.append(new_square)
#
#         new_squares = copy(new_squares_in_iteration)
#
#         if len(new_squares) == 0:  # Check if there are no more squares to be marked
#             all_reached = True
#
#     n_moves = 1
#     reached_squares = []
#     for amazon in board.black_positions:  # Black amazons
#         squares = get_free_squares_around(board, amazon)  # Get squares reached from an amazon
#         for square in squares:  # Mark those squares with the number of moves
#             if square not in reached_squares:
#                 board_black[square[0]][square[1]] = n_moves
#                 reached_squares.append(square)
#
#     new_squares = copy(reached_squares)
#     all_reached = False
#     while not all_reached:
#         n_moves += 1
#         new_squares_in_iteration = []
#         for square in new_squares:
#             reachable_squares = get_free_squares_around(board, square)
#
#             for new_square in reachable_squares:
#                 if new_square not in reached_squares:
#                     board_black[new_square[0]][new_square[1]] = n_moves
#                     reached_squares.append(new_square)
#                     new_squares_in_iteration.append(new_square)
#
#         new_squares = copy(new_squares_in_iteration)
#
#         if len(new_squares) == 0:  # Check if there are no more squares to be marked
#             all_reached = True
#
#     return board_white, board_black
