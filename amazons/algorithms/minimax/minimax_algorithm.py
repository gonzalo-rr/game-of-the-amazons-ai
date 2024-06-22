from collections import deque
from copy import copy
from typing import Callable

from amazons.algorithms.algorithm import Algorithm
from abc import abstractmethod, ABC

from amazons.logic.amazons_logic import Board

# 2D directions in a board
directions = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]


# Move ordering for the history table
def sort_moves(moves: [(int, int, int)], rating: [float]) -> [(int, int, int)]:
    combi = zip(moves, rating)
    combi = sorted(combi, key=lambda c: c[1], reverse=True)
    return [item[0] for item in combi]


# Weight for the history table
def weight(depth: int) -> int:
    if type(depth) is not int:
        raise TypeError("depth must be an int")
    if depth < 0:
        raise ValueError("depth must be greater than or equal to 0")
    return depth * depth


# Mobility evaluation
def evaluate_mobility(board: Board) -> int | float:
    if not isinstance(board, Board):
        raise TypeError("argument must be a board")

    if board.is_win(1):
        return float('inf')
    if board.is_win(-1):
        return float('-inf')

    white_moves = board.get_legal_moves(1)
    black_moves = board.get_legal_moves(-1)
    return len(white_moves) - len(black_moves)


# Calculate minimal number of moves to reach a square for a player
def calculate_full_distance(board: Board, square: (int, int), player: int) -> int | float:
    min_distance = float('inf')
    positions = board.white_positions if player == 1 else board.black_positions
    for amazon in positions:  # for each amazon of the player
        distance = calculate_distance(board, amazon, square)
        if distance < min_distance:
            min_distance = distance
    return min_distance


# Calculate minimal number of moves between 2 squares
def calculate_distance(board: Board, start: (int, int), end: (int, int)) -> int | float:
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


# Gives value for the difference between number of moves to reach a square by white (D1) and black (D2)
# with k=5
def difference_relative_territory(d1: int, d2: int, player: int) -> int:
    # 5 if D2 is inf and D1 is not
    # -5 if D1 is inf and D2 is not
    # 0 if both are inf
    # D2 - D1 otherwise

    k = 5 * player
    if d2 > 9999 and d1 < 9999:
        return k
    if d1 > 9999 and d2 < 9999:
        return -k
    if d1 > 9999 and d2 > 9999:
        return 0
    else:
        return d2 - d1


# Gives value for the difference between number of moves to reach a square by white (D1) and black (D2)
# with k=1/5
def difference_territory(d1: int, d2: int, player: int) -> int | float:
    # 0 if both are inf
    # k if both are equal and not inf (k can be 1/5 or -1/5 depending on the turn)
    # 1 if D1 < D2
    # -1 if D1 > D2

    k = (1 / 5) * player

    if d1 > 9999 and d2 > 9999:
        return 0
    if d1 == d2 and d1 < 9999 and d2 < 9999:
        return k
    if d1 < d2:
        return 1
    if d1 > d2:
        return -1


# Deprecated, gives value for the difference between number of moves to reach a square by white (D1) and black (D2)
# with k=10
def difference_relative_territory_10(white_moves: int, black_moves: int, player: int) -> int:
    k = 10
    if white_moves > 9999:
        if black_moves > 9999:
            return 0
        else:
            return -k
    if black_moves > 9999:
        return k
    if white_moves == black_moves:
        return 0
    else:
        return black_moves - white_moves


# Returns True if all reachable squares have been reached
# If no unmarked squares are reached, that means that all reachable squares have been reached
def all_squares_marked(new_squares: [(int, int)], reached_squares: [(int, int)]) -> bool:
    for square in new_squares:
        if square not in reached_squares:
            return False
    return True


# Deprecated, previous relative territory evaluation
def evaluate_relative_territory_prev(board: Board, player: int) -> int:
    # First: initialize the territory boards of white and black

    board_white = [[]] * board.n  # white territory evaluation for queen moves
    board_black = [[]] * board.n  # black territory evaluation for queen moves

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
                t1 += difference_relative_territory(board_white[i][j], board_black[i][j], player)
    return t1


