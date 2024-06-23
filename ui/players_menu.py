import pygame

from amazons.players.player import Player
from ui.drop_down import DropDown


class PlayersMenu:
    """
    Class for the full menu with 2 dropdowns to choose the players

    Attributes:
        screen: surface to draw the menu on
        unit_size: unit of size to use
        players: list of players to show
        big_font: big font to write
        font: normal font to write
        menu_rect1: surface containing the first dropdown
        menu_rect2: surface containing the second dropdown
        dropdown1: first dropdown
        dropdown2: second dropdown
        white_player: current white player
        black_player: current black player

    Author: Gonzalo Rodríguez Rodríguez
    """

    def __init__(self, screen: pygame.surface.Surface, location: (int, int), unit_size: int, players: list[Player],
                 big_font: pygame.font.Font, font: pygame.font.Font) -> None:
        """
        Constructor for the class
        :param screen: surface to draw the menu on
        :param location: position of the menu
        :param unit_size: unit of size to use
        :param players: list of players to show
        :param big_font: big font to write
        :param font: normal font to write
        """
        self.screen = screen
        self.unit_size = unit_size
        self.players = players
        self.big_font = big_font
        self.font = font

        x = location[0]
        y = location[1]

        self.menu_rect1 = pygame.Rect(x, y, unit_size * 4, unit_size * (3 / 4))
        self.menu_rect2 = pygame.Rect(x, unit_size * 3, unit_size * 4, unit_size * (3 / 4))

        self.screen.blit(font.render('White', True, 'black'),
                         (self.menu_rect1.x, self.menu_rect1.y - unit_size / 2))
        self.screen.blit(font.render('Black', True, 'black'),
                         (self.menu_rect2.x, self.menu_rect2.y - unit_size / 2))

        options = []
        for player in players:
            options.append(str(player))

        self.dropdown1 = DropDown(self.menu_rect1[0], self.menu_rect1[1], self.menu_rect1[2], self.menu_rect1[3],
                                  options, big_font, font)
        self.dropdown2 = DropDown(self.menu_rect2[0], self.menu_rect2[1], self.menu_rect2[2], self.menu_rect2[3],
                                  options, big_font, font)

        self.white_player = players[0]
        self.black_player = players[0]

    def draw(self) -> None:
        """
        Method to draw the menu
        :return: None
        """
        self.screen.blit(self.font.render("White", True, "black"),
                         (self.dropdown1.body.x, self.dropdown1.body.y - self.dropdown1.body.height / 2))
        self.dropdown1.draw_menu(self.screen)
        if not self.dropdown1.deployed:
            self.screen.blit(self.font.render("Black", True, "black"),
                             (self.dropdown2.body.x, self.dropdown2.body.y - self.dropdown2.body.height / 2))
            self.dropdown2.draw_menu(self.screen)

    def handle_menu_event(self, event: pygame.event.Event) -> None:
        """
        Method to handle menu event
        :param event: event to handle
        :return: None
        """
        if not self.dropdown1.handle_event(event):
            self.dropdown2.handle_event(event)

    def get_players(self) -> (Player, Player):
        """
        Method to get the current selected players
        :return: selected players in a tuple, first is white player, second is black player
        """
        return self.players[self.dropdown1.selected_option], self.players[self.dropdown2.selected_option]
