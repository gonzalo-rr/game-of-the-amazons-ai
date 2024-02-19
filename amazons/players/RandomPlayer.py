import time

import pygame
import random


class RandomPlayer:

    def __init__(self, game_gui):
        self.game = game_gui
        self.current_move = None

    def wait(self, millis):
        end = round(time.time() * 1000) + millis
        while round(time.time() * 1000) < end:
            self.game.event_queue = pygame.event.get()
            for event in self.game.event_queue:
                # Quit game
                if event.type == pygame.QUIT:
                    self.game.running = False

    def make_move(self):
        if self.game.turn_step <= 2:  # White's turn
            player = 1
        else:  # Black's turn
            player = -1

        moves = self.game.board.get_legal_moves(player)
        if len(moves) != 0:
            move = random.choice(moves)
            amazon = move[0]
            place = move[1]
            shoot = move[2]

            self.game.select_amazon(amazon)
            self.wait(2000)
            self.game.move_piece(amazon, place, player)
            self.wait(2000)
            self.game.shoot_arrow(shoot)

            event1 = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': amazon, 'button': 1})
            event2 = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': place, 'button': 1})
            event3 = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': shoot, 'button': 1})

            pygame.event.post(event1)
            pygame.event.post(event2)
            pygame.event.post(event3)

        return
