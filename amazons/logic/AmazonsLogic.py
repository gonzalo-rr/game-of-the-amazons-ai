from copy import copy


class Board:
    """
    Board data:
        1=white, -1=black, 0=empty, 2=blocked

        move = (amazon, place, shoot) where:
            amazon: the piece that will be moved
            place: the tile where the piece will be moved
            shoot: the tile that will be shot by the amazon
    """

    __directions = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]

    def __init__(self, *args):
        if len(args) == 0:
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
        elif len(args) == 1:
            if not isinstance(args[0], Board):
                raise TypeError("argument must be of type Board")  # throw type error

            prev_board = args[0]
            self.n = len(prev_board.board)  # Dimension of the board
            self.board = [[]] * self.n  # Board

            for i in range(self.n):
                self.board[i] = copy(prev_board.board[i])

            self.black_positions = copy(prev_board.black_positions)
            self.white_positions = copy(prev_board.white_positions)
        else:
            raise ValueError("invalid number of arguments, only 1 allowed")  # throw value error

    def __getitem__(self, index: int) -> list[int]:
        return self.board[index]

    def __eq__(self, other) -> bool:
        if not isinstance(other, Board):
            return False

        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] != other.board[i][j]:
                    return False
        return True

    def get_legal_moves(self, player: int) -> list[((int, int), (int, int), (int, int))]:
        """
        Get all the legal moves for a player (-1 is black, 1 is white)
        :param player: int
        :return: all legal full moves
        """

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

    def get_moves_amazon(self, amazon: (int, int), player: int) -> list[(int, int)]:
        """
        Get the full moves for a certain amazon
        :param amazon: (int, int)
        :param player: int
        :return: full game of the amazons move for a player
        """

        moves = []

        for move in self.get_moves_position(amazon):  # Get the 'physical' moves
            self.board[amazon[0]][amazon[1]] = 0
            for shot in self.get_moves_position(move):  # For each 'physical' move get each arrow shot
                moves.append((amazon, move, shot))
            self.board[amazon[0]][amazon[1]] = player

        return moves

    def get_moves_position(self, position: (int, int)) -> list[(int, int)]:
        """
        Get the queen-like moves from a certain position
        :param position: (int, int)
        :return: amazon queen-like moves from the position
        """

        moves = []

        for direction in self.__directions:
            x = position[0] + direction[0]
            y = position[1] + direction[1]

            while self.n > x >= 0 and self.n > y >= 0 and self.board[x][y] == 0:
                moves.append((x, y))
                x += direction[0]
                y += direction[1]

        return moves

    def has_legal_moves(self, player: int) -> bool:
        """
        Returns True is the specified player has legal moves and False otherwise
        :param player: int
        :return: bool
        """

        if len(self.get_legal_moves(player)) > 0:
            return True
        else:
            return False

    def is_win(self, player: int) -> bool:
        """
        Returns True if the player has won, False otherwise
        :param player: int
        :return: bool
        """

        if not (self.has_legal_moves(-player)):
            return True
        else:
            return False

    def execute_move(self, move: ((int, int), (int, int), (int, int)), player: int) -> None:
        """
        Executes a full move on the board

        A move has the following elements:
        amazon: the piece that will be moved
        place: the tile where the piece will be moved
        shoot: the tile that will be shot by the amazon
        :param move: move to be executed
        :param player: player to move
        :return: None
        """

        if not self.is_valid_move(move):
            return

        (amazon, place, shoot) = move

        self.move_piece(amazon, place, player)

        self.shoot_arrow(shoot)

    def undo_move(self, move: ((int, int), (int, int), (int, int)), player: int) -> None:
        """
        Undoes a move, that is, leaves the board as if the move was never made
        :param move: move to undo
        :param player: player that made the move
        :return: None
        """

        if not self.is_valid_move(move):
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

    def is_valid_move(self, move: ((int, int), (int, int), (int, int)), player: int) -> bool:
        """
        Returns True if the specified move is valid and False otherwise
        :param move: move to be verified
        :param player: player that makes the move
        :return: bool
        """
        if not isinstance(move, tuple) or len(move) != 3:
            return False
        if type(player) is not int:
            return False
        if player != 1 and player != -1:
            return False

        initial_square, final_square, arrow = move

        if initial_square[0] >= self.n or initial_square[1] >= self.n or initial_square[0] < 0 or initial_square[1] < 0:
            return False
        if final_square[0] >= self.n or final_square[1] >= self.n or final_square[0] < 0 or final_square[1] < 0:
            return False
        if arrow[0] >= self.n or arrow[1] >= self.n or arrow[0] < 0 or arrow[1] < 0:
            return False

        if self.board[initial_square[0]][initial_square[1]] != player:
            return False
        if self.board[final_square[0]][final_square[1]] != 0:
            return False
        if self.board[arrow[0]][arrow[1]] != 0:
            return False

        return True

    def move_piece(self, amazon: (int, int), place: (int, int), player: int) -> None:
        """
        Moves a piece from one tile to another
        (note that this is not a full move, just a piece move without the shot)
        :param amazon: amazon to move
        :param place: square to move the amazon to
        :param player: player that moves the amazon
        :return: None
        """

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

    def shoot_arrow(self, shoot: (int, int)) -> None:
        """
        Blocks a tile from the board, that is the shooting part of a full move
        :param shoot: square to shoot
        :return: None
        """

        (x, y) = shoot

        self.board[x][y] = 2

    def print_board(self) -> None:
        """
        Prints the board xd
        :return: None
        """
        for i in range(self.n):
            for j in range(self.n):
                print(self.board[j][i], end="\t")
            print()
