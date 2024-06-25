from abc import ABC, abstractmethod

from amazons.logic.amazons_logic import Board


class Node(ABC):
    """
    Abstract class to represent a Node for the MCTS algorithms

    Attributes:
        state: board state of the node
        action: action that the node represents
        player: player for the state of the node
        parent: parent node
        children: list of child nodes

    Author: Gonzalo Rodríguez Rodríguez
    """

    def __init__(self, state: Board, action: tuple, player: int) -> None:
        """
        Constructor for the subclasses
        :param state: board state
        :param action: move
        :param player: int that represents the player
        """
        self.state = Board(state)
        self.action = action
        self.player = player
        self.parent = None
        self.children = []

    @abstractmethod
    def expand(self) -> None:
        """
        Expands the node, obtaining the child nodes of the current node
        :return: None
        """
        ...
