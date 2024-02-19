import pygame


class HumanPlayer:

    def __init__(self, game_gui):
        self.game = game_gui

    def make_move(self):
        for event in self.game.event_queue:
            # Quit game
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.game.game_over:
                x_coord = event.pos[0] // self.game.tile_size
                y_coord = event.pos[1] // self.game.tile_size
                click_coords = (x_coord, y_coord)

                if self.game.turn_step <= 2:
                    self.game.handle_click(click_coords, 1)
                else:
                    self.game.handle_click(click_coords, -1)
