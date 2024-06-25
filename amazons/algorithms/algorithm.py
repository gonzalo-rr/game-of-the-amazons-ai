from abc import ABC, abstractmethod

from amazons.logic.amazons_logic import Board


class Algorithm(ABC):
    """
    Interface for the algorithms of the system

    Author: Gonzalo Rodríguez Rodríguez
    """

    @abstractmethod
    def make_move(self, board: Board, player: int) -> tuple:
        """
        Method to get the move chosen by the algorithm in a given position for a given player
        :param board: position of the game
        :param player: player to move
        :return: move chosen by the algorithm
        """
        ...
