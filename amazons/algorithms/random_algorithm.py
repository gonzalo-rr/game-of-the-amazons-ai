import random

from amazons.algorithms.algorithm import Algorithm
from amazons.logic.amazons_logic import Board


class RandomAlgorithm(Algorithm):
    """
    Algorithm that chooses a random action

    Author: Gonzalo Rodríguez Rodríguez
    """

    def __str__(self) -> str:
        """
        Method that returns the string value of the class
        :return: name of the algorithm
        """
        return 'Random'

    def make_move(self, board: Board, player: int) -> ((int, int), (int, int), (int, int)):
        moves = board.get_legal_moves(player)
        if len(moves) != 0:
            return random.choice(moves)
        else:
            raise ValueError("no moves found for the position")
