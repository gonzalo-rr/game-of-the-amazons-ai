import random
import time

from amazons.logic.amazons_logic import Board
from amazons.algorithms.mcts.node.node_epsilon import NodeEpsilon
from amazons.algorithms.mcts.mcts_algorithm import MCTSAlgorithm


def calculate_probability(node, nodes):
    s = 0
    for n in nodes:
        s += n.Q * (1 - (1 if node.__eq__(n) else 0))
    if s == 0:
        return 1
    return node.Q / s


class MCTSAlgorithmE(MCTSAlgorithm):

    def __init__(self, max_simulations, max_time, epsilon=0.1):
        super().__init__(max_simulations, max_time)

        self.epsilon = epsilon  # Epsilon value

    def __str__(self):
        return "MCTS_EGreedy"

    def make_move(self, board, player):
        if board.is_win(1) or board.is_win(-1):
            raise ValueError("no moves found for the position")

        new_board = Board(board)
        self._leaf_nodes = []
        self._root = NodeEpsilon(new_board, None, player)
        self._leaf_nodes.append(self._root)
        self._expand(self._root)
        self._current_state = self._root

        if len(self._root.children) == 1:
            return self._root.children[0].action

        self._simulations = 0
        self._end = time.time() + self._max_time

        while time.time() <= self._end and self._simulations < self._max_simulations:
            if len(self._current_state.children) == 0:  # Leaf node
                if self._current_state.n == 0:  # Not yet sampled
                    result = self._simulate(self._current_state)  # SIMULATION
                    self._back_propagate(self._current_state, result)  # BACKPROPAGATION
                else:  # Already sampled
                    self._expand(self._current_state)  # EXPANSION
                    if not (self._current_state.state.is_win(1) or self._current_state.state.is_win(-1)):
                        self._current_state = self._current_state.children[0]

                    result = self._simulate(self._current_state)  # SIMULATION
                    self._back_propagate(self._current_state, result)  # BACKPROPAGATION
                self._current_state = self._root  # Always return no root after back-propagation
            else:  # Not a leaf node
                self._current_state = self._select()  # SELECTION

        self._root.children.sort(key=lambda c: c.n, reverse=True)
        return self._root.children[0].action

    def _select(self):
        sorted_leaf_nodes = sorted(self._leaf_nodes, key=lambda n: n.Q, reverse=True)

        r = random.randint(0, 1)

        # With probability epsilon, select from the possible nodes using q value based probability
        if self.epsilon > r:
            probability_distribution = []
            for leaf_node in sorted_leaf_nodes[1:]:
                probability_distribution.append(calculate_probability(leaf_node, sorted_leaf_nodes))
            return random.choices(sorted_leaf_nodes[1:], probability_distribution, k=1)[0]
        # With probability 1 - epsilon, select the node with largest Q value
        return sorted_leaf_nodes[0]

    def _expand(self, node):
        self._leaf_nodes.remove(node)
        node.expand()
        self._leaf_nodes.extend(node.children)

    def _simulate(self, node):
        self._simulations += 1

        current_state = Board(node.state)
        current_player = node.player

        finished = False
        while not finished:
            if current_state.is_win(node.player):
                return 1
            if current_state.is_win(-node.player):
                return 0

            moves = current_state.get_legal_moves(current_player)

            move = random.choice(moves)  # random move
            current_state.execute_move(move, current_player)
            current_player *= -1

    def _back_propagate(self, node, win):
        node.Q += win

        current_node = node
        while current_node.parent is not None:
            current_node.parent.Q += win

            current_node = current_node.parent

            win = 1 - win  # Win for node means loss to parent
