import random

from amazons.AmazonsLogic import Board


class Node:

    def __init__(self, state, action, player):
        self.state = Board(state)
        self.action = action
        self.player = player
        self.parent = None
        self.children = []
        self.w = 0  # number of simulations resulting in a win
        self.s = 0  # number of simulations
        # self.c = 2  # exploration parameter

    def expand(self):
        moves = self.state.get_legal_moves(self.player)
        random.shuffle(moves)
        for move in moves:
            new_board = Board(self.state)
            new_board.execute_move(move, self.player)
            new_node = Node(new_board, move, -1 * self.player)
            new_node.parent = self
            self.children.append(new_node)
