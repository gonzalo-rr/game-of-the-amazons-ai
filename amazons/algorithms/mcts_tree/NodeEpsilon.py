import math

from amazons.AmazonsLogic import Board


class NodeEpsilon:

    def __init__(self, state, action, player):
        self.state = state
        self.action = action
        self.player = player
        self.parent = None
        self.children = []
        self.w = 0  # number of simulations resulting in a win
        self.s = 0  # number of simulations
        self.c = 2  # exploration parameter
        self.N = 0

        self.Q = 1

    def ucb_score(self):
        if self.s == 0:
            return float('inf')
        return (self.w / self.s) + self.c * math.sqrt(math.log(self.parent.s) / self.s)

    def expand(self):
        moves = self.state.get_legal_moves(self.player)
        # Order moves by function
        # Take 48 best moves
        for move in moves:
            new_board = Board(self.state)
            new_board.execute_move(move, self.player)
            new_node = NodeEpsilon(new_board, move, -self.player)
            new_node.parent = self
            self.children.append(new_node)
