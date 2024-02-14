import pygame


class HumanPlayer:

    def __init__(self, game_gui):
        self.game = game_gui

    def make_move(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.game.game_over:
            x_coord = event.pos[0] // self.game.tile_size
            y_coord = event.pos[1] // self.game.tile_size
            click_coords = (x_coord, y_coord)

            if self.game.turn_step <= 2:
                self.handle_click_white(click_coords)
            else:
                self.handle_click_black(click_coords)

    def handle_click_white(self, click_coords):
        if click_coords in self.game.white_positions:  # Select a piece
            self.game.selection = click_coords
            if self.game.turn_step == 0:
                self.game.turn_step = 1

        if click_coords in self.game.valid_moves and self.game.selection is not None:
            if self.game.turn_step == 1:  # Move a piece
                self.game.white_positions.remove(self.game.selection)  # Previous position
                self.game.white_positions.append(click_coords)  # New position

                self.game.board.move_piece(self.game.selection, click_coords, 1)
                self.game.selection = click_coords
                self.game.turn_step = 2
                self.game.get_valid_moves()  # Get the new list of valid moves
            elif self.game.turn_step == 2:  # Shoot an arrow
                self.game.blocked_positions.append(click_coords)

                self.game.board.shoot_arrow(click_coords)
                self.game.turn_step = 3
                self.game.selection = None
                self.game.valid_moves = []

    def handle_click_black(self, click_coords):
        if click_coords in self.game.black_positions:  # Select a piece
            self.game.selection = click_coords
            if self.game.turn_step == 3:
                self.game.turn_step = 4

        if click_coords in self.game.valid_moves and self.game.selection is not None:
            if self.game.turn_step == 4:  # Move a piece
                self.game.black_positions.remove(self.game.selection)  # Previous position
                self.game.black_positions.append(click_coords)  # New position

                self.game.board.move_piece(self.game.selection, click_coords, -1)
                self.game.selection = click_coords
                self.game.turn_step = 5
                self.game.get_valid_moves()  # Get the new list of valid moves
            elif self.game.turn_step == 5:  # Shoot an arrow
                self.game.blocked_positions.append(click_coords)

                self.game.board.shoot_arrow(click_coords)
                self.game.turn_step = 0
                self.game.selection = None
                self.game.valid_moves = []
