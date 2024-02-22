from copy import deepcopy

"""
Wants to decrease the number of moves for the opposite player
"""


def make_move(board, player):
    moves = board.get_legal_moves(player)
    min_moves = float('inf')
    best_move = None
    for move in moves:
        new_board = deepcopy(board)
        new_board.execute_move(move, player)
        n_moves = len(new_board.get_legal_moves(-player))
        if n_moves < min_moves:
            min_moves = n_moves
            best_move = move

    return best_move
