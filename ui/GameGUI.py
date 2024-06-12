from amazons.AmazonsLogic import Board
import pygame

from amazons.algorithms.mcts.MCTSAlgorithmUCB_cut import MCTSAlgorithm2
from amazons.algorithms.mcts.MCTSAlgorithmEGreedy import MCTSAlgorithmB
from amazons.algorithms.mcts.MCTSAlgorithmEGreedyMod import MCTSAlgorithmMAB
from ui.DropDown import DropDown
from amazons.players.HumanPlayer import HumanPlayer
from amazons.players.AIPlayer import AIPlayer

import threading

wait_time = 0000


class GameGUI:
    def __init__(self, tile_size):
        # Game variables
        # 0 - whites turn no selection, 1 - whites turn selection, 2 - whites turn half move,
        # 3 - blacks turn no selection, 4 - blacks turn selection, 5 - blacks turn half move
        self.board = Board(False)

        self.turn_step = 0
        self.selection = None
        self.valid_moves = []

        self.white_positions = self.board.white_positions
        self.black_positions = self.board.black_positions
        self.blocked_positions = []

        # Basic configuration
        self.running = True
        self.playing = False
        self.game_over = False
        self.waiting = 0
        self.making_move = False

        self.width = self.board.n * tile_size
        self.height = self.board.n * tile_size
        self.tile_size = tile_size

        self.total_width = self.width + tile_size * 6
        self.total_height = self.height

        self.size = (self.total_width, self.total_height)
        self.screen = pygame.display.set_mode(self.size)
        self.font = pygame.font.Font('freesansbold.ttf', 40)
        self.big_font = pygame.font.Font('freesansbold.ttf', 50)

        self.timer = pygame.time.Clock()
        self.fps = 30

        # Play game button
        self.button_rect = pygame.Rect(self.width + tile_size, tile_size * 8, tile_size * 4, tile_size)

        # Game menu
        menu_rect1 = pygame.Rect(self.width + tile_size, tile_size, tile_size * 4, tile_size)
        menu_rect2 = pygame.Rect(self.width + tile_size, tile_size * 3, tile_size * 4, tile_size)
        self.screen.blit(self.font.render('White', True, 'black'),
                         (menu_rect1.x, menu_rect1.y - tile_size / 2))
        self.screen.blit(self.font.render('Black', True, 'black'),
                         (menu_rect2.x, menu_rect2.y - tile_size / 2))

        options = ["Human", "MCTSB", "MCTS2", "MCTS_MAB"]
        self.menu1 = DropDown(menu_rect1[0], menu_rect1[1], menu_rect1[2], menu_rect1[3],
                              options, self.big_font, self.font)
        self.menu2 = DropDown(menu_rect2[0], menu_rect2[1], menu_rect2[2], menu_rect2[3],
                              options, self.big_font, self.font)

        # Game pieces
        self.white_amazon = pygame.image.load('amazons/assets/images/white_amazon.png')
        self.white_amazon = pygame.transform.scale(self.white_amazon, (80, 80))

        self.black_amazon = pygame.image.load('amazons/assets/images/black_amazon.png')
        self.black_amazon = pygame.transform.scale(self.black_amazon, (80, 80))

        self.blocked_tile = pygame.image.load('amazons/assets/images/blocked_tile.png')
        self.blocked_tile = pygame.transform.scale(self.blocked_tile, (80, 80))

        # minimax = MinimaxAlgorithmMultiProcess(1, 10, 6)
        # minimax = MinimaxAlgorithm(5, 2)
        # minimaxMob = MinimaxAlgorithmMobility(5, 2)
        # mctsA = MCTSAlgorithm(1000, 10)
        mctsB = MCTSAlgorithmB(1000, 10)
        mcts2 = MCTSAlgorithm2(1000, 10)
        mcts_mab = MCTSAlgorithmMAB(1000, 10)

        # Players
        self.players = [
            HumanPlayer(self),
            # AIPlayer(self, GreedyAlgorithmMobility(), wait_time),
            # AIPlayer(self, minimaxMob, wait_time),
            # AIPlayer(self, mctsA, wait_time),
            AIPlayer(self, mctsB, wait_time),
            AIPlayer(self, mcts2, wait_time),
            AIPlayer(self, mcts_mab, wait_time)
        ]
        self.white_player = self.players[0]
        self.black_player = self.players[0]

        # Event queue
        self.event_queue = None

    def restart_game(self):
        # Game board
        self.board = Board(False)

        # Game variables
        # 0 - whites turn no selection, 1 - whites turn selection, 2 - whites turn half move,
        # 3 - blacks turn no selection, 4 - blacks turn selection, 5 - blacks turn half move
        self.turn_step = 0
        self.selection = None
        self.valid_moves = []

        self.white_positions = self.board.white_positions
        self.black_positions = self.board.black_positions
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

    def get_valid_moves(self):
        if self.selection is not None:
            # White or black piece selected or moved
            if self.turn_step == 1 or self.turn_step == 2 or self.turn_step == 4 or self.turn_step == 5:
                self.valid_moves = self.board.get_moves_position(self.selection)

    def draw_valid_moves(self):
        self.get_valid_moves()
        for move in self.valid_moves:
            pygame.draw.circle(self.screen, 'black',
                               (move[0] * self.tile_size + self.tile_size / 2,
                                move[1] * self.tile_size + self.tile_size / 2),
                               10)

    def draw_win(self, player):
        winner = 'WHITE' if player == 1 else 'BLACK'
        self.screen.blit(self.font.render(f'{winner} WON', True, 'black'), (420, 420))

    def draw_menu(self):
        self.screen.blit(self.font.render("White", True, "black"),
                         (self.menu1.body.x, self.menu1.body.y - self.menu1.body.height / 2))
        self.menu1.draw_menu(self.screen)
        if not self.menu1.deployed:
            self.screen.blit(self.font.render("Black", True, "black"),
                             (self.menu2.body.x, self.menu2.body.y - self.menu2.body.height / 2))
            self.menu2.draw_menu(self.screen)

    def handle_menu_event(self, event):
        if not self.menu1.handle_event(event):
            self.menu2.handle_event(event)

    def draw_play_button(self):
        text = 'Play'

        x_offset = (self.button_rect.width - self.big_font.size(text)[0]) / 2
        y_offset = self.button_rect.height / 2 - self.big_font.size(text)[1] / 2

        pygame.draw.rect(self.screen, 'black', self.button_rect, 3)
        self.screen.blit(self.big_font.render(text, True, 'black'),
                         (self.button_rect.x + x_offset, self.button_rect.y + y_offset))

    def draw_restart_button(self):
        text = 'Restart'

        x_offset = (self.button_rect.width - self.big_font.size(text)[0]) / 2
        y_offset = self.button_rect.height / 2 - self.big_font.size(text)[1] / 2

        pygame.draw.rect(self.screen, 'black', self.button_rect, 3)
        self.screen.blit(self.big_font.render(text, True, 'black'),
                         (self.button_rect.x + x_offset, self.button_rect.y + y_offset))

    # Returns True if the button was pressed with the intention to play
    def handle_play_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint((event.pos[0], event.pos[1])):
                return True

    def set_players(self):
        self.white_player = self.players[self.menu1.selected_option]
        self.black_player = self.players[self.menu2.selected_option]

    def update_gui(self):
        self.screen.fill('gray')
        self.draw_board()
        self.draw_valid_moves()
        self.draw_pieces()
        self.draw_menu()

    def handle_turn(self, turn):
        player = self.white_player if turn == 1 else self.black_player
        if player.is_human():
            player.make_move()
        else:
            if not self.making_move:
                thread = threading.Thread(target=lambda: player.make_move())
                thread.daemon = True
                thread.start()
                self.making_move = True

    def make_move(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.game_over:
            x_coord = event.pos[0] // self.tile_size
            y_coord = event.pos[1] // self.tile_size
            click_coords = (x_coord, y_coord)

            if self.turn_step <= 2:
                self.handle_click(click_coords, 1)
            else:
                self.handle_click(click_coords, -1)

    def handle_click(self, click_coords, player):
        positions = self.white_positions if player == 1 else self.black_positions

        if self.turn_step != 2 and self.turn_step != 5:  # Piece not already selected
            if click_coords in positions:  # Select a piece
                self.select_amazon(click_coords)

        if click_coords in self.valid_moves and self.selection is not None:
            if player == 1:
                if self.turn_step == 1:  # Move a piece
                    self.move_piece(self.selection, click_coords, player)
                elif self.turn_step == 2:  # Shoot an arrow
                    self.shoot_arrow(click_coords)
            else:
                if self.turn_step == 4:  # Move a piece
                    self.move_piece(self.selection, click_coords, player)
                elif self.turn_step == 5:  # Shoot an arrow
                    self.shoot_arrow(click_coords)

    def select_amazon(self, amazon):
        self.selection = amazon
        if self.turn_step == 0:
            self.turn_step = 1
        elif self.turn_step == 3:
            self.turn_step = 4

        self.update_gui()
        pygame.display.flip()

    def move_piece(self, prev, new, player):
        self.board.move_piece(prev, new, player)
        self.selection = new
        self.turn_step += 1

        self.update_gui()
        pygame.display.flip()

    def shoot_arrow(self, pos):
        self.blocked_positions.append(pos)

        self.board.shoot_arrow(pos)
        self.turn_step = (self.turn_step + 1) % 5
        self.selection = None
        self.valid_moves = []

        self.update_gui()
        pygame.display.flip()

    def check_end(self):
        if self.turn_step != 2 and self.turn_step != 5:  # Checks that the winner is not selected during a half-move
            if self.board.is_win(-1):  # Black wins
                self.draw_win(-1)
                self.game_over = True
                self.playing = False
            elif self.board.is_win(1):  # White wins
                self.draw_win(1)
                self.game_over = True
                self.playing = False

    def run(self):
        self.timer.tick(self.fps)

        while self.running:
            self.update_gui()

            # Play button
            if not self.playing and not self.game_over:
                self.draw_play_button()

            # Restart button
            if self.game_over and not self.playing:
                self.draw_restart_button()

            self.event_queue = pygame.event.get()

            # Game end
            self.check_end()

            # Game moves
            if self.playing:
                if self.turn_step <= 2:  # White's turn
                    self.handle_turn(1)
                else:  # Black's turn
                    self.handle_turn(-1)

            # Event handling
            for event in self.event_queue:
                # Quit game
                if event.type == pygame.QUIT:
                    self.running = False
                    exit(-1)

                # Menu options and Game start
                if not self.playing:
                    self.handle_menu_event(event)
                    if self.handle_play_event(event):
                        self.playing = True
                        self.set_players()

                # Game restart
                if self.game_over:
                    if self.handle_play_event(event):
                        self.game_over = False
                        self.playing = True
                        self.restart_game()
                        self.set_players()

            pygame.display.flip()
        pygame.quit()
