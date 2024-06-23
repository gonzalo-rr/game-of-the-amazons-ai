import random
import time

from amazons.algorithms.minimax.minimax_algorithm import MinimaxAlgorithm, calculate_queen_boards, evaluate_territory, \
    difference_territory, evaluate_individual_mobility
from amazons.logic.amazons_logic import Board


"""
white - max
black - min
"""


class MinimaxAlgorithmTerritoryMobility(MinimaxAlgorithm):
    """
    Class for the Minimax algorithm with territory-mobility evaluation

    Attributes:
        _max_depth: max depth of the search tree
        _max_time: max time for exploring the tree

    Author: Gonzalo Rodríguez Rodríguez
    """

    def __init__(self, max_depth: int, max_time: int) -> None:
        """
        Constructor of the class
        :param max_depth: max depth of the search tree
        :param max_time: max time for exploring the tree
        """
        super().__init__(max_depth, max_time)

    def __str__(self) -> str:
        """
        Method that returns the string value of the class
        :return: name of the algorithm
        """
        return 'MinimaxTerMob'

    def make_move(self, board: Board, player: int) -> ((int, int), (int, int), (int, int)):
        """
        Method to get the move chosen by the algorithm in a given position for a given player
        :param board: position of the game
        :param player: player to move
        :return: move chosen by the algorithm
        """
        super().make_move(board, player)

        new_board = Board(board)
        moves = new_board.get_legal_moves(player)
        if len(moves) == 0:
            raise ValueError("no moves found for the position")

        best_move = moves[0]

        self._end = time.time() + self._max_time
        for depth in range(1, self._max_depth + 1):
            self._max_depth = depth
            if time.time() >= self._end:
                break
            _, new_best_move = self._minimax(new_board, player, float('-inf'), float('inf'), 0)
            if new_best_move is not None:
                best_move = new_best_move

        return best_move

    def _minimax(self, board: Board, player: int, alpha: float, beta: float, depth: int) -> \
            (float, ((int, int), (int, int), (int, int))):
        """
        Minimax recursive search algorithm
        :param board: board with the current state of the game
        :param player: player with the turn
        :param alpha: alpha pruning parameter
        :param beta: beta pruning parameter
        :param depth: depth where the minimax algorithm is executed
        :return: (evaluation, move)
        """
        if board.is_win(player) or board.is_win(-player) or depth == self._max_depth:
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




