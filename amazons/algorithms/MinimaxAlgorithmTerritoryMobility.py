import random
import sys
import time
from collections import deque
from copy import copy

from amazons.AmazonsLogic import Board

sys.setrecursionlimit(2_000)

"""
white - max
black - min
"""


class MinimaxAlgorithmTerritoryMobility:

    def __init__(self, max_depth, max_time):
        self.max_depth = max_depth
        self.max_time = max_time
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

        return best_move

    def minimax(self, board, player, alpha, beta, depth):
        if board.is_win(player) or board.is_win(-player) or depth == self.max_depth:
            if board.is_win(1):
                return 9999, None
            if board.is_win(-1):
                return -9999, None

            queen_board_white, queen_board_black = calculate_queen_boards(board)
            t1 = evaluate_territory(board, queen_board_white, queen_board_black, player)
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


def evaluate_territory(board, board_white, board_black, player):
    # For each empty square, calculate the difference between white and black scores
    t1 = 0  # evaluation for queen moves
    for i in range(board.n):
        for j in range(board.n):
            if board[i][j] == 0:  # Empty square
                t1 += difference(board_white[i][j], board_black[i][j], player)

    return t1


def calculate_queen_boards(board):
    board_white = [float('inf')] * board.n  # white territory evaluation for queen moves
    board_black = [float('inf')] * board.n  # black territory evaluation for queen moves

    for i in range(board.n):
        board_white[i] = [float('inf')] * board.n
        board_black[i] = [float('inf')] * board.n

    n_moves = 1
    reached_squares = []
    for amazon in board.white_positions:  # White amazons
        squares = board.get_moves_position(amazon)  # Get squares reached from an amazon
        for square in squares:  # Mark those squares with the number of moves
            if square not in reached_squares:
                board_white[square[0]][square[1]] = n_moves
                reached_squares.append(square)

    new_squares = copy(reached_squares)
    all_reached = False
    while not all_reached:
        n_moves += 1
        new_squares_in_iteration = []
        for square in new_squares:
            reachable_squares = board.get_moves_position(square)

            for new_square in reachable_squares:
                if new_square not in reached_squares:
                    board_white[new_square[0]][new_square[1]] = n_moves
                    reached_squares.append(new_square)
                    new_squares_in_iteration.append(new_square)

        new_squares = copy(new_squares_in_iteration)

        if len(new_squares) == 0:  # Check if there are no more squares to be marked
            all_reached = True

    n_moves = 1
    reached_squares = []
    for amazon in board.black_positions:  # Black amazons
        squares = board.get_moves_position(amazon)  # Get squares reached from an amazon
        for square in squares:  # Mark those squares with the number of moves
            if square not in reached_squares:
                board_black[square[0]][square[1]] = n_moves
                reached_squares.append(square)

    new_squares = copy(reached_squares)
    all_reached = False
    while not all_reached:
        n_moves += 1
        new_squares_in_iteration = []
        for square in new_squares:
            reachable_squares = board.get_moves_position(square)

            for new_square in reachable_squares:
                if new_square not in reached_squares:
                    board_black[new_square[0]][new_square[1]] = n_moves
                    reached_squares.append(new_square)
                    new_squares_in_iteration.append(new_square)

        new_squares = copy(new_squares_in_iteration)

        if len(new_squares) == 0:  # Check if there are no more squares to be marked
            all_reached = True

    return board_white, board_black


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


directions = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]


def weight(depth):
    return depth * depth


def calculate_full_distance(board, square, player):
    min_distance = float('inf')
    positions = board.white_positions if player == 1 else board.black_positions
    for amazon in positions:  # for each amazon of the player
        distance = calculate_distance(board, amazon, square)
        if distance < min_distance:
            min_distance = distance
    return min_distance


def calculate_distance(board, start, end):
    if start == end:
        return 0
    visited = set()
    queue = deque([(start, 0)])

    while queue:
        square, distance = queue.popleft()
        if square == end:
            return distance
        visited.add(square)
        moves = board.get_moves_position(square)
        for move in moves:
            if move not in visited:
                queue.append((move, distance + 1))
                visited.add(move)
    return float('inf')


def difference(D1, D2, player):
    # 0 if both are inf
    # k if both are equal and not inf (k can be 1/5 or -1/5 depending on the turn)
    # 1 if D1 < D2
    # -1 if D1 > D2

    k = (1 / 5) * player

    if D1 > 9999 and D2 > 9999:
        return 0
    if D1 == D2 and D1 < 9999 and D2 < 9999:
        return k
    if D1 < D2:
        return 1
    if D1 > D2:
        return -1


# If no unmarked squares are reached, that means that all reachable squares have been reached
def all_squares_marked(new_squares, reached_squares):
    for square in new_squares:
        if square not in reached_squares:
            return False
    return True


def evaluate_individual_mobility(board, queen_board_white, queen_board_black):
    # Factor that determines the phase of the game
    w = calculate_w_factor(board, queen_board_white, queen_board_black)

    king_moves_board = calculate_king_moves(board)

    # Player 1 (white)
    result_white = 0
    for amazon in board.white_positions:
        alpha_white = calculate_mobility(king_moves_board, board, queen_board_white, amazon)
        result_white += f(w, alpha_white)

    # Player 2 (black)
    result_black = 0
    for amazon in board.black_positions:
        alpha_black = calculate_mobility(king_moves_board, board, queen_board_black, amazon)
        result_black += f(w, alpha_black)

    return result_white - result_black


def calculate_king_moves(board):
    new_board = [0] * board.n
    for i in range(board.n):
        new_board[i] = [0] * board.n

    for i in range(board.n):
        for j in range(board.n):
            if board[i][j] == 0:
                new_board[i][j] = len(get_free_squares_around(board, (i, j)))

    return new_board


def get_free_squares_around(board, square):
    free_squares = []
    for direction in directions:
        x = square[0] + direction[0]
        y = square[1] + direction[1]

        if board.n > x >= 0 and board.n > y >= 0 and board.board[x][y] == 0:
            if board[x][y] == 0:
                free_squares.append((x, y))
            x += direction[0]
            y += direction[1]

    return free_squares


def calculate_mobility(king_moves_board, board, opponent_board, amazon):
    alpha = 0

    for direction in directions:
        x = amazon[0] + direction[0]
        y = amazon[1] + direction[1]

        dist = 0
        while board.n > x >= 0 and board.n > y >= 0 and board.board[x][y] == 0:
            if board[x][y] == 0 and opponent_board[x][y] < 9999:
                alpha += (king_moves_board[x][y]) / (2 ** dist)
            x += direction[0]
            y += direction[1]

            dist += 1

    return alpha


def calculate_w_factor(board, queen_board_white, queen_board_black):
    # For each empty square
    w = 0
    for i in range(board.n):
        for j in range(board.n):
            if board[i][j] == 0:  # Empty square
                dist_white = queen_board_white[i][j]
                dist_black = queen_board_black[i][j]
                if dist_white < 9999 and dist_black < 9999:
                    w += 1 / (2 ** abs(dist_white - dist_black))

    return w


def f(w, alpha):
    return w * (alpha / 100)

