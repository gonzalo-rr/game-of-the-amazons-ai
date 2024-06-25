import time

import pygame

from amazons.algorithms.algorithm import Algorithm
from amazons.logic.amazons_logic import Board
from amazons.players.player import Player


class AIPlayer(Player):
    """
    Class that represents an artificial intelligence player

    Attributes:
        __game: game graphic user interface
        __current_move: move chosen
        __algorithm: intelligent algorithm to make the move
        __wait_time: time to wait to simulate the time to move

    Author: Gonzalo Rodríguez Rodríguez
    """

    def __init__(self, game_gui, algorithm: Algorithm, wait_time: int) -> None:
        """
        Constructor of the class
        :param game_gui: game graphic user interface
        :param algorithm: intelligent algorithm to make the move
        :param wait_time: time to wait to simulate the time to move
        """
        # if not isinstance(game_gui, GameGUI):
        #     raise TypeError("game_gui must be a game interface")
        # if not isinstance(algorithm, Algorithm):
        #     raise TypeError("there must be a valid algorithm")
        # if type(wait_time) is not int:
        #     raise TypeError("wait_time must be an int")
        # if wait_time < 0:
        #     raise ValueError("wait_time must be greater thar or equal to 0")

        self.__game = game_gui
        self.__current_move = None
        self.__algorithm = algorithm
        self.__wait_time = wait_time

    def __str__(self) -> str:
        """
        Returns the string value of the class
        :return: the name of the algorithm
        """
        return str(self.__algorithm)

    def is_human(self) -> bool:
        """
        Returns if the player is human
        :return: False
        """
        return False

    def __wait(self, millis: int) -> None:
        """
        Method to execute the wait time
        :param millis: milliseconds to wait
        :return: None
        """
        end = round(time.time() * 1000) + millis
        while round(time.time() * 1000) < end:
            self.__game.event_queue = pygame.event.get()
            for event in self.__game.event_queue:
                # Quit game
                if event.type == pygame.QUIT:
                    self.__game.__running = False

    def make_move(self) -> None:
        """
        Method to execute a move
        :return: None
        """
        if self.__game.turn_step <= 2:  # White's turn
            player = 1
        else:  # Black's turn
            player = -1

        board = Board(self.__game.board)  # Copy board to avoid altering original UI board

        if board.is_win(player) or board.is_win(-player):
            return

        move = self.__algorithm.make_move(board, player)
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

        self.__game.making_move = False
