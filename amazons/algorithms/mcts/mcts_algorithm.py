import math
from abc import abstractmethod

from amazons.algorithms.algorithm import Algorithm


def ucb_score(node, c):
    if node.s == 0:
        return float('inf')
    return (node.w / node.s) + c * math.sqrt(math.log(node.parent.s) / node.s)


class MCTSAlgorithm(Algorithm):

    def __init__(self, max_simulations, max_time):
        self._max_simulations = max_simulations
        self._simulations = 0
        self._max_time = max_time
        self._end = 0
        self._root = None
        self._current_state = None
        self._leaf_nodes = []

    @abstractmethod
    def _expand(self, node):
        ...

    @abstractmethod
    def _simulate(self, node):
        ...

    @abstractmethod
    def _back_propagate(self, node, reward):
        ...
