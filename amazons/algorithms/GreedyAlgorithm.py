from copy import deepcopy

"""
Wants to decrease the number of moves for the opposite player
"""


def make_move(board, player):
    moves = board.get_legal_moves(player)
    best_score = best_score = player * float('-inf')
    best_move = None
    for move in moves:
        new_board = deepcopy(board)
        new_board.execute_move(move, player)
        score = evaluate(new_board)

        if player == 1:
            if score > best_score:
                best_move = move
                best_score = score
        else:
            if score < best_score:
                best_move = move
                best_score = score

    return best_move


def evaluate(board):
    if board.is_win(1):
        return float('inf')
    if board.is_win(-1):
        return float('-inf')

    white_moves = board.get_legal_moves(1)
    black_moves = board.get_legal_moves(-1)
    return len(white_moves) - len(black_moves)
