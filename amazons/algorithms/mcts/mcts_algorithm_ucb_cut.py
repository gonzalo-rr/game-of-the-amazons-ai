import random
import time

from amazons.algorithms.mcts.mcts_algorithm import MCTSAlgorithm, ucb_score
from amazons.logic.amazons_logic import Board
from amazons.algorithms.mcts.node.node_ucb_cut import NodeUCB


class MCTSAlgorithmCut(MCTSAlgorithm):
    """
    Class for the MCTS UCB cut algorithm

    Attributes:
        exploration_parameter: exploration parameter, by default 2

    Author: Gonzalo Rodríguez Rodríguez
    """

    def __init__(self, max_simulations: int, max_time: int, exploration_parameter: float = 2) -> None:
        """
        Constructor for the class
        :param max_simulations: max number of simulations
        :param max_time: max time allowed to choose a move
        :param exploration_parameter: exploration parameter 2 by default
        """
        super().__init__(max_simulations, max_time)

        self.exploration_parameter = exploration_parameter  # Exploration parameter

    def __str__(self) -> str:
        """
        Method that returns the string value of the class
        :return: name of the algorithm
        """
        return "MCTS_Cut"

    def make_move(self, board: Board, player: int) -> tuple:
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

        self._root = NodeUCB(new_board, None, player)
        self._expand(self._root)
        self._current_state = self._root

        if len(self._root.children) == 1:
            return self._root.children[0].action

        self._simulations = 0
        self._end = time.time() + self._max_time

        while time.time() <= self._end and self._simulations < self._max_simulations:
            if len(self._current_state.children) == 0:  # Leaf node
                if self._current_state.s == 0:  # Not yet sampled
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

        self._root.children.sort(key=lambda c: c.s, reverse=True)
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

    def _select(self, node: NodeUCB) -> (NodeUCB, float):
        """
        Method to select which node is going to be the current node from the descendants of a given node
        :return: None
        """
        best_node = None
        best_ucb = 0

        for child in node.children:
            if len(child.children) == 0:  # Not yet expanded (leaf node)
                ucb = ucb_score(child, self.exploration_parameter)
                if ucb > best_ucb:
                    best_ucb = ucb
                    best_node = child
            else:  # Already expanded (not leaf node)
                node, ucb = self._select(child)
                if ucb > best_ucb:
                    best_node = node
                    best_ucb = ucb

        return best_node, best_ucb

    def _expand(self, node: NodeUCB):
        """
        Method to expand a given node
        :param node: node to expand
        :return: None
        """
        node.expand()

    def _simulate(self, node: NodeUCB):
        """
        Simulate a game from the specified node
        :param node: node to simulate from
        :return: the result of the simulation
        """
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

    def _back_propagate(self, node: NodeUCB, win: int):
        """
        Propagate backwards the reward of a simulation
        :param node: Node to propagate backwards from
        :param win: result to propagate backwards
        :return: None
        """

        current_node = node
        while current_node.parent is not None:
            current_node.parent.w += win
            current_node.parent.s += 1
            current_node = current_node.parent

            win = 1 - win  # Win for node means loss to parent
