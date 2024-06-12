from copy import deepcopy, copy

from amazons.AmazonsLogic import Board


class GreedyAlgorithmTerritory:

    def __str__(self):
        return 'GreedyTer'

    def make_move(self, board, player):
        moves = board.get_legal_moves(player)
        best_score = player * float('-inf')
        best_move = moves[0]

        if len(moves) == 1:
            print("hola")
            best_move = moves[0]

        for move in moves:
            new_board = Board(board)
            new_board.execute_move(move, player)
            score = evaluate_territory(new_board)

            if player == 1:
                if score > best_score:
                    best_move = move
                    best_score = score
            else:
                if score < best_score:
                    best_move = move
                    best_score = score

        return best_move


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

# If no unmarked squares are reached, that means that all reachable squares have been reached
def all_squares_marked(new_squares, reached_squares):
    for square in new_squares:
        if square not in reached_squares:
            return False
    return True

