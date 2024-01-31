from amazons.AmazonsLogic import Board
import pygame, sys

# Basic configuration
pygame.init()

width = 1_000
height = 1_000
tile_size = 100

size = (width, height)
screen = pygame.display.set_mode(size)
font = pygame.font.Font('freesansbold.ttf', 20)
pygame.display.set_caption('Game of the Amazons')
timer = pygame.time.Clock()
fps = 30

# Game board
board = Board()

# Game pieces
white_amazon = pygame.image.load('assets/images/white_amazon.png')
white_amazon = pygame.transform.scale(white_amazon, (80, 80))

black_amazon = pygame.image.load('assets/images/black_amazon.png')
black_amazon = pygame.transform.scale(black_amazon, (80, 80))

blocked_tile = pygame.image.load('assets/images/blocked_tile.png')
blocked_tile = pygame.transform.scale(blocked_tile, (80, 80))

# Game variables
# 0 - whites turn no selection, 1 - whites turn selection, 2 - whites turn half move,
# 3 - blacks turn no selection, 4 - blacks turn selection, 5 - blacks turn half move
turn_step = 0
selection = None
valid_moves = []

white_positions = [(0, 6), (9, 6), (3, 9), (6, 9)]
black_positions = [(3, 0), (6, 0), (0, 3), (9, 3)]
blocked_positions = []

def restart_game():
    global board, turn_step, selection, valid_moves, white_positions, black_positions, blocked_positions

    # Game board
    board = Board()

    # Game variables
    # 0 - whites turn no selection, 1 - whites turn selection, 2 - whites turn half move,
    # 3 - blacks turn no selection, 4 - blacks turn selection, 5 - blacks turn half move
    turn_step = 0
    selection = None
    valid_moves = []

    white_positions = [(0, 6), (9, 6), (3, 9), (6, 9)]
    black_positions = [(3, 0), (6, 0), (0, 3), (9, 3)]
    blocked_positions = []

def draw_board():
    for i in range(board.n):
        pygame.draw.line(screen, 'black', (0, i * tile_size), (height, i * tile_size))
        pygame.draw.line(screen, 'black', (i * tile_size, 0), (i * 100, width))


def draw_pieces():
    for column in range(board.n):
        for row in range(board.n):
            if board[column][row] == 1:  # White amazon
                screen.blit(white_amazon, (tile_size * column + 10, tile_size * row + 10))
            elif board[column][row] == -1:  # Black amazon
                screen.blit(black_amazon, (tile_size * column + 10, tile_size * row + 10))
            elif board[column][row] == 2:  # Arrow
                screen.blit(blocked_tile, (tile_size * column + 10, tile_size * row + 10))

            if selection == (column, row):
                pygame.draw.rect(screen, 'red',
                                 [column * tile_size + 1, row * tile_size + 1, 100, 100], 2)


def handle_white_turn(click_coords):
    global turn_step, valid_moves, selection, board

    if click_coords in white_positions:  # Select a piece
        selection = click_coords
        if turn_step == 0:
            turn_step = 1

    if click_coords in valid_moves and selection is not None:
        if turn_step == 1:  # Move a piece
            white_positions.remove(selection)  # Previous position
            white_positions.append(click_coords)  # New position

            board.move_piece(selection, click_coords, 1)
            selection = click_coords
            turn_step = 2
            get_valid_moves()  # Get the new list of valid moves
        elif turn_step == 2:  # Shoot an arrow
            blocked_positions.append(click_coords)

            board.shoot_arrow(click_coords)
            turn_step = 3
            selection = None
            valid_moves = []


def handle_black_turn(click_coords):
    global turn_step, valid_moves, selection, board

    if click_coords in black_positions:  # Select a piece
        selection = click_coords
        if turn_step == 3:
            turn_step = 4

    if click_coords in valid_moves and selection is not None:
        if turn_step == 4:  # Move a piece
            black_positions.remove(selection)  # Previous position
            black_positions.append(click_coords)  # New position

            board.move_piece(selection, click_coords, -1)
            selection = click_coords
            turn_step = 5
            get_valid_moves()  # Get the new list of valid moves
        elif turn_step == 5:  # Shoot an arrow
            blocked_positions.append(click_coords)

            board.shoot_arrow(click_coords)
            turn_step = 0
            selection = None
            valid_moves = []


def get_valid_moves():
    global valid_moves

    if turn_step == 1 or turn_step == 4:  # White or black piece selected
        valid_moves = board.get_moves_position(selection)
    elif turn_step == 2 or turn_step == 5:  # White or black piece moved
        valid_moves = board.get_moves_position(selection)


def draw_valid_moves():
    for move in valid_moves:
        pygame.draw.circle(screen, 'black',
                           (move[0] * tile_size + tile_size / 2, move[1] * tile_size + tile_size / 2),
                           10)


def draw_win(player):
    winner = 'white' if player == 1 else 'black'
    pygame.draw.rect(screen, 'black', [400, 400, 300, 200])
    screen.blit(font.render(f'{winner} won the game', True, 'white'), (420, 420))
    screen.blit(font.render('Press ENTER to restart', True, 'white'), (420, 560))


def main():
    global valid_moves

    run = True
    game_over = False
    while run:
        timer.tick(fps)
        screen.fill('gray')
        draw_board()
        draw_pieces()

        if selection is not None:
            get_valid_moves()
            draw_valid_moves()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Exit game
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:  # Click while playing
                x_coord = event.pos[0] // tile_size
                y_coord = event.pos[1] // tile_size
                click_coords = (x_coord, y_coord)

                if turn_step <= 2:  # White's turn
                    handle_white_turn(click_coords)
                else:  # Black's turn
                    handle_black_turn(click_coords)
            if event.type == pygame.KEYDOWN and game_over:  # Both ifs for key pressed after game ended
                if event.key == pygame.K_RETURN:
                    game_over = False
                    restart_game()

        if turn_step == 0 or turn_step == 3:  # This checks that the winner is not selected during a half-move
            if board.is_win(-1):  # Black wins
                draw_win(-1)
                game_over = True
            elif board.is_win(1):  # White wins
                draw_win(1)
                game_over = True

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
