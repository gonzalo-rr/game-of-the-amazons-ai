from abc import ABC, abstractmethod

from amazons.logic.AmazonsLogic import Board


class Algorithm(ABC):

    @abstractmethod
    def make_move(self, board: Board, player: int) -> ((int, int), (int, int), (int, int)):
        ...
