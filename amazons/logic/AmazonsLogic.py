"""
Board data:
    1=white, -1=black, 0=empty, 2=blocked

    move = (amazon, place, shoot) where:
        amazon: the piece that will be moved
        place: the tile where the piece will be moved
        shoot: the tile that will be shot by the amazon
"""
from copy import copy


class Board:
    __directions = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]

    def __init__(self, *args):
        self.white_positions = []
        self.black_positions = []
        if len(args) == 1:
            if type(args[0]) is bool:
                if args[0]:  # Small is True
                    self.n = 5  # Dimension of the board
                    self.board = [[]] * self.n  # Board

                    for i in range(self.n):
                        self.board[i] = [0] * self.n

                    self.board[1][0] = -1
                    self.board[3][0] = -1
                    self.board[0][1] = -1
                    self.board[4][1] = -1

                    self.board[0][3] = 1
                    self.board[4][3] = 1
                    self.board[1][4] = 1
                    self.board[3][4] = 1

                    self.black_positions = [(1, 0), (3, 0), (0, 1), (4, 1)]
                    self.white_positions = [(0, 3), (4, 3), (1, 4), (3, 4)]
                else:  # Big is False
                    self.n = 10  # Dimension of the board
                    self.board = [[]] * self.n  # Board

                    for i in range(self.n):
                        self.board[i] = [0] * self.n

                    self.board[3][0] = -1
                    self.board[6][0] = -1
                    self.board[0][3] = -1
                    self.board[9][3] = -1

                    self.board[0][6] = 1
                    self.board[9][6] = 1
                    self.board[3][9] = 1
                    self.board[6][9] = 1

                    self.black_positions = [(3, 0), (6, 0), (0, 3), (9, 3)]
                    self.white_positions = [(0, 6), (9, 6), (3, 9), (6, 9)]
            else:
                prev_board = args[0]
                self.n = len(prev_board.board)  # Dimension of the board
                self.board = [[]] * self.n  # Board

                for i in range(self.n):
                    self.board[i] = copy(prev_board.board[i])

                self.black_positions = copy(prev_board.black_positions)
                self.white_positions = copy(prev_board.white_positions)
        else:
            return  # Error

    def __getitem__(self, index):
        return self.board[index]

    def __eq__(self, other):
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] != other.board[i][j]:
                    return False
        return True

    """
    Get all the legal moves for a player (-1 is black, 1 is white)
    """

    def get_legal_moves(self, player):
        moves = []

        # Find the positions of the player's amazons
        amazons = []

        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == player:
                    amazons.append((i, j))
                    if len(amazons) == 4:
                        break
            else:
                continue
            break

        # Find the moves for each amazon
        for amazon in amazons:
            for move in self.get_moves_amazon(amazon, player):
                moves.append(move)
        return moves

    """
    Get the full moves for a certain amazon
    """

    def get_moves_amazon(self, amazon, player):
        moves = []

        for move in self.get_moves_position(amazon):  # Get the 'physical' moves
            self.board[amazon[0]][amazon[1]] = 0
            for shot in self.get_moves_position(move):  # For each 'physical' move get each arrow shot
                moves.append((amazon, move, shot))
            self.board[amazon[0]][amazon[1]] = player

        return moves

    """
    Get the queen-like moves from a certain position
    """

    def get_moves_position(self, position):
        moves = []

        for direction in self.__directions:
            x = position[0] + direction[0]
            y = position[1] + direction[1]

            while self.n > x >= 0 and self.n > y >= 0 and self.board[x][y] == 0:
                moves.append((x, y))
                x += direction[0]
                y += direction[1]

        return moves

    """
    :returns True is the specified player has legal moves and False otherwise
    """

    def has_legal_moves(self, player):
        if len(self.get_legal_moves(player)) > 0:
            return True
        else:
            return False

    def is_win(self, player):
        if not (self.has_legal_moves(-player)):
            return True
        else:
            return False

    """
    Executes a full move on the board
    
    A move has the following elements:
    amazon: the piece that will be moved
    place: the tile where the piece will be moved
    shoot: the tile that will be shot by the amazon
    """

    def execute_move(self, move, player):
        if not self.check_valid_move(move):
            return

        (amazon, place, shoot) = move

        self.move_piece(amazon, place, player)

        self.shoot_arrow(shoot)

    def undo_move(self, move, player):
        if not self.check_valid_move(move):
            return

        (amazon, place, shoot) = move

        self.board[shoot[0]][shoot[1]] = 0

        self.board[place[0]][place[1]] = 0

        self.board[amazon[0]][amazon[1]] = player

        if player == 1:  # White
            self.white_positions.remove(place)
            self.white_positions.append(amazon)
        else:  # Black
            self.black_positions.remove(place)
            self.black_positions.append(amazon)

    """
    :returns True if the specified move is valid and False otherwise
    """

    def check_valid_move(self, move):
        return True

    """
    Moves a piece from one tile to another
    (note that this is not a full move, just a piece move without the shot)
    """

    def move_piece(self, amazon, place, player):
        (x1, y1) = amazon
        (x2, y2) = place

        self.board[x1][y1] = 0

        self.board[x2][y2] = player

        if player == 1:  # White
            self.white_positions.remove(amazon)
            self.white_positions.append(place)
        else:  # Black
            self.black_positions.remove(amazon)
            self.black_positions.append(place)

    """
    Blocks a tile from the board
    """

    def shoot_arrow(self, shoot):
        (x, y) = shoot

        self.board[x][y] = 2

    """
    Prints the board xd
    """

    def print_board(self):
        for i in range(self.n):
            for j in range(self.n):
                print(self.board[j][i], end="\t")
            print()