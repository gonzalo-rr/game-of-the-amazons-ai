import random

from amazons.algorithms.Algorithm import Algorithm
from amazons.logic.AmazonsLogic import Board


class RandomAlgorithm(Algorithm):

    def __init__(self) -> None:
        self.name = 'Random'

    def __str__(self) -> str:
        return self.name

    def make_move(self, board: Board, player: int) -> ((int, int), (int, int), (int, int)):
        moves = board.get_legal_moves(player)
        if len(moves) != 0:
            return random.choice(moves)
        else:
            raise ValueError("no moves found for the position")
