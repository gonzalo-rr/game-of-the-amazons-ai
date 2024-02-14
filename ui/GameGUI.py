from amazons.AmazonsLogic import Board
import pygame
from ui.DropDown import DropDown


class GameGUI:
    def __init__(self, width, height, tile_size):
        # Basic configuration
        self.width = width
        self.height = height
        self.tile_size = tile_size

        self.total_width = width + tile_size * 6
        self.total_height = height

        self.size = (self.total_width, self.total_height)
        self.screen = pygame.display.set_mode(self.size)
        self.font = pygame.font.Font('freesansbold.ttf', 40)
        self.big_font = pygame.font.Font('freesansbold.ttf', 50)

        self.timer = pygame.time.Clock()
        self.fps = 30

        # Play game button
        self.button_rect = pygame.Rect(width + tile_size, tile_size * 8, tile_size * 4, tile_size)

        # Game menu
        menu_rect1 = pygame.Rect(width + tile_size, tile_size, tile_size * 4, tile_size)
        menu_rect2 = pygame.Rect(width + tile_size, tile_size * 3, tile_size * 4, tile_size)
        self.screen.blit(self.font.render('White', True, 'black'),
                         (menu_rect1.x, menu_rect1.y - tile_size / 2))
        self.screen.blit(self.font.render('Black', True, 'black'),
                         (menu_rect2.x, menu_rect2.y - tile_size / 2))

        self.players = ['Human', 'Random']
        self.menu1 = DropDown(menu_rect1[0], menu_rect1[1], menu_rect1[2], menu_rect1[3],
                              self.players, self.big_font, self.font)
        self.menu2 = DropDown(menu_rect2[0], menu_rect2[1], menu_rect2[2], menu_rect2[3],
                              self.players, self.big_font, self.font)

        # Game pieces
        self.white_amazon = pygame.image.load('assets/images/white_amazon.png')
        self.white_amazon = pygame.transform.scale(self.white_amazon, (80, 80))

        self.black_amazon = pygame.image.load('assets/images/black_amazon.png')
        self.black_amazon = pygame.transform.scale(self.black_amazon, (80, 80))

        self.blocked_tile = pygame.image.load('assets/images/blocked_tile.png')
        self.blocked_tile = pygame.transform.scale(self.blocked_tile, (80, 80))

        # Game variables
        # 0 - whites turn no selection, 1 - whites turn selection, 2 - whites turn half move,
        # 3 - blacks turn no selection, 4 - blacks turn selection, 5 - blacks turn half move
        self.board = Board()

        self.turn_step = 0
        self.selection = None
        self.valid_moves = []

        self.white_positions = [(0, 6), (9, 6), (3, 9), (6, 9)]
        self.black_positions = [(3, 0), (6, 0), (0, 3), (9, 3)]
        self.blocked_positions = []

    def restart_game(self):
        # Game board
        self.board = Board()

        # Game variables
        # 0 - whites turn no selection, 1 - whites turn selection, 2 - whites turn half move,
        # 3 - blacks turn no selection, 4 - blacks turn selection, 5 - blacks turn half move
        self.turn_step = 0
        self.selection = None
        self.valid_moves = []

        self.white_positions = [(0, 6), (9, 6), (3, 9), (6, 9)]
        self.black_positions = [(3, 0), (6, 0), (0, 3), (9, 3)]
        self.blocked_positions = []

    def draw_board(self):
        for i in range(self.board.n + 1):
            pygame.draw.line(self.screen, 'black',
                             (0, i * self.tile_size), (self.height, i * self.tile_size))
            pygame.draw.line(self.screen, 'black',
                             (i * self.tile_size, 0), (i * 100, self.width))

    def draw_pieces(self):
        for column in range(self.board.n):
            for row in range(self.board.n):
                if self.board[column][row] == 1:  # White amazon
                    self.screen.blit(self.white_amazon, (self.tile_size * column + 10, self.tile_size * row + 10))
                elif self.board[column][row] == -1:  # Black amazon
                    self.screen.blit(self.black_amazon, (self.tile_size * column + 10, self.tile_size * row + 10))
                elif self.board[column][row] == 2:  # Arrow
                    self.screen.blit(self.blocked_tile, (self.tile_size * column + 10, self.tile_size * row + 10))

                if self.selection == (column, row):
                    pygame.draw.rect(self.screen, 'red',
                                     [column * self.tile_size + 1, row * self.tile_size + 1, 100, 100], 2)

    def handle_white_turn(self, click_coords):
        if click_coords in self.white_positions:  # Select a piece
            self.selection = click_coords
            if self.turn_step == 0:
                self.turn_step = 1

        if click_coords in self.valid_moves and self.selection is not None:
            if self.turn_step == 1:  # Move a piece
                self.white_positions.remove(self.selection)  # Previous position
                self.white_positions.append(click_coords)  # New position

                self.board.move_piece(self.selection, click_coords, 1)
                self.selection = click_coords
                self.turn_step = 2
                self.get_valid_moves()  # Get the new list of valid moves
            elif self.turn_step == 2:  # Shoot an arrow
                self.blocked_positions.append(click_coords)

                self.board.shoot_arrow(click_coords)
                self.turn_step = 3
                self.selection = None
                self.valid_moves = []

    def handle_black_turn(self, click_coords):
        if click_coords in self.black_positions:  # Select a piece
            self.selection = click_coords
            if self.turn_step == 3:
                self.turn_step = 4

        if click_coords in self.valid_moves and self.selection is not None:
            if self.turn_step == 4:  # Move a piece
                self.black_positions.remove(self.selection)  # Previous position
                self.black_positions.append(click_coords)  # New position

                self.board.move_piece(self.selection, click_coords, -1)
                self.selection = click_coords
                self.turn_step = 5
                self.get_valid_moves()  # Get the new list of valid moves
            elif self.turn_step == 5:  # Shoot an arrow
                self.blocked_positions.append(click_coords)

                self.board.shoot_arrow(click_coords)
                self.turn_step = 0
                self.selection = None
                self.valid_moves = []

    def get_valid_moves(self):
        if self.turn_step == 1 or self.turn_step == 4:  # White or black piece selected
            self.valid_moves = self.board.get_moves_position(self.selection)
        elif self.turn_step == 2 or self.turn_step == 5:  # White or black piece moved
            self.valid_moves = self.board.get_moves_position(self.selection)

    def draw_valid_moves(self):
        for move in self.valid_moves:
            pygame.draw.circle(self.screen, 'black',
                               (move[0] * self.tile_size + self.tile_size / 2,
                                move[1] * self.tile_size + self.tile_size / 2),
                               10)

    def draw_win(self, player):
        winner = 'white' if player == 1 else 'black'
        pygame.draw.rect(self.screen, 'black', [400, 400, 300, 200])
        self.screen.blit(self.font.render(f'{winner} won the game', True, 'white'), (420, 420))
        self.screen.blit(self.font.render('Press ENTER to restart', True, 'white'), (420, 560))

    def draw_menu(self):
        self.menu1.draw_menu(self.screen)
        if not self.menu1.deployed:
            self.menu2.draw_menu(self.screen)

    def handle_menu_event(self, event):
        if not self.menu1.handle_event(event):
            self.menu2.handle_event(event)

    def draw_play_button(self):
        text = 'Play'

        x_offset = (self.button_rect.width - self.big_font.size(text)[0]) / 2
        y_offset = self.button_rect.height / 2 - self.big_font.size(text)[1] / 2

        pygame.draw.rect(self.screen, 'black', self.button_rect, 3)
        self.screen.blit(self.big_font.render('Play', True, 'black'),
                         (self.button_rect.x + x_offset, self.button_rect.y + y_offset))

    # Returns True if the button was pressed with the intention to play
    def handle_play_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint((event.pos[0], event.pos[1])):
                return True

    def run(self):
        run = True
        playing = False
        game_over = False
        while run:
            self.timer.tick(self.fps)
            self.screen.fill('gray')
            self.draw_board()
            self.draw_pieces()
            self.draw_menu()
            self.draw_play_button()

            if self.selection is not None:
                self.get_valid_moves()
                self.draw_valid_moves()

            # Event handling
            for event in pygame.event.get():
                # Quit game
                if event.type == pygame.QUIT:
                    run = False

                # Menu options
                if not playing:
                    self.handle_menu_event(event)

                # Game start
                if not playing:
                    if self.handle_play_event(event):
                        playing = True

                if playing:
                    # Game moves
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
                        x_coord = event.pos[0] // self.tile_size
                        y_coord = event.pos[1] // self.tile_size
                        click_coords = (x_coord, y_coord)

                        if self.turn_step <= 2:  # White's turn
                            self.handle_white_turn(click_coords)
                        else:  # Black's turn
                            self.handle_black_turn(click_coords)

                    # Game restart
                    # if event.type == pygame.KEYDOWN and game_over:  # Both ifs for key pressed after game ended
                    #     if event.key == pygame.K_RETURN:
                    #         game_over = False
                    #         restart_game()

            # Game end
            if self.turn_step == 0 or self.turn_step == 3:  # Checks that the winner is not selected during a half-move
                if self.board.is_win(-1):  # Black wins
                    self.draw_win(-1)
                    game_over = True
                elif self.board.is_win(1):  # White wins
                    self.draw_win(1)
                    game_over = True

            pygame.display.flip()
        pygame.quit()