# Evaluate territory based on a difference function, which can be relative or absolute
def evaluate_territory(board: Board, difference: Callable[[int, int, int], int], player: int,
                       queen_board_white: list[list[int]] = None, queen_board_black: list[list[int]] = None) -> int:
    if board.is_win(1):
        return 9999
    if board.is_win(-1):
        return -9999

    if queen_board_white is None or queen_board_black is None:
        queen_board_white, queen_board_black = calculate_queen_boards(board)

    # For each empty square, calculate the difference between white and black scores

    t1 = 0  # evaluation for queen moves
    for i in range(board.n):
        for j in range(board.n):
            if board[i][j] == 0:  # Empty square
                t1 += difference(queen_board_white[i][j], queen_board_black[i][j], player)

    return t1


# Evaluates the individual mobility of each player and gives an estimate of which has better mobility
def evaluate_individual_mobility(board: Board,
                                 queen_board_white: list[list[int]], queen_board_black: list[list[int]]) -> int:
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


# Calculates and returns the queen-move boards of each player
# that is, for each free square, the minimal number of moves to be reached by each player
def calculate_queen_boards(board: Board) -> (list[list[int]], list[list[int]]):
    # First: initialize the territory boards of white and black

    board_white = [[]] * board.n  # white territory evaluation for queen moves
    board_black = [[]] * board.n  # black territory evaluation for queen moves

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

    return board_white, board_black


# Calculates a board where each free square contains a number that indicates the number of surrounding free squares
def calculate_king_moves(board: Board) -> list[int]:
    new_board = [[]] * board.n
    for i in range(board.n):
        new_board[i] = [0] * board.n

    for i in range(board.n):
        for j in range(board.n):
            if board[i][j] == 0:
                new_board[i][j] = len(get_free_squares_around(board, (i, j)))

    return new_board


# Returns the list of free squares around a given square
def get_free_squares_around(board: Board, square: (int, int)) -> list[(int, int)]:
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


# Calculates individual mobility of the amazons of a player
def calculate_mobility(king_moves_board: list[int], board: Board, opponent_board: list[list[int]],
                       amazon: (int, int)) -> float:
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


# Calculates the w factor (that indicates the phase of the game)
def calculate_w_factor(board: Board, queen_board_white: list[list[int]], queen_board_black: list[list[int]]) -> float:
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


# Function to weigh the alpha parameter (that indicates individual amazon mobility of a player)
# and the w factor (that indicates the phase of the game)
def f(w: float, alpha: float) -> float:
    return w * (alpha / 100)


class MinimaxAlgorithm(Algorithm, ABC):
    def __init__(self, max_depth: int, max_time: int) -> None:
        if type(max_depth) is not int:
            raise TypeError("max_depth must be int")
        if type(max_time) is not int:
            raise TypeError("max_time must be int")
        if max_depth <= 0:
            raise ValueError("max_depth must be greater than 0")
        if max_time < 0:
            raise ValueError("max_time must be greater than or equal to 0")

        self._max_depth = max_depth
        self._max_time = max_time
        self._end = 0

    @abstractmethod
    def _minimax(self, board: Board, player: int, alpha: float, beta: float, depth: int) -> \
            (float, ((int, int), (int, int), (int, int))):

        # if not isinstance(board, Board):
        #     raise TypeError("board argument must be of type Board")
        # if type(player) is not int:
        #     raise TypeError("player must be an int")
        # if player != 1 and player != -1:
        #     raise ValueError(f"player can only be 1 (white) or -1 (black), it cannot be {player}")
        # if not type(alpha) is float and not type(alpha) is int:
        #     raise TypeError("alpha must be float or int")
        # if not type(beta) is float and not type(beta) is int:
        #     raise TypeError("beta must be float or int")
        # if type(depth) is not int:
        #     raise TypeError("depth must be an int")
        # if depth < 0:
        #     raise ValueError("depth must be greater than or equal to 0")
        ...

    @abstractmethod
    def make_move(self, board: Board, player: int) -> ((int, int), (int, int), (int, int)):
        if not isinstance(board, Board):
            raise TypeError("board argument must be of type Board")
        if type(player) is not int:
            raise TypeError("player must be an int")
        if player != 1 and player != -1:
            raise ValueError(f"player can only be 1 (white) or -1 (black), it cannot be {player}")

        ...
