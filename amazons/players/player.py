from abc import ABC, abstractmethod


class Player(ABC):
    """
    Interface for the players

    Author: Gonzalo Rodríguez Rodríguez
    """

    @abstractmethod
    def is_human(self) -> bool:
        """
        Returns if the player is human
        :return: True if is human, False otherwise
        """
        ...

    @abstractmethod
    def make_move(self) -> None:
        """
        Method to execute a move
        :return: None
        """
        ...
