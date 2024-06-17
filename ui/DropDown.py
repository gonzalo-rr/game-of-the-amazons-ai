import pygame

from amazons.algorithms.Algorithm import Algorithm


class DropDown:

    def __init__(self, x: (int, int), y: (int, int), width: int, height: int, options: list[str],
                 big_font: pygame.font.Font, font: pygame.font.Font):
        self.body = pygame.Rect(x, y, width, height)
        self.__options = options
        self.__big_font = big_font
        self.__font = font

        self.deployed = False
        self.active = False
        self.selected_option = 0

    def draw_menu(self, screen: pygame.surface.Surface) -> None:
        # Draw current option
        self.__draw_option(screen, self.__options[self.selected_option], self.body.x, self.body.y)

        # Draw other options
        if self.deployed:
            for i in range(len(self.__options)):
                self.__draw_option(screen, self.__options[i], self.body.x, self.body.y + (i + 1) * self.body.height)

    def __draw_option(self, screen: pygame.surface.Surface, option: str, x: (int, int), y: (int, int)):
        x_offset = (self.body.width - self.__big_font.size(option)[0]) / 2
        y_offset = self.body.height / 2 - self.__big_font.size(option)[1] / 2

        option_rect = pygame.Rect(x, y, self.body.width, self.body.height)
        screen.fill('gray', option_rect)
        pygame.draw.rect(screen, 'black', option_rect, 3)
        screen.blit(self.__big_font.render(option, True, 'black'), (x + x_offset, y + y_offset))

    # True in an option has been selected, False otherwise
    def handle_event(self, event: pygame.event.Event) -> bool:
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
