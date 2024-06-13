import random
import time

from amazons.AmazonsLogic import Board
from amazons.algorithms.mcts.node.NodeEpsilon import NodeEpsilon


def calculate_probability(node, nodes):
    s = 0
    for n in nodes:
        s += n.Q * (1 - (1 if node.__eq__(n) else 0))
    if s == 0:
        return 1
    return node.Q / s


class MCTSAlgorithmE:

    def __init__(self, max_simulations, max_time, epsilon=0.1):
        self.__max_simulations = max_simulations
        self.__simulations = 0
        self.__max_time = max_time
        self.__end = 0
        self.__root = None
        self.__current_state = None
        self.__leaf_nodes = []

        self.epsilon = epsilon  # Epsilon value

    def __str__(self):
        return "MCTS_EGreedy"

    def make_move(self, board, player):
        if board.is_win(1) or board.is_win(-1):
            return None

        new_board = Board(board)
        self.__leaf_nodes = []
        self.__root = NodeEpsilon(new_board, None, player)
        self.__leaf_nodes.append(self.__root)
        self.__expand(self.__root)
        self.__current_state = self.__root

        if len(self.__root.children) == 1:
            return self.__root.children[0].action

        self.__simulations = 0
        self.__end = time.time() + self.__max_time

        while time.time() <= self.__end and self.__simulations < self.__max_simulations:
            if len(self.__current_state.children) == 0:  # Leaf node
                if self.__current_state.n == 0:  # Not yet sampled
                    result = self.__simulate(self.__current_state)  # SIMULATION
                    self.__back_propagate(self.__current_state, result)  # BACKPROPAGATION
                else:  # Already sampled
                    self.__expand(self.__current_state)  # EXPANSION
                    if not (self.__current_state.state.is_win(1) or self.__current_state.state.is_win(-1)):
                        self.__current_state = self.__current_state.children[0]

                    result = self.__simulate(self.__current_state)  # SIMULATION
                    self.__back_propagate(self.__current_state, result)  # BACKPROPAGATION
                self.__current_state = self.__root  # Always return no root after back-propagation
            else:  # Not a leaf node
                self.__current_state = self.__select()  # SELECTION

        self.__root.children.sort(key=lambda c: c.n, reverse=True)
        return self.__root.children[0].action

    def __select(self):
        sorted_leaf_nodes = sorted(self.__leaf_nodes, key=lambda n: n.Q, reverse=True)

        r = random.randint(0, 1)

        # With probability epsilon, select from the possible nodes using q value based probability
        if self.epsilon > r:
            probability_distribution = []
            for leaf_node in sorted_leaf_nodes[1:]:
                probability_distribution.append(calculate_probability(leaf_node, sorted_leaf_nodes))
            return random.choices(sorted_leaf_nodes[1:], probability_distribution, k=1)[0]
        # With probability 1 - epsilon, select the node with largest Q value
        return sorted_leaf_nodes[0]

    def __expand(self, node):
        self.__leaf_nodes.remove(node)
        node.expand()
        self.__leaf_nodes.extend(node.children)

    def __simulate(self, node):
        self.__simulations += 1

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

    def __back_propagate(self, node, win):
        node.Q += win

        current_node = node
        while current_node.parent is not None:
            current_node.parent.Q += win

            current_node = current_node.parent

            win = 1 - win  # Win for node means loss to parent
