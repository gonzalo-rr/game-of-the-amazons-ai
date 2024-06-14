from abc import ABC, abstractmethod


class Algorithm(ABC):

    @abstractmethod
    def make_move(self, board, player):
        ...
