import random

from amazons.algorithms.mcts.node.node import Node
from amazons.logic.amazons_logic import Board


class NodeUCB(Node):

    def __init__(self, state, action, player):
        super().__init__(state, action, player)

        self.w = 0  # number of simulations resulting in a win
        self.s = 0  # number of simulations

    def expand(self):
        moves = self.state.get_legal_moves(self.player)
        random.shuffle(moves)
        for move in moves:
            new_board = Board(self.state)
            new_board.execute_move(move, self.player)
            new_node = NodeUCB(new_board, move, -1 * self.player)
            new_node.parent = self
            self.children.append(new_node)
