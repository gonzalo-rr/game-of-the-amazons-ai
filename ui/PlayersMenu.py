import pygame

from amazons.players.Player import Player
from ui.DropDown import DropDown


class PlayersMenu:

    def __init__(self, screen: pygame.surface.Surface, location: (int, int), unit_size: int, players: list[Player],
                 big_font: pygame.font.Font, font: pygame.font.Font) -> None:
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
        self.screen.blit(self.font.render("White", True, "black"),
                         (self.dropdown1.body.x, self.dropdown1.body.y - self.dropdown1.body.height / 2))
        self.dropdown1.draw_menu(self.screen)
        if not self.dropdown1.deployed:
            self.screen.blit(self.font.render("Black", True, "black"),
                             (self.dropdown2.body.x, self.dropdown2.body.y - self.dropdown2.body.height / 2))
            self.dropdown2.draw_menu(self.screen)

    def handle_menu_event(self, event: pygame.event.Event) -> None:
        if not self.dropdown1.handle_event(event):
            self.dropdown2.handle_event(event)

    def get_players(self) -> (Player, Player):
        return self.players[self.dropdown1.selected_option], self.players[self.dropdown2.selected_option]
