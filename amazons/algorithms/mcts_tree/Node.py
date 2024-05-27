import math

from amazons.AmazonsLogic import Board


class Node:

    def __init__(self, state, action, player):
        self.state = state
        self.action = action
        self.player = player
        self.parent = None
        self.children = []
        self.w = 0
        self.s = 0
        self.c = 2
        self.N = 0

    def ucb_score(self):
        if self.s == 0:
            return float('inf')
        return (self.w / self.s) + self.c * math.sqrt(math.log(self.parent.s) / self.s)

    def expand(self):
        for move in self.state.get_legal_moves(self.player):
            new_board = Board(self.state)
            new_board.execute_move(move, self.player)
            new_node = Node(new_board, move, -self.player)
            new_node.parent = self
            self.children.append(new_node)
