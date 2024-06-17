from abc import ABC, abstractmethod

from amazons.logic.AmazonsLogic import Board


class Node(ABC):
    def __init__(self, state, action, player):
        self.state = Board(state)
        self.action = action
        self.player = player
        self.parent = None
        self.children = []

    @abstractmethod
    def expand(self):
        ...
