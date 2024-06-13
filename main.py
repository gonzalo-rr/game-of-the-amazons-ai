import time
from copy import deepcopy

import pygame

from amazons.test import MatchTraining
from amazons.logic.AmazonsLogic import Board
from amazons.algorithms.RandomAlgorithm import RandomAlgorithm
from amazons.algorithms.greedy.GreedyAlgorithmMobility import GreedyAlgorithmMobility
from amazons.algorithms.minimax.MinimaxAlgorithmTerritory import MinimaxAlgorithmTerritory

from ui.GameGUI import GameGUI
import multiprocessing as mp


def main():
    # mcts = MCTSAlgorithm(10)
    # b = Board(False)
    # mcts.make_move(b, 1)

    # node = Node(b, 1)
    # node.expand()
    # print(len(node.children))

    # board = Board(False)
    # board.board = [
    #      [0, 0, 0, -1, 0, 0, 1, 0, 0, 0],
    #      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #      [-1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #      [0, 0, 0, 0, 2, 2, 2, 0, 0, 0],
    #      [0, 0, 0, 0, 2, 0, 2, 0, 0, 0],
    #      [-1, 0, 0, 0, 2, 2, 2, 0, 0, 1],
    #      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #      [0, 0, 0, -1, 0, 0, 1, 0, 0, 0]
    #      ]
    # # print(len(board.get_legal_moves(-1)))
    # # board.white_positions = [(0, 6), (9, 6), (3, 9), (6, 9)]
    # # board.black_positions = [(3, 0), (6, 0), (0, 3), (9, 3)]
    # # print(len(board.get_legal_moves(-1)))
    #
    # eval2 = MinimaxAlgorithm.evaluate_territory2(board)
    # print("Eval", eval2)

    # board = Board(False)
    # # board.print_board()
    # print()
    # start = time.time()
    # eval2 = MinimaxAlgorithm.evaluate_territory2(board)
    # end = time.time()
    # print('New way:', end - start, eval2)
    # start = time.time()
    # eval1 = MinimaxAlgorithm.evaluate_territory1(board)
    # end = time.time()
    # print('Old way:', end - start, eval1)

    # calculate_copy_times()

    run_gui()

    # calculate_king_moves(Board(False))
    # b = Board(False)
    # b.board = [
    #     [0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
    #     [0, 0, 0, 0, 2, 0, 0, 2, 0, 0],
    #     [0, 0, 0, 1, 0, -1, 0, 0, 0, 0],
    #     [0, 0, 2, 2, 0, -1, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 2, 0, 0, 0, 2, 0],
    #     [0, 2, -1, 2, 0, 2, 2, 2, 2, 2],
    #     [0, 0, 0, 0, 0, 2, 1, 1, 2, 0],
    #     [0, 0, 0, 1, 2, 2, 0, 2, 0, 0],
    #     [0, 2, -1, 0, 0, 2, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
    #      ]
    # b.white_positions = [(2,3),(6,6),(6,7),(7,3)]
    # b.black_positions = [(2,5), (3,5), (5,2), (8,2)]
    # b.print_board()
    # print()
    # _, bw, bb = evaluate_territory(b)
    # evaluate_individual_mobility(b, bw, bb)

    # n_matches = 100
    # MatchTraining.match_training(n_matches)

    # test_parallelization()

    # Check history table ratings
    # h = HistoryTable()
    # h.load_table()
    # b = Board(False)
    # moves = b.get_legal_moves(1)
    # for move in moves:
    #     rating = h.get_rating(move)
    #     if rating > 0:
    #         print(rating)

    # b = Board(False)
    # move = RandomAlgorithm.make_move(b, 1)
    # b.execute_move(((3, 9), (4, 8), (5, 7)), 1)
    # b.print_board()
    # print()
    # MinimaxAlgorithm.evaluate_territory(b)


def test_parallelization():
    # global x

    # start = time.time()
    # calculation(4)
    # calculation(4)
    # end = time.time()
    # print(end - start, " secs no paralelo", x)

    x = mp.Array('i', 2)

    start = time.time()
    process1 = mp.Process(target=calculation, args=(4, 0, x))
    process2 = mp.Process(target=calculation, args=(4, 1, x))
    process1.start()
    process2.start()
    process1.join()
    process2.join()
    end = time.time()
    print(end - start, " secs paralelo", x[:])


def calculation(secs, pid, array):
    array[pid] = pid
    time.sleep(secs)


def calculate_copy_times():
    start = time.time_ns()

    board = Board()

    n_times = 1000

    for i in range(n_times):
        new_board = deepcopy(board)

    end = time.time_ns()

    print("Deepcopy = " + str(end - start) + " ns")

    start = time.time_ns()

    for i in range(n_times):
        new_board = Board(board)

    end = time.time_ns()

    print("Copy columns = " + str(end - start) + " ns")

    move = ((0, 6), (1, 6), (2, 6))
    player = 1

    start = time.time_ns()

    for i in range(n_times):
        board.execute_move(move, player)
        board.undo_move(move, player)

    end = time.time_ns()

    print("Undo move = " + str(end - start) + " ns")


def run_gui():
    # Basic configuration
    pygame.init()

    tile_size = 100
    algorithms = [
        RandomAlgorithm(),
        GreedyAlgorithmMobility(),
        MinimaxAlgorithmTerritory(2, 5),
    ]

    gameGUI = GameGUI(tile_size, algorithms)

    gameGUI.run()


if __name__ == "__main__":
    main()
