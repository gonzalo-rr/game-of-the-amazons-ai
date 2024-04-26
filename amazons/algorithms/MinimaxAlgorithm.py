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


class MinimaxAlgorithm:

    def __init__(self, max_depth, max_time):
        self.max_depth = max_depth
        self.max_time = max_time
        self.history_table = HistoryTable()
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

        self.history_table.save_table()
        return best_move

    def minimax(self, board, player, alpha, beta, depth):
        if board.is_win(player) or board.is_win(-player) or depth == self.max_depth:
            return evaluate_territory(board), None
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


def sort_moves(moves, rating):
    combi = zip(moves, rating)
    combi = sorted(combi, key=lambda c: c[1], reverse=True)
    return [item[0] for item in combi]


def weight(depth):
    return depth * depth


def evaluate_territory1(board):
    # First: initialize the territory boards of white and black

    board_white = [0] * board.n  # white territory evaluation for queen moves
    board_black = [0] * board.n  # black territory evaluation for queen moves

    for i in range(board.n):
        board_white[i] = [0] * board.n
        board_black[i] = [0] * board.n

    # Second: calculate the number of queen and king moves to each square for black and white

    for i in range(board.n):
        for j in range(board.n):
            if board[i][j] == 0:  # Empty square
                board_white[i][j] = calculate_full_distance(board, (i, j), 1)
                board_black[i][j] = calculate_full_distance(board, (i, j), -1)

    # Third: for each empty square, calculate the difference between white and black scores

    t1 = 0  # evaluation for queen moves
    for i in range(board.n):
        for j in range(board.n):
            if board[i][j] == 0:  # Empty square
                t1 += difference(board_white[i][j], board_black[i][j])
    return t1


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


def difference(D1, D2):
    k = 1 / 5
    if D1 > 9999:
        if D2 > 9999:
            return 0
        else:
            return -10
    if D2 > 9999:
        return 10
    if D1 == D2:
        return 0
    if D1 > D2:
        return -1 * abs(D1 - D2)
    else:
        return abs(D1 - D2)


def evaluate_territory(board):
    if board.is_win(1):
        return 9999
    if board.is_win(-1):
        return -9999

    # First: initialize the territory boards of white and black

    board_white = [float('inf')] * board.n  # white territory evaluation for queen moves
    board_black = [float('inf')] * board.n  # black territory evaluation for queen moves

    for i in range(board.n):
        board_white[i] = [float('inf')] * board.n
        board_black[i] = [float('inf')] * board.n

    # Second: calculate the number of queen moves to each square for white and black

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

        # Third: for each empty square, calculate the difference between white and black scores

    t1 = 0  # evaluation for queen moves
    for i in range(board.n):
        for j in range(board.n):
            if board[i][j] == 0:  # Empty square
                # t1 += difference(board_white[i][j], board_black[i][j])
                # if board_white[i][j] > board_black[i][j]:  # Reached first by black
                #     t1 -= abs(board_white[i][j] - board_black[i][j])
                # elif board_white[i][j] < board_black[i][j]:  # Reached first by white
                #     t1 += abs(board_white[i][j] - board_black[i][j])
                t1 += difference(board_white[i][j], board_black[i][j])

    return t1


# If no unmarked squares are reached, that means that all reachable squares have been reached
def all_squares_marked(new_squares, reached_squares):
    for square in new_squares:
        if square not in reached_squares:
            return False
    return True
