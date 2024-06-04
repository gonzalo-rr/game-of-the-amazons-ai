import pygame


class HumanPlayer:

    def __init__(self, game_gui):
        self.__game = game_gui

    def is_human(self):
        return True

    def make_move(self):
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
