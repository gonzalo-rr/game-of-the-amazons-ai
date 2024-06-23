import random
import time

from amazons.algorithms.mcts.mcts_algorithm import MCTSAlgorithm
from amazons.logic.amazons_logic import Board
from amazons.algorithms.mcts.node.node_epsilon import NodeEpsilon


def calculate_probability(node, nodes):
    """
    Function to calculate probability of selecting a node given the rest of the nodes
    :param node: node to calculate the probability
    :param nodes: rest of the nodes
    :return: probability of the node
    """
    s = 0
    for n in nodes:
        s += n.Q * (1 - (1 if node.__eq__(n) else 0))
    if s == 0:
        return 1
    return node.Q / s


def calculate_reward(delta_moves: int) -> float:
    """
    Method to calculate the reward of a finished games given the difference in available moves
    :param delta_moves: difference in available moves
    :return: reward
    """
    if delta_moves > 0:
        return 1 - 1 / (2 + (2 * delta_moves / 3))
    else:
        return 1 / (2 + (2 * -delta_moves / 3))


class MCTSAlgorithmEMod(MCTSAlgorithm):
    """
    Class for the MCTS Epsilon-Greedy modified algorithm

    Attributes:
        epsilon: epsilon probability value, by default 0.1

    Author: Gonzalo Rodríguez Rodríguez
    """

    def __init__(self, max_simulations: int, max_time: int, epsilon: float = 0.1) -> None:
        """
        Constructor for the class
        :param max_simulations: max number of simulations
        :param max_time: max time allowed to choose a move
        :param epsilon: epsilon probability value, by default 0.1
        """
        super().__init__(max_simulations, max_time)

        self.epsilon = epsilon  # Epsilon value

    def __str__(self) -> str:
        """
        Method that returns the string value of the class
        :return: name of the algorithm
        """
        return "MCTS_EGreedy_Mod"

    def make_move(self, board: Board, player: int) -> ((int, int), (int, int), (int, int)):
        """
        Method to get the move chosen by the algorithm in a given position for a given player
        :param board: position of the game
        :param player: player to move
        :return: move chosen by the algorithm
        :raises ValueError if a valid move is not found
        """
        super().make_move(board, player)

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
                    reward = self._simulate(self._current_state)  # SIMULATION
                    self._back_propagate(self._current_state, reward)  # BACKPROPAGATION
                else:  # Already sampled
                    self._expand(self._current_state)  # EXPANSION
                    if not (self._current_state.state.is_win(1) or self._current_state.state.is_win(-1)):
                        self._current_state = self._current_state.children[0]

                    reward = self._simulate(self._current_state)  # SIMULATION
                    self._back_propagate(self._current_state, reward)  # BACKPROPAGATION
                self._current_state = self._root  # Always return no root after back-propagation
            else:  # Not a leaf node
                self._current_state = self._select()  # SELECTION

        self._root.children.sort(key=lambda c: c.n, reverse=True)
        return self._root.children[0].action

    def _select(self):
        """
        Method to select which node is going to be the current node
        :return: None
        """
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

    def _expand(self, node: NodeEpsilon) -> None:
        """
        Method to expand a given node
        :param node: node to expand
        :return: None
        """
        self._leaf_nodes.remove(node)
        node.expand()
        self._leaf_nodes.extend(node.children)

    def _simulate(self, node: NodeEpsilon) -> float:
        """
        Simulate a game from the specified node
        :param node: node to simulate from
        :return: the result of the simulation
        """
        self._simulations += 1

        current_state = Board(node.state)
        current_player = node.player
        delta_moves = 0

        finished = False
        while not finished:
            if current_state.is_win(current_player):  # Win by current player
                delta_moves = current_player * len(current_state.get_legal_moves(current_player))
                break
            if current_state.is_win(-current_player):  # Win by opposite player
                delta_moves = -current_player * len(current_state.get_legal_moves(-current_player))
                break

            moves = current_state.get_legal_moves(current_player)

            move = random.choice(moves)  # random move
            current_state.execute_move(move, current_player)
            current_player *= -1

        # Obtain reward from the difference in moves in range [0, 1)
        reward = calculate_reward(delta_moves)
        return reward

    def _back_propagate(self, node: NodeEpsilon, reward: float) -> None:
        """
        Propagate backwards the reward of a simulation
        :param node: Node to propagate backwards from
        :param win: result to propagate backwards
        :return: None
        """
        node.Q += reward

        current_node = node
        while current_node.parent is not None:
            current_node.parent.Q += reward

            current_node = current_node.parent

            reward = 1 - reward  # Win for node means loss to parent


def calculate_reward_1_1(delta_moves: int) -> float:
    """
    Deprecated, old way to calculate reward
    :param delta_moves: difference in available moves
    :return: reward
    """
    reward = -1 / (1 + abs(delta_moves) / 3) + 1
    if delta_moves > 0:
        return reward
    else:
        return -reward
