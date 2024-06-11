import random
import time
import math

from amazons.AmazonsLogic import Board
from amazons.algorithms.mcts_tree.NodeEpsilon import NodeEpsilon


def calculate_probability(node, nodes):
    s = 0
    for n in nodes:
        s += n.Q * (1 - (1 if node.__eq__(n) else 0))
    if s == 0:
        return 1
    return node.Q / s


def back_propagate(node, win):
    node.Q += win

    current_node = node
    while current_node.parent is not None:
        current_node.parent.Q += win

        current_node = current_node.parent

        win = 1 - win  # Win for node means loss to parent


class MCTSAlgorithmB:

    def __init__(self, max_simulations, max_time):
        self.max_simulations = max_simulations
        self.simulations = 0
        self.max_time = max_time
        self.end = 0
        self.root = None
        self.current_state = None
        self.leaf_nodes = []

        self.epsilon = 0.1  # Epsilon value

    def __str__(self):
        return "MCTS"

    def make_move(self, board, player):
        if board.is_win(1) or board.is_win(-1):
            return None

        new_board = Board(board)
        self.leaf_nodes = []
        self.root = NodeEpsilon(new_board, None, player)
        self.leaf_nodes.append(self.root)
        self.expand(self.root)
        self.current_state = self.root

        if len(self.root.children) == 1:
            return self.root.children[0].action

        self.simulations = 0
        self.end = time.time() + self.max_time

        while time.time() <= self.end and self.simulations < self.max_simulations:
            if len(self.current_state.children) == 0:  # Leaf node
                if self.current_state.n == 0:  # Not yet sampled
                    result = self.simulate(self.current_state)  # SIMULATION
                    back_propagate(self.current_state, result)  # BACKPROPAGATION
                else:  # Already sampled
                    self.expand(self.current_state)  # EXPANSION
                    if not (self.current_state.state.is_win(1) or self.current_state.state.is_win(-1)):
                        self.current_state = self.current_state.children[0]

                    result = self.simulate(self.current_state)  # SIMULATION
                    back_propagate(self.current_state, result)  # BACKPROPAGATION
                self.current_state = self.root  # Always return no root after back-propagation
            else:  # Not a leaf node
                self.current_state = self.select()  # SELECTION

        self.root.children.sort(key=lambda c: c.n, reverse=True)
        return self.root.children[0].action

    def select(self):
        sorted_leaf_nodes = sorted(self.leaf_nodes, key=lambda n: n.Q, reverse=True)

        r = random.randint(0, 1)

        # With probability epsilon, select from the possible nodes using q value based probability
        if self.epsilon > r:
            probability_distribution = []
            for leaf_node in sorted_leaf_nodes[1:]:
                probability_distribution.append(calculate_probability(leaf_node, sorted_leaf_nodes))
            return random.choices(sorted_leaf_nodes[1:], probability_distribution, k=1)[0]
        # With probability 1 - epsilon, select the node with largest Q value
        return sorted_leaf_nodes[0]

    def expand(self, node):
        self.leaf_nodes.remove(node)
        node.expand()
        self.leaf_nodes.extend(node.children)

    def simulate(self, node):
        self.simulations += 1

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
