import time
from copy import copy, deepcopy

import pygame

from amazons.AmazonsLogic import Board
from amazons.algorithms import RandomAlgorithm, GreedyAlgorithm, MinimaxAlgorithm
from amazons.algorithms.MinimaxAlgorithmMultiProcess import MinimaxAlgorithmMultiProcess
from amazons.assets.HistoryTable import HistoryTable
from ui.GameGUI import GameGUI
import multiprocessing as mp


def main():
    # calculate_copy_times()

    run_gui()

    # match_training()

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
    gameGUI = GameGUI(tile_size)

    gameGUI.run()


def match_training():
    white = GreedyAlgorithm
    minimax = MinimaxAlgorithmMultiProcess(3, 10, 6)
    black = minimax

    total_matches = 10
    wins_white = 0
    wins_black = 0
    n_moves = 0

    for game in range(total_matches):
        board = Board()
        playing = True
        while playing:
            if board.is_win(1):
                wins_white += 1
                break
            elif board.is_win(-1):
                wins_black += 1
                break

            white_move = white.make_move(board, 1)
            board.execute_move(white_move, 1)
            n_moves += 1
            # board.print_board()

            if board.is_win(1):
                wins_white += 1
                break
            elif board.is_win(-1):
                wins_black += 1
                break

            black_move = black.make_move(board, -1)
            board.execute_move(black_move, -1)
            n_moves += 1
            # board.print_board()

    print("Wins by white: " + str(wins_white))
    print("Wins by black: " + str(wins_black))


if __name__ == "__main__":
    main()
