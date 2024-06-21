import unittest

from amazons.algorithms.RandomAlgorithm import RandomAlgorithm
from amazons.algorithms.greedy.GreedyAlgorithmMobility import GreedyAlgorithmMobility
from amazons.algorithms.greedy.GreedyAlgorithmTerritory import GreedyAlgorithmTerritory
from amazons.algorithms.mcts.MCTSAlgorithmEGreedy import MCTSAlgorithmE
from amazons.algorithms.mcts.MCTSAlgorithmEGreedyMod import MCTSAlgorithmEMod
from amazons.algorithms.mcts.MCTSAlgorithmUCB import MCTSAlgorithmUCB
from amazons.algorithms.mcts.MCTSAlgorithmUCB_cut import MCTSAlgorithmCut
from amazons.algorithms.minimax.MinimaxAlgorithmMobility import MinimaxAlgorithmMobility
from amazons.algorithms.minimax.MinimaxAlgorithmRelativeTerritory import MinimaxAlgorithmRelativeTerritory
from amazons.algorithms.minimax.MinimaxAlgorithmTerritory import MinimaxAlgorithmTerritory
from amazons.algorithms.minimax.MinimaxAlgorithmTerritoryMobility import MinimaxAlgorithmTerritoryMobility
from amazons.logic.AmazonsLogic import Board


class AlgorithmsTest(unittest.TestCase):

    def test_make_move(self):
        algorithms = [
            RandomAlgorithm(),
            GreedyAlgorithmMobility(),
            GreedyAlgorithmTerritory(),
            MinimaxAlgorithmMobility(1, 1),
            MinimaxAlgorithmTerritory(1, 1),
            MinimaxAlgorithmRelativeTerritory(1, 1),
            MinimaxAlgorithmTerritoryMobility(1, 1),
            MCTSAlgorithmUCB(1, 1),
            MCTSAlgorithmCut(1, 1),
            MCTSAlgorithmE(1, 1),
            MCTSAlgorithmEMod(1, 1)
        ]

        # 0 legal moves white
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
        board.white_positions = [(9, 9), (9, 8), (9, 7), (9, 6)]
        board.black_positions = [(8, 9), (8, 8), (8, 7), (8, 6)]
        for algorithm in algorithms:
            self.assertRaises(ValueError, algorithm.make_move, board, 1)

        # 0 legal moves black
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
        for algorithm in algorithms:
            self.assertRaises(ValueError, algorithm.make_move, board, -1)

        # 1 legal move white
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
            [0, 0, 0, 0, 2, 2, -1, -1, -1, -1],
            [0, 0, 0, 0, 2, 0, 1, 1, 1, 1],
        ]
        board.white_positions = [(9, 9), (9, 8), (9, 7), (9, 6)]
        board.black_positions = [(8, 9), (8, 8), (8, 7), (8, 6)]
        for algorithm in algorithms:
            self.assertEqual(algorithm.make_move(board, 1), ((9, 6), (9, 5), (9, 6)))

        # 1 legal move black
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
        for algorithm in algorithms:
            self.assertEqual(algorithm.make_move(board, -1), ((9, 6), (9, 5), (9, 6)))

        # 2176 legal moves white
        board = Board()
        for algorithm in algorithms:
            move = algorithm.make_move(board, 1)
            self.assertIsNotNone(move)
            self.assertTrue(board.is_valid_move(move, 1))

        # 1214 legal moves black
        board = Board()
        board.print_board()
        move = ((3, 9), (3, 3), (6, 3))
        board.execute_move(move, 1)
        for algorithm in algorithms:
            move = algorithm.make_move(board, -1)
            self.assertIsNotNone(move)
            self.assertTrue(board.is_valid_move(move, -1))


if __name__ == '__main__':
    unittest.main()
