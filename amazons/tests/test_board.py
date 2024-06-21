import unittest

from amazons.logic.AmazonsLogic import Board


class BoardTest(unittest.TestCase):

    def test_init(self):
        coords_white = [(0, 6), (9, 6), (3, 9), (6, 9)]
        coords_black = [(3, 0), (6, 0), (0, 3), (9, 3)]

        # Created board
        board = Board()

        self.assertEqual(sorted(coords_white), sorted(board.white_positions))
        self.assertEqual(sorted(coords_black), sorted(board.black_positions))

        # Copied un-modified board
        board = Board()

        board_copy = Board(board)

        self.assertEqual(sorted(coords_white), sorted(board_copy.white_positions))
        self.assertEqual(sorted(coords_black), sorted(board_copy.black_positions))

        # Copied modified board
        board = Board()

        board_copy = Board(board)
        board_copy.execute_move(((0, 6), (1, 7), (2, 8)), 1)

        coords_white.remove((0, 6))
        coords_white.append((1, 7))

        self.assertEqual(sorted(coords_white), sorted(board_copy.white_positions))
        self.assertEqual(sorted(coords_black), sorted(board_copy.black_positions))

    def test_is_valid_move(self):
        board = Board()
        move = ((0, 6), (1, 7), (2, 8))  # Valid move for white player
        self.assertTrue(board.is_valid_move(move, 1))

        move = ((0, 3), (0, 4), (0, 5))  # Valid move for black player
        self.assertTrue(board.is_valid_move(move, -1))

        move = ("str", "str", "str")  # Invalid type move
        self.assertFalse(board.is_valid_move(move, -1))

        move = ((0, 6), (1, 7), (2, 8))  # Invalid type player
        self.assertFalse(board.is_valid_move(move, "1"))

        move = ((0, 6), (-1, 6), (-2, 5))  # Invalid coordinate < 0
        self.assertFalse(board.is_valid_move(move, 1))

        move = ((0, 6), (1, 7), (1, 10))  # Invalid coordinate > 9
        self.assertFalse(board.is_valid_move(move, 1))

        move = ((0, 0), (1, 7), (1, 10))  # Invalid coordinate (no amazon)
        self.assertFalse(board.is_valid_move(move, 1))

        board = Board()
        move = ((0, 6), (1, 8), (0, 6))  # Invalid coordinate (impossible move)
        self.assertFalse(board.is_valid_move(move, 1))

        move = ((0, 6), (1, 7), (2, 8))  # Invalid player number
        self.assertFalse(board.is_valid_move(move, 2))

        move = ((0, 6), (1, 7), (2, 8))  # Invalid move for black player
        self.assertFalse(board.is_valid_move(move, -1))

    def test_execute_move(self):
        board = Board()
        move = ((0, 6), (1, 7), (2, 8))  # Valid move for white player
        board.execute_move(move, 1)

        board = Board()
        move = ((0, 3), (0, 4), (0, 5))  # Valid move for black player
        board.execute_move(move, -1)

        board = Board()
        move = ("str", "str", "str")  # Invalid type move
        self.assertRaises(ValueError, board.execute_move, move, -1)

        board = Board()
        move = ((0, 6), (1, 7), (2, 8))  # Invalid type player
        self.assertRaises(ValueError, board.execute_move, move, "1")

        board = Board()
        move = ((0, 6), (-1, 6), (-2, 5))  # Invalid coordinate < 0
        self.assertRaises(ValueError, board.execute_move, move, 1)

        board = Board()
        move = ((0, 6), (1, 7), (1, 10))  # Invalid coordinate > 9
        self.assertRaises(ValueError, board.execute_move, move, 1)

        board = Board()
        move = ((0, 0), (1, 7), (1, 10))  # Invalid coordinate (no amazon)
        self.assertRaises(ValueError, board.execute_move, move, 1)

        board = Board()
        move = ((0, 6), (1, 8), (0, 6))  # Invalid coordinate (impossible move)
        self.assertRaises(ValueError, board.execute_move, move, 1)

        board = Board()
        move = ((0, 6), (1, 7), (2, 8))  # Invalid player number
        self.assertRaises(ValueError, board.execute_move, move, 2)

        board = Board()
        move = ((0, 6), (1, 7), (2, 8))  # Invalid move for black player
        self.assertRaises(ValueError, board.execute_move, move, -1)

    def test_undo_move(self):
        board = Board()
        move = ((0, 6), (1, 7), (2, 8))  # Valid move for white player
        board.execute_move(move, 1)
        board.undo_move(move, 1)

        board = Board()
        move = ((0, 3), (0, 4), (0, 5))  # Valid move for black player
        board.execute_move(move, -1)
        board.undo_move(move, -1)

        board = Board()
        move = ("str", "str", "str")  # Invalid type move
        self.assertRaises(ValueError, board.undo_move, move, -1)

        board = Board()
        move = ((0, 6), (1, 7), (2, 8))  # Invalid type player
        self.assertRaises(ValueError, board.undo_move, move, "1")

        board = Board()
        move = ((0, 6), (-1, 6), (-2, 5))  # Invalid coordinate < 0
        self.assertRaises(ValueError, board.undo_move, move, 1)

        board = Board()
        move = ((0, 6), (1, 7), (1, 10))  # Invalid coordinate > 9
        self.assertRaises(ValueError, board.undo_move, move, 1)

        board = Board()
        move = ((0, 0), (1, 7), (1, 10))  # Invalid coordinate (no amazon)
        self.assertRaises(ValueError, board.undo_move, move, 1)

        board = Board()
        move = ((0, 6), (1, 8), (0, 6))  # Invalid coordinate (impossible move)
        self.assertRaises(ValueError, board.undo_move, move, 1)

        board = Board()
        move = ((0, 6), (1, 7), (2, 8))  # Invalid player number
        self.assertRaises(ValueError, board.undo_move, move, 2)

        board = Board()
        move = ((0, 6), (1, 7), (2, 8))  # Invalid move for black player
        self.assertRaises(ValueError, board.undo_move, move, -1)

    def test_eq(self):
        mod_board1 = Board()
        mod_board1.board = [[i for i in range(10)] for _ in range(10)]

        mod_board2 = Board()
        mod_board2.white_positions = [j for j in range(4)]
        mod_board2.black_positions = [j for j in range(4, 8)]

        mod_board3 = Board()
        mod_board3.board = [[i for i in range(10)] for _ in range(10)]
        mod_board3.white_positions = [j for j in range(4)]
        mod_board3.black_positions = [j for j in range(4, 8)]

        std_board = Board()

        self.assertFalse(std_board.__eq__(mod_board3))  # Both board and positions not equal
        self.assertFalse(std_board.__eq__(mod_board2))  # Only positions not equal
        self.assertFalse(std_board.__eq__(mod_board1))  # Only board not equal
        self.assertTrue(std_board.__eq__(Board()))  # Equal boards

    def test_get_legal_moves(self):
        # 0 legal moves
        board = Board()
        board.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 2, -1, -1, -1, -1],
        ]
        board.white_positions = [(8, 9), (8, 8), (8, 7), (8, 6)]
        board.black_positions = [(9, 9), (9, 8), (9, 7), (9, 6)]
        self.assertEqual(board.get_legal_moves(-1), [])

        # 1 legal move
        board = Board()
        board.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 2, 1, 1, 1, 1],
            [0, 0, 0, 0, 2, 0, -1, -1, -1, -1],
        ]
        board.white_positions = [(8, 9), (8, 8), (8, 7), (8, 6)]
        board.black_positions = [(9, 9), (9, 8), (9, 7), (9, 6)]
        self.assertEqual(sorted(board.get_legal_moves(-1)), sorted([((9, 6), (9, 5), (9, 6))]))

        # 2 legal moves
        board = Board()
        board.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 2, 2, 0, 0, 2, 1, 1, 1, 1],
            [-1, 0, 2, 0, 0, 2, 0, -1, -1, -1],
        ]
        board.white_positions = [(8, 9), (8, 8), (8, 7), (8, 6)]
        board.black_positions = [(9, 9), (9, 8), (9, 7), (9, 0)]
        self.assertEqual(sorted(board.get_legal_moves(-1)), sorted([((9, 7), (9, 6), (9, 7)),
                                                                    ((9, 0), (9, 1), (9, 0))]))

    def test_is_win(self):
        board = Board()
        self.assertRaises(TypeError, board.is_win, "str")  # Error type player

        board = Board()
        self.assertRaises(ValueError, board.is_win, 0)  # Error number player

        board = Board()
        self.assertFalse(board.is_win(1))  # Not a win for any, check for white

        board = Board()
        self.assertFalse(board.is_win(-1))  # Not a win for any, check for black

        board = Board()
        board.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 2, -1, -1, -1, -1],
        ]
        board.white_positions = [(8, 9), (8, 8), (8, 7), (8, 6)]
        board.black_positions = [(9, 9), (9, 8), (9, 7), (9, 6)]
        self.assertTrue(board.is_win(1))  # Win for white, check for white

        board = Board()
        board.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 2, -1, -1, -1, -1],
        ]
        board.white_positions = [(8, 9), (8, 8), (8, 7), (8, 6)]
        board.black_positions = [(9, 9), (9, 8), (9, 7), (9, 6)]
        self.assertFalse(board.is_win(-1))  # Win for white, check for black

        board = Board()
        board.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, 2, 1, 1, 1, 1],
        ]
        board.black_positions = [(8, 9), (8, 8), (8, 7), (8, 6)]
        board.white_positions = [(9, 9), (9, 8), (9, 7), (9, 6)]
        self.assertFalse(board.is_win(1))  # Win for black, check for white

        board = Board()
        board.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, 2, 1, 1, 1, 1],
        ]
        board.black_positions = [(8, 9), (8, 8), (8, 7), (8, 6)]
        board.white_positions = [(9, 9), (9, 8), (9, 7), (9, 6)]
        self.assertTrue(board.is_win(-1))  # Win for black, check for black


if __name__ == '__main__':
    unittest.main()
