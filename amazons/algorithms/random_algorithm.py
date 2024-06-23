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
        """
        Method to get the move chosen by the algorithm in a given position for a given player
        :param board: position of the game
        :param player: player to move
        :return: move chosen randomly
        """
        moves = board.get_legal_moves(player)
        if len(moves) != 0:
            return random.choice(moves)
        else:
            raise ValueError("no moves found for the position")
