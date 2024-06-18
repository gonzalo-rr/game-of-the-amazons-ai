import unittest

from amazons.logic.AmazonsLogic import Board


class MyTestCase(unittest.TestCase):

    def test_valid_move(self):
        board = Board()
        move = ((0, 6), (1, 7), (2, 8))  # Valid move for white player
        self.assertTrue(board.is_valid_move(move, 1))

        move = ((0, 3), (0, 4), (0, 5))  # Valid move for black player
        self.assertTrue(board.is_valid_move(move, -1))

        move = "((0, 3), (0, 4), (0, 5))"  # Invalid type move
        self.assertFalse(board.is_valid_move(move, -1))

        move = ((0, 6), (1, 7), (2, 8))  # Invalid type player
        self.assertFalse(board.is_valid_move(move, "1"))

        move = ((0, 6), (-1, 6), (-2, 5))  # Invalid coordinate < 0
        self.assertFalse(board.is_valid_move(move, 1))

        move = ((0, 6), (1, 7), (1, 10))  # Invalid coordinate > 9
        self.assertFalse(board.is_valid_move(move, 1))

        move = ((0, 0), (1, 7), (1, 10))  # Invalid coordinate (no amazon)
        self.assertFalse(board.is_valid_move(move, 1))

        move = ((0, 6), (1, 7), (2, 8))  # Invalid player number
        self.assertFalse(board.is_valid_move(move, 2))

        move = ((0, 6), (1, 7), (2, 8))  # Invalid move for black player
        self.assertFalse(board.is_valid_move(move, -1))


if __name__ == '__main__':
    unittest.main()
