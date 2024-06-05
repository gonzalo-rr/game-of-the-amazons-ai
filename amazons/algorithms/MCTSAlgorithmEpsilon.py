import random
import time

from amazons.AmazonsLogic import Board
from amazons.algorithms.mcts_tree.NodeEpsilon import NodeEpsilon


class MCTSAlgorithmEpsilon:

    def __init__(self, max_simulations, max_time):
        self.max_simulations = max_simulations
        self.simulations = 0
        self.max_time = max_time
        self.end = 0
        self.root = None
        self.current_state = None

        self.epsilon = 0.5

    def __str__(self):
        return "MCTS"

    def make_move(self, board, player):
        if board.is_win(1) or board.is_win(-1):
            return None

        new_board = Board(board)

        self.root = NodeEpsilon(new_board, None, player)
        self.root.expand()
        self.current_state = self.root

        if len(self.root.children) == 1:
            return self.root.children[0].action

        self.simulations = 0
        self.end = time.time() + self.max_time

        while time.time() <= self.end and self.simulations < self.max_simulations:
            if len(self.current_state.children) == 0:  # Leaf node
                if self.current_state.s == 0:  # Not yet sampled
                    result = self.simulate(self.current_state)  # SIMULATION
                    self.backpropagate(self.current_state, result)  # BACKPROPAGATION
                else:  # Already sampled
                    self.current_state.expand()  # EXPANSION
                    if not (self.current_state.state.is_win(1) or self.current_state.state.is_win(-1)):
                        self.current_state = self.current_state.children[0]

                    result = self.simulate(self.current_state)  # SIMULATION
                    self.backpropagate(self.current_state, result)  # BACKPROPAGATION
                self.current_state = self.root  # Always return no root after back-propagation
            else:  # Not a leaf node
                self.current_state, _ = self.select(self.root)  # SELECTION

        self.root.children.sort(key=lambda c: c.s, reverse=True)
        return self.root.children[0].action

    def select(self, node):
        # Traverse the tree to get Q of all nodes
        q_dict = ()
        for child in node.children:
            get_q(child)
        # Order nodes by Q
        # With probability epsilon, select node with highest Q
        # If highest Q node is not selected, select node by probability p


        best_child = None
        best_child_ucb = 0

        for child in node.children:
            if len(child.children) == 0:  # Not yet expanded (leaf node)
                ucb = child.ucb_score()
                if ucb > best_child_ucb:
                    best_child_ucb = ucb
                    best_child = child
            else:  # Already expanded (not leaf node)
                node, ucb = self.select(child)
                if ucb > best_child_ucb:
                    best_child = node
                    best_child_ucb = ucb

        # print(best_ucb)
        return best_child, best_child_ucb

    def simulate(self, node):
        # Simulation based on the probability of moves using formula
        self.simulations += 1

        current_state = Board(node.state)
        current_player = node.player

        finished = False
        while not finished:
            # print(self.root.player)
            if current_state.is_win(self.root.player):
                return 1
            if current_state.is_win(-self.root.player):
                return 0

            moves = current_state.get_legal_moves(current_player)

            move = random.choice(moves)  # random move
            current_state.execute_move(move, current_player)
            current_player *= -1


    def backpropagate(self, node, win):
        # Back-propagate Q based on the formula

        node.w += win
        node.s += 1

        current_node = node
        while current_node.parent is not None:
            current_node.parent.w += win
            current_node.parent.s += 1
            current_node = current_node.parent
