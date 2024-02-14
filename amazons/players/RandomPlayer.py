import pygame
import random


class RandomPlayer:

    def __init__(self, game_gui):
        self.game = game_gui

    def make_move(self, event):
        if self.game.turn_step <= 2:  # White's turn
            player = 1
        else:  # Black's turn
            player = -1

        moves = self.game.board.get_legal_moves(player)
        if len(moves) != 0:
            move = random.choice(moves)

            self.game.board.execute_move(move, player)

            self.game.turn_step = 3 if player == 1 else 0
            self.game.selection = None
            self.game.valid_moves = []
