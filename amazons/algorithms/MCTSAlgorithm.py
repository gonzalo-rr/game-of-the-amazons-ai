import random
import time

from amazons.AmazonsLogic import Board
from amazons.algorithms.mcts_tree.Node import Node


class MCTSAlgorithm:

    def __init__(self, max_time):
        self.max_time = max_time
        self.end = 0
        self.root = None

    def __str__(self):
        return "MCTS"

    def make_move(self, board, player):
        new_board = Board(board)

        self.end = time.time() + self.max_time
        self.root = Node(new_board, None, player)

        self.root.expand()
        count = 1
        while time.time() <= self.end:
            # print("count", count)
            # Selection
            best_node, best_ucb = self.select(self.root)
            # print("BEST:", best_ucb)

            # Expansion
            if best_node.s > 0:
                # print("expanding")
                best_node.expand()

            # Simulation
            win = self.simulate(best_node)

            # Backpropagation
            self.backpropagation(best_node, win)

            count+=1

        self.root.children.sort(key=lambda c: c.w)
        # print(self.root.children[0].action)
        return self.root.children[0].action

    def select(self, node):
        best_node = None
        best_ucb = 0

        for child in node.children:
            if len(child.children) == 0:  # Not yet expanded (leaf node)
                ucb = child.ucb_score()
                if ucb >= best_ucb:
                    best_ucb = ucb
                    best_node = child
            else:
                node, ucb = self.select(child)
                if ucb >= best_ucb:
                    best_node = node
                    best_ucb = ucb

        # print(best_ucb)
        return best_node, best_ucb

    def simulate(self, node):
        win = 0

        current_state = Board(node.state)
        current_player = node.player

        finished = False
        while not finished:
            if current_state.is_win(node.player):
                win = 1
                break
            if current_state.is_win(-node.player):
                break

            moves = current_state.get_legal_moves(current_player)

            move = random.choice(moves)  # random move
            current_state.execute_move(move, current_player)
            current_player *= -1



        return win

    def backpropagation(self, node, win):
        node.w += win
        node.s += 1

        current_node = node
        while current_node.parent is not None:
            current_node.parent.w += win
            current_node.parent.s += 1
            current_node = current_node.parent
