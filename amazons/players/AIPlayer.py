import time

import pygame


class AIPlayer:

    def __init__(self, game_gui, algorithm, wait_time):
        self.game = game_gui
        self.current_move = None
        self.algorithm = algorithm
        self.wait_time = wait_time

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

        if self.game.board.is_win(player) or self.game.board.is_win(-player):
            return

        move = self.algorithm.make_move(self.game.board, player)
        if move is None:
            return

        amazon = move[0]
        place = move[1]
        shoot = move[2]

        self.game.select_amazon(amazon)
        self.wait(self.wait_time // 2)
        self.game.move_piece(amazon, place, player)
        self.wait(self.wait_time // 2)
        self.game.shoot_arrow(shoot)

        event1 = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': amazon, 'button': 1})
        event2 = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': place, 'button': 1})
        event3 = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': shoot, 'button': 1})

        pygame.event.post(event1)
        pygame.event.post(event2)
        pygame.event.post(event3)
