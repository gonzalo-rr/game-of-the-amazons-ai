import random

from amazons.AmazonsLogic import Board


class NodeEpsilon:

    def __init__(self, state, action, player):
        self.state = Board(state)
        self.action = action
        self.player = player
        self.parent = None
        self.children = []

        self.w = 0

        self.n = 0  # number of simulations
        self.Q = 1  # action value estimate

    def __eq__(self, other):
        return self.state == other.state

    def expand(self):
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

    def __sort_moves(self, moves):
        rating = []
        for move in moves:
            self.state.execute_move(move, self.player)
            rating.append(self.__evaluate_mobility(self.state))
            self.state.undo_move(move, self.player)

        combi = zip(moves, rating)
        combi = sorted(combi, key=lambda c: c[1], reverse=self.player == 1)
        return [item[0] for item in combi]

    def __evaluate_mobility(self, board):
        if board.is_win(1):
            return float('inf')
        if board.is_win(-1):
            return float('-inf')

        white_moves = board.get_legal_moves(1)
        black_moves = board.get_legal_moves(-1)
        return len(white_moves) - len(black_moves)
