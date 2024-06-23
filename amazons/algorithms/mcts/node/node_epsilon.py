import random

from amazons.algorithms.mcts.node.node import Node
from amazons.logic.amazons_logic import Board


class NodeEpsilon(Node):
    """
    Class to represent a Node for the MCTS Epsilon-Greedy algorithm

    Attributes:
        n: number of visits to the node
        Q: action value estimate

    Author: Gonzalo Rodríguez Rodríguez
    """

    def __init__(self, state: Board, action: ((int, int), (int, int), (int, int)), player: int) -> None:
        """
        Constructor for the class
        :param state: board state
        :param action: move
        :param player: int that represents the player
        """
        super().__init__(state, action, player)

        self.n = 0  # number of simulations
        self.Q = 1  # action value estimate

    def __eq__(self, other: Node) -> bool:
        """
        Method to check if another object is equal to this one
        :param other: other object
        :return: True if it is equal, False if not
        """
        return self.state == other.state

    def expand(self) -> None:
        """
        Expands the node, obtaining the child nodes of the current node
        :return: None
        """
        moves = self.state.get_legal_moves(self.player)
        # Order moves by function
        moves = self.__sort_moves(moves)
        # Take 48 best moves
        moves = moves[0:48]
        random.shuffle(moves)

        for move in moves:
            new_board = Board(self.state)
            new_board.execute_move(move, self.player)
            new_node = NodeEpsilon(new_board, move, -self.player)
            new_node.parent = self
            self.children.append(new_node)

    def __sort_moves(self, moves: list[(int, int), (int, int), (int, int)]) -> list:
        """
        Sort the moves
        :param moves: moves to be sorted
        :return: sorted moves
        """
        rating = []
        for move in moves:
            self.state.execute_move(move, self.player)
            rating.append(self.__evaluate_mobility(self.state))
            self.state.undo_move(move, self.player)

        combi = zip(moves, rating)
        combi = sorted(combi, key=lambda c: c[1], reverse=self.player == 1)
        return [item[0] for item in combi]

    def __evaluate_mobility(self, board: Board) -> int | float:
        """
        Evaluate the mobility of the board
        :param board: board to evaluate
        :return: evaluation
        """
        if board.is_win(1):
            return float('inf')
        if board.is_win(-1):
            return float('-inf')

        white_moves = board.get_legal_moves(1)
        black_moves = board.get_legal_moves(-1)
        return len(white_moves) - len(black_moves)
