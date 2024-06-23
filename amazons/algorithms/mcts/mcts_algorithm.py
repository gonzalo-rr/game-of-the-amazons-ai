import math
from abc import abstractmethod

from amazons.algorithms.algorithm import Algorithm
from amazons.algorithms.mcts.node.node import Node
from amazons.algorithms.mcts.node.node_ucb import NodeUCB as NodeUCB
from amazons.algorithms.mcts.node.node_ucb_cut import NodeUCB as NodeUCBCut
from amazons.logic.amazons_logic import Board


def ucb_score(node: NodeUCB | NodeUCBCut, c: int | float) -> float:
    """
    Function to calculate the standard ucb score
    :param node: node to calculate ucb score
    :param c: exploration parameter
    :return: the calculated ucb score
    """
    if node.s == 0:
        return float('inf')
    return (node.w / node.s) + c * math.sqrt(math.log(node.parent.s) / node.s)


class MCTSAlgorithm(Algorithm):
    """
    Abstract class for the MCTS algorithm

    Attributes:
        _max_simulations: max number of simulations
        _simulations: current number of simulations
        _max_time: max time allowed to choose a move
        _end: end instant for the algorithm
        _root: root node
        _current_state: current node
        _leaf_nodes: current leaf nodes

    Author: Gonzalo Rodríguez Rodríguez
    """

    def __init__(self, max_simulations: int, max_time: int) -> None:
        """
        Constructor for the subclasses
        :param max_simulations: max number of simulations
        :param max_time: max time allowed to choose a move
        """
        self._max_simulations = max_simulations
        self._simulations = 0
        self._max_time = max_time
        self._end = 0
        self._root = None
        self._current_state = None
        self._leaf_nodes = []

    @abstractmethod
    def make_move(self, board: Board, player: int) -> ((int, int), (int, int), (int, int)):
        """
        Method to get the move chosen by the algorithm in a given position for a given player
        :param board: position of the game
        :param player: player to move
        :return: move chosen by the algorithm
        """
        if not isinstance(board, Board):
            raise TypeError("board argument must be of type Board")
        if type(player) is not int:
            raise TypeError("player must be an int")
        if player != 1 and player != -1:
            raise ValueError(f"player can only be 1 (white) or -1 (black), it cannot be {player}")

        ...

    @abstractmethod
    def _expand(self, node: Node) -> None:
        """
        Expand a node
        :param node: node to be expanded
        :return: None
        """
        ...

    @abstractmethod
    def _simulate(self, node: Node) -> int | float:
        """
        Simulate a game from the specified node
        :param node: node to simulate from
        :return: the result of the simulation
        """
        ...

    @abstractmethod
    def _back_propagate(self, node: Node, reward: int | float) -> None:
        """
        Propagate backwards the reward of a simulation
        :param node: Node to propagate backwards from
        :param reward: reward to propagate backwards
        :return: None
        """
        ...
