import random
import time

from amazons.algorithms.mcts.MCTSAlgorithm import MCTSAlgorithm, ucb_score
from amazons.logic.AmazonsLogic import Board
from amazons.algorithms.mcts.node.NodeEpsilon import NodeEpsilon


class MCTSAlgorithmCut(MCTSAlgorithm):

    def __init__(self, max_simulations, max_time, exploration_parameter=2):
        super().__init__(max_simulations, max_time)

        self.c = exploration_parameter  # Exploration parameter

    def __str__(self):
        return "MCTS_Cut"

    def make_move(self, board, player):
        if board.is_win(1) or board.is_win(-1):
            return None

        new_board = Board(board)

        self._root = NodeEpsilon(new_board, None, player)
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
                    self._current_state.expand()  # EXPANSION
                    if not (self._current_state.state.is_win(1) or self._current_state.state.is_win(-1)):
                        self._current_state = self._current_state.children[0]

                    result = self._simulate(self._current_state)  # SIMULATION
                    self._back_propagate(self._current_state, result)  # BACKPROPAGATION
                self._current_state = self._root  # Always return no root after back-propagation
            else:  # Not a leaf node
                self._current_state, _ = self._select(self._root)  # SELECTION

        self._root.children.sort(key=lambda c: c.n, reverse=True)
        return self._root.children[0].action

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

    def _select(self, node):
        best_node = None
        best_ucb = 0

        for child in node.children:
            if len(child.children) == 0:  # Not yet expanded (leaf node)
                ucb = ucb_score(child, self.c)
                if ucb > best_ucb:
                    best_ucb = ucb
                    best_node = child
            else:  # Already expanded (not leaf node)
                node, ucb = self._select(child)
                if ucb > best_ucb:
                    best_node = node
                    best_ucb = ucb

        return best_node, best_ucb

    def _expand(self, node):
        node.expand()

    def _simulate(self, node):
        self._simulations += 1

        current_state = Board(node.state)
        current_player = node.player

        finished = False
        while not finished:
            if current_state.is_win(self._root.player):
                return 1
            if current_state.is_win(-self._root.player):
                return 0

            moves = current_state.get_legal_moves(current_player)

            move = random.choice(moves)  # random move
            current_state.execute_move(move, current_player)
            current_player *= -1

    def _back_propagate(self, node, win):
        node.w += win
        node.n += 1

        current_node = node
        while current_node.parent is not None:
            current_node.parent.w += win
            current_node.parent.n += 1
            current_node = current_node.parent

            win = 1 - win  # Win for node means loss to parent
