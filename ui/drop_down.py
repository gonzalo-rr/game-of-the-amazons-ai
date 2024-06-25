import pygame

from amazons.algorithms.algorithm import Algorithm


class DropDown:
    """
    Class for the dropdowns in the gui

    Attributes:
        body: body of the dropdown
        __options: list of strings, they are the names of the possible algorithm options
        __big_font: big font
        __font: normal font
        deployed: boolean that represents if the dropdown is deployed or not
        active: boolean that represents if the dropdown is active and can be interacted with
        selected_option: index of the currently selected option

    Author: Gonzalo Rodríguez Rodríguez
    """

    def __init__(self, x: tuple, y: tuple, width: int, height: int, options: list,
                 big_font: pygame.font.Font, font: pygame.font.Font) -> None:
        """
        Constructor of the class
        :param x: x coordinate for the position of the dropdown
        :param y: y coordinate for the position of the dropdown
        :param width: width of the dropdown
        :param height: height of the dropdown
        :param options: string options of the dropdown
        :param big_font: big font to display text
        :param font: normal font to display text
        :return: None
        """
        self.body = pygame.Rect(x, y, width, height)
        self.__options = options
        self.__big_font = big_font
        self.__font = font

        self.deployed = False
        self.active = False
        self.selected_option = 0

    def draw_menu(self, screen: pygame.surface.Surface) -> None:
        """
        Method to draw the menu
        :param screen: surface to draw the menu on
        :return: None
        """
        # Draw current option
        self.__draw_option(screen, self.__options[self.selected_option], self.body.x, self.body.y)

        # Draw other options
        if self.deployed:
            for i in range(len(self.__options)):
                self.__draw_option(screen, self.__options[i], self.body.x, self.body.y + (i + 1) * self.body.height)

    def __draw_option(self, screen: pygame.surface.Surface, option: str, x: int, y: int) -> None:
        """
        Method to draw an option
        :param screen: surface to draw the menu on
        :param option: option string to draw
        :param x: x coordinate of the option
        :param y: y coordinate of the option
        :return: None
        """
        x_offset = (self.body.width - self.__big_font.size(option)[0]) / 2
        y_offset = self.body.height / 2 - self.__big_font.size(option)[1] / 2

        option_rect = pygame.Rect(x, y, self.body.width, self.body.height)
        screen.fill('gray', option_rect)
        pygame.draw.rect(screen, 'black', option_rect, 3)
        screen.blit(self.__big_font.render(option, True, 'black'), (x + x_offset, y + y_offset))

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle an event for the dropdown
        :param event: event to be handled
        :return: a boolean that is True in an option has been selected, False otherwise
        """
        pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not self.deployed:  # Menu not deployed
                if self.body.collidepoint(pos):
                    self.deployed = True
            else:  # Menu deployed
                self.deployed = False
                for i in range(len(self.__options)):
                    option = self.body.copy()
                    option.y += (i + 1) * self.body.height
                    if option.collidepoint(pos):
                        self.selected_option = i
                        return True

        return False
