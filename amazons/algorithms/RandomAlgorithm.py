import random


class RandomAlgorithm:

    def __init__(self):
        self.name = 'Random'

    def __str__(self):
        return self.name

    def make_move(self, board, player):
        moves = board.get_legal_moves(player)
        if len(moves) != 0:
            return random.choice(moves)
        else:
            return None
