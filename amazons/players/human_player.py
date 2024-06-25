import pygame

from amazons.players.player import Player


class HumanPlayer(Player):
    """
    Class that represents a human player

    Attributes:
        __game: game graphic user interface

    Author: Gonzalo Rodríguez Rodríguez
    """

    def __init__(self, game_gui):
        """
        Constructor of the class
        :param game_gui: game graphic user interface
        """
        # if not isinstance(game_gui, GameGUI):
        #     raise TypeError("game_gui must be a game interface")

        self.__game = game_gui

    def __str__(self) -> str:
        """
        Returns the string value of the class
        :return: "Human"
        """
        return "Human"

    def is_human(self) -> bool:
        """
        Returns if the player is human
        :return: True
        """
        return True

    def make_move(self) -> None:
        """
        Method to execute the wait time
        :return: None
        """
        for event in self.__game.event_queue:
            # Quit game
            if event.type == pygame.QUIT:
                self.__game.__running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.__game.game_over:
                x_coord = event.pos[0] // self.__game.tile_size
                y_coord = event.pos[1] // self.__game.tile_size
                click_coords = (x_coord, y_coord)

                if self.__game.turn_step <= 2:
                    self.__game.handle_click(click_coords, 1)
                else:
                    self.__game.handle_click(click_coords, -1)
