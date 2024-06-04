import time

import pygame


class AIPlayer:

    def __init__(self, game_gui, algorithm, wait_time):
        self.__game = game_gui
        self.__current_move = None
        self.__algorithm = algorithm
        self.__wait_time = wait_time

    def is_human(self):
        return False

    def __wait(self, millis):
        end = round(time.time() * 1000) + millis
        while round(time.time() * 1000) < end:
            self.__game.event_queue = pygame.event.get()
            for event in self.__game.event_queue:
                # Quit game
                if event.type == pygame.QUIT:
                    self.__game.__running = False

    def make_move(self):
        if self.__game.turn_step <= 2:  # White's turn
            player = 1
        else:  # Black's turn
            player = -1

        if self.__game.board.is_win(player) or self.__game.board.is_win(-player):
            return

        move = self.__algorithm.make_move(self.__game.board, player)
        if move is None:
            return

        amazon = move[0]
        place = move[1]
        shoot = move[2]

        self.__game.select_amazon(amazon)
        self.__wait(self.__wait_time // 2)
        self.__game.move_piece(amazon, place, player)
        self.__wait(self.__wait_time // 2)
        self.__game.shoot_arrow(shoot)

        event1 = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': amazon, 'button': 1})
        event2 = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': place, 'button': 1})
        event3 = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': shoot, 'button': 1})

        pygame.event.post(event1)
        pygame.event.post(event2)
        pygame.event.post(event3)

        self.__game.__making_move = False
