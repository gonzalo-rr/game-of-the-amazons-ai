import random


def make_move(board, player):
    moves = board.get_legal_moves(player)
    if len(moves) != 0:
        return random.choice(moves)
    else:
        return None
