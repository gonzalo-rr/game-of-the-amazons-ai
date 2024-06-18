from amazons.algorithms.Algorithm import Algorithm
from amazons.logic.AmazonsLogic import Board
import pygame

from amazons.players.HumanPlayer import HumanPlayer
from amazons.players.AIPlayer import AIPlayer

import threading

from ui.PlayersMenu import PlayersMenu

wait_time = 0000


class GameGUI:
    def __init__(self, tile_size: int, algorithms: list[Algorithm]) -> None:
        self.board = Board()

        # Game variables
        # 0 - whites turn no selection, 1 - whites turn selection, 2 - whites turn half move,
        # 3 - blacks turn no selection, 4 - blacks turn selection, 5 - blacks turn half move

        self.turn_step = 0
        self.__selection = None
        self.__valid_moves = []

        self.__white_positions = self.board.white_positions
        self.__black_positions = self.board.black_positions
        self.__blocked_positions = []

        # Basic configuration
        self.__running = True
        self.__playing = False
        self.game_over = False
        self.__waiting = 0
        self.making_move = False

        self.width = self.board.n * tile_size
        self.height = self.board.n * tile_size
        self.tile_size = tile_size

        self.total_width = self.width + tile_size * 6
        self.total_height = self.height

        self.size = (self.total_width, self.total_height)
        self.screen = pygame.display.set_mode(self.size)
        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.big_font = pygame.font.Font('freesansbold.ttf', 40)

        self.__timer = pygame.time.Clock()
        self.__fps = 30

        # Play game button
        self.__button_rect = pygame.Rect(self.width + tile_size, tile_size * 8.5, tile_size * 4, tile_size * 3/4)

        # Players
        self.__players = []
        self.__players.append(HumanPlayer(self))
        for algorithm in algorithms:
            self.__players.append(AIPlayer(self, algorithm, wait_time))
        self.white_player = self.__players[0]
        self.black_player = self.__players[0]

        # Game menu
        self.__menu = PlayersMenu(self.screen, (self.width + tile_size, tile_size), tile_size, self.__players,
                                  self.big_font, self.font)

        # Game pieces
        self.__white_amazon = pygame.image.load('assets/images/white_amazon.png')
        self.__white_amazon = pygame.transform.scale(self.__white_amazon, (80, 80))

        self.__black_amazon = pygame.image.load('assets/images/black_amazon.png')
        self.__black_amazon = pygame.transform.scale(self.__black_amazon, (80, 80))

        self.__blocked_tile = pygame.image.load('assets/images/blocked_tile.png')
        self.__blocked_tile = pygame.transform.scale(self.__blocked_tile, (80, 80))

        # Event queue
        self.event_queue = None

    def __restart_game(self) -> None:
        # Game board
        self.board = Board()

        # Game variables
        # 0 - whites turn no selection, 1 - whites turn selection, 2 - whites turn half move,
        # 3 - blacks turn no selection, 4 - blacks turn selection, 5 - blacks turn half move
        self.turn_step = 0
        self.__selection = None
        self.__valid_moves = []

        self.__white_positions = self.board.white_positions
        self.__black_positions = self.board.black_positions
        self.__blocked_positions = []

    def __draw_board(self) -> None:
        for i in range(self.board.n + 1):
            pygame.draw.line(self.screen, 'black',
                             (0, i * self.tile_size), (self.height, i * self.tile_size))
            pygame.draw.line(self.screen, 'black',
                             (i * self.tile_size, 0), (i * 100, self.width))

    def __draw_pieces(self) -> None:
        for column in range(self.board.n):
            for row in range(self.board.n):
                if self.board[column][row] == 1:  # White amazon
                    self.screen.blit(self.__white_amazon, (self.tile_size * column + 10, self.tile_size * row + 10))
                elif self.board[column][row] == -1:  # Black amazon
                    self.screen.blit(self.__black_amazon, (self.tile_size * column + 10, self.tile_size * row + 10))
                elif self.board[column][row] == 2:  # Arrow
                    self.screen.blit(self.__blocked_tile, (self.tile_size * column + 10, self.tile_size * row + 10))

                if self.__selection == (column, row):
                    pygame.draw.rect(self.screen, 'red',
                                     [column * self.tile_size + 1, row * self.tile_size + 1, 100, 100], 2)

    def __get_valid_moves(self) -> None:
        if self.__selection is not None:
            # White or black piece selected or moved
            if self.turn_step == 1 or self.turn_step == 2 or self.turn_step == 4 or self.turn_step == 5:
                self.__valid_moves = self.board.get_moves_position(self.__selection)

    def __draw_valid_moves(self) -> None:
        self.__get_valid_moves()
        for move in self.__valid_moves:
            pygame.draw.circle(self.screen, 'black',
                               (move[0] * self.tile_size + self.tile_size / 2,
                                move[1] * self.tile_size + self.tile_size / 2),
                               10)

    def __draw_win(self, player: int) -> None:
        winner = 'WHITE' if player == 1 else 'BLACK'
        self.screen.blit(self.big_font.render(f'{winner} WON', True, 'black'), (420, 420))

    def __draw_play_button(self) -> None:
        text = 'Play'

        x_offset = (self.__button_rect.width - self.big_font.size(text)[0]) / 2
        y_offset = self.__button_rect.height / 2 - self.big_font.size(text)[1] / 2

        pygame.draw.rect(self.screen, 'black', self.__button_rect, 3)
        self.screen.blit(self.big_font.render(text, True, 'black'),
                         (self.__button_rect.x + x_offset, self.__button_rect.y + y_offset))

    def __draw_restart_button(self) -> None:
        text = 'Restart'

        x_offset = (self.__button_rect.width - self.big_font.size(text)[0]) / 2
        y_offset = self.__button_rect.height / 2 - self.big_font.size(text)[1] / 2

        pygame.draw.rect(self.screen, 'black', self.__button_rect, 3)
        self.screen.blit(self.big_font.render(text, True, 'black'),
                         (self.__button_rect.x + x_offset, self.__button_rect.y + y_offset))

    # Returns True if the button was pressed with the intention to play
    def __handle_play_event(self, event: pygame.event.Event) -> bool | None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.__button_rect.collidepoint((event.pos[0], event.pos[1])):
                return True

    def __update_gui(self) -> None:
        self.screen.fill('gray')
        self.__draw_board()
        self.__draw_valid_moves()
        self.__draw_pieces()
        self.__menu.draw()

    def __handle_turn(self, turn: int) -> None:
        player = self.white_player if turn == 1 else self.black_player
        if player.is_human():
            player.make_move()
        else:
            if not self.making_move:
                thread = threading.Thread(target=lambda: player.make_move())
                thread.daemon = True
                thread.start()
                self.making_move = True

    def make_move(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.game_over:
            x_coord = event.pos[0] // self.tile_size
            y_coord = event.pos[1] // self.tile_size
            click_coords = (x_coord, y_coord)

            if self.turn_step <= 2:
                self.handle_click(click_coords, 1)
            else:
                self.handle_click(click_coords, -1)

    def handle_click(self, click_coords: (int, int), player: int) -> None:
        positions = self.__white_positions if player == 1 else self.__black_positions

        if self.turn_step != 2 and self.turn_step != 5:  # Piece not already selected
            if click_coords in positions:  # Select a piece
                self.select_amazon(click_coords)

        if click_coords in self.__valid_moves and self.__selection is not None:
            if player == 1:
                if self.turn_step == 1:  # Move a piece
                    self.move_piece(self.__selection, click_coords, player)
                elif self.turn_step == 2:  # Shoot an arrow
                    self.shoot_arrow(click_coords)
            else:
                if self.turn_step == 4:  # Move a piece
                    self.move_piece(self.__selection, click_coords, player)
                elif self.turn_step == 5:  # Shoot an arrow
                    self.shoot_arrow(click_coords)

    def select_amazon(self, amazon: (int, int)) -> None:
        self.__selection = amazon
        if self.turn_step == 0:
            self.turn_step = 1
        elif self.turn_step == 3:
            self.turn_step = 4

        self.__update_gui()
        pygame.display.flip()

    def move_piece(self, prev: (int, int), new: (int, int), player: int) -> None:
        self.board.move_piece(prev, new, player)
        self.__selection = new
        self.turn_step += 1

        self.__update_gui()
        pygame.display.flip()

    def shoot_arrow(self, pos: (int, int)) -> None:
        self.__blocked_positions.append(pos)

        self.board.shoot_arrow(pos)
        self.turn_step = (self.turn_step + 1) % 5
        self.__selection = None
        self.__valid_moves = []

        self.__update_gui()
        pygame.display.flip()

    def __check_end(self) -> None:
        if self.turn_step == 0 or 3:
            if self.board.is_win(-1):  # Black wins
                self.__draw_win(-1)
                self.game_over = True
                self.__playing = False
            elif self.board.is_win(1):  # White wins
                self.__draw_win(1)
                self.game_over = True
                self.__playing = False

    def run(self) -> None:
        self.__timer.tick(self.__fps)

        while self.__running:
            self.__update_gui()

            # Play button
            if not self.__playing and not self.game_over:
                self.__draw_play_button()

            # Restart button
            if self.game_over and not self.__playing:
                self.__draw_restart_button()

            self.event_queue = pygame.event.get()

            # Game moves
            if self.__playing:
                if self.turn_step <= 2:  # White's turn
                    self.__handle_turn(1)
                else:  # Black's turn
                    self.__handle_turn(-1)

            # Game end
            self.__check_end()

            # Event handling
            for event in self.event_queue:
                # Quit game
                if event.type == pygame.QUIT:
                    self.__running = False
                    exit(-1)

                # Menu options and Game start
                if not self.__playing:
                    self.__menu.handle_menu_event(event)
                    if self.__handle_play_event(event):
                        self.__playing = True
                        self.white_player, self.black_player = self.__menu.get_players()

                # Game restart
                if self.game_over:
                    if self.__handle_play_event(event):
                        self.game_over = False
                        self.__playing = True
                        self.__restart_game()
                        self.white_player, self.black_player = self.__menu.get_players()

            pygame.display.flip()
        pygame.quit()
