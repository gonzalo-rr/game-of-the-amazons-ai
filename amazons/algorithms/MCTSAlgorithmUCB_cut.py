import random
import time
import math

from amazons.AmazonsLogic import Board
from amazons.algorithms.mcts_tree.NodeEpsilon import NodeEpsilon


class MCTSAlgorithm2:

    def __init__(self, max_simulations, max_time):
        self.max_simulations = max_simulations
        self.simulations = 0
        self.max_time = max_time
        self.end = 0
        self.root = None
        self.current_state = None
        self.leaf_nodes = []

        self.c = 2  # Exploration parameter

    def __str__(self):
        return "MCTS2"

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
                if self.current_state.n == 0:  # Not yet sampled
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

        self.root.children.sort(key=lambda c: c.n, reverse=True)
        return self.root.children[0].action

    # def make_move(self, board, player):
    #     if board.is_win(1) or board.is_win(-1):
    #         return None
    #
    #     new_board = Board(board)
    #
    #     self.simulations = 0
    #     self.end = time.time() + self.max_time
    #     self.root = Node(new_board, None, player)
    #
    #     self.root.expand()
    #     count = 1
    #     while time.time() <= self.end and self.simulations < self.max_simulations:
    #         # print("count", count)
    #         # Selection
    #         best_node, best_ucb = self.select(self.root)
    #         # print("BEST:", best_ucb)
    #
    #         # Expansion
    #         if best_node.s > 0:
    #             # print("expanding")
    #             best_node.expand()
    #
    #         # Simulation
    #         win = self.simulate(best_node)
    #
    #         # Backpropagation
    #         self.backpropagate(best_node, win)
    #
    #         count+=1
    #
    #     self.root.children.sort(key=lambda c: self.selection(c), reverse=True)
    #     # print(len(self.root.children))
    #     node1 = self.root.children[0]
    #     node2 = self.root.children[1]
    #     # print(node1.s)
    #     # print(node1.w)
    #     # print(node2.s)
    #     # print(node2.w)
    #     # print(self.simulations)
    #     # print(self.root.children[0].action)
    #     return self.root.children[0].action

    def select(self, node):
        best_node = None
        best_ucb = 0

        for child in node.children:
            if len(child.children) == 0:  # Not yet expanded (leaf node)
                ucb = self.ucb_score(child)
                if ucb > best_ucb:
                    best_ucb = ucb
                    best_node = child
            else:  # Already expanded (not leaf node)
                node, ucb = self.select(child)
                if ucb > best_ucb:
                    best_node = node
                    best_ucb = ucb

        return best_node, best_ucb

    def simulate(self, node):
        self.simulations += 1

        current_state = Board(node.state)
        current_player = node.player

        finished = False
        while not finished:
            if current_state.is_win(self.root.player):
                return 1
            if current_state.is_win(-self.root.player):
                return 0

            moves = current_state.get_legal_moves(current_player)

            move = random.choice(moves)  # random move
            current_state.execute_move(move, current_player)
            current_player *= -1

    def backpropagate(self, node, win):
        node.w += win
        node.n += 1

        current_node = node
        while current_node.parent is not None:
            current_node.parent.w += win
            current_node.parent.n += 1
            current_node = current_node.parent

            win = 1 - win  # Win for node means loss to parent

    def ucb_score(self, node):
        if node.n == 0:
            return float('inf')
        return (node.w / node.n) + self.c * math.sqrt(math.log(node.parent.n) / node.n)
