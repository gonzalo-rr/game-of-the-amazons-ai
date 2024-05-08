import time
from copy import copy, deepcopy

import pygame

from amazons.AmazonsLogic import Board
from amazons.algorithms.RandomAlgorithm import RandomAlgorithm
from amazons.algorithms.GreedyAlgorithmMobility import GreedyAlgorithmMobility
from amazons.algorithms.MinimaxAlgorithmRelativeTerritory5 import MinimaxAlgorithmRelativeTerritory5
from amazons.algorithms.MinimaxAlgorithmRelativeTerritory import MinimaxAlgorithmRelativeTerritory
from amazons.algorithms.MinimaxAlgorithmMobility import MinimaxAlgorithmMobility
from amazons.algorithms.MinimaxAlgorithmMultiProcess import MinimaxAlgorithmMultiProcess
from amazons.assets.HistoryTable import HistoryTable
from ui.GameGUI import GameGUI
import multiprocessing as mp
import csv


def main():
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

    # run_gui()

    matches = []
    n_matches = 100

    # greedyRTerritory10 = GreedyAlgorithmRelativeTerritory()
    # greedyTerritory = GreedyAlgorithmMobility()
    #
    # matches.append(
    #     (greedyRTerritory10, greedyTerritory, 'Game1')
    # )
    #
    # minimaxMobility1 = MinimaxAlgorithmMobility(1, 10)
    # minimaxRTerritory1 = MinimaxAlgorithmRelativeTerritory(1, 10)
    #
    # matches.append(
    #     (minimaxMobility1, minimaxRTerritory1, 'Game2')
    # )
    #
    # minimaxMobility3 = MinimaxAlgorithmMobility(3, 5)
    # minimaxRTerritory3 = MinimaxAlgorithmRelativeTerritory(3, 5)
    #
    # matches.append(
    #     (minimaxMobility3, minimaxRTerritory3, 'Game3')
    # )
    #
    # minimaxMobility5 = MinimaxAlgorithmMobility(5, 5)
    # minimaxRTerritory5 = MinimaxAlgorithmRelativeTerritory(5, 5)
    #
    # matches.append(
    #     (minimaxMobility5, minimaxRTerritory5, 'Game4')
    # )

    # Minimax Relative Territory 5 vs Minimax Relative Territory 10
    minimaxRTerritory5 = MinimaxAlgorithmRelativeTerritory5(2, 10)
    minimaxRTerritory10 = MinimaxAlgorithmRelativeTerritory(2, 10)

    matches.append(
        (minimaxRTerritory5, minimaxRTerritory10, 'MinimaxRT5VMinimaxRT10.csv')
    )

    match_training(matches, n_matches)

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
    gameGUI = GameGUI(tile_size)

    gameGUI.run()


def match_training(matches, n_matches):
    for match in matches:
        player1 = match[0]
        player2 = match[1]
        name = match[2]

        play_n_games(player1, player2, n_matches, name)


def play_n_games(p1, p2, n_matches, name):
    full_results = []  # Each element is the results of a single game

    for game in range(n_matches // 2):
        results = play_game(p1, p2)
        full_results.append(results)

    for game in range(n_matches // 2):
        results = play_game(p2, p1)
        full_results.append(results)

    update_csv(full_results, name)


# [white, black, result, total_time, n_moves_w, n_moves_b, avg_move_time_white, avg_move_time_black]
def play_game(white, black):
    result = 0
    avg_move_time_white = 0
    avg_move_time_black = 0

    wins_white = 0
    wins_black = 0
    n_moves_white = 0
    n_moves_black = 0

    board = Board(False)
    playing = True
    start = time.time()
    while playing:
        if board.is_win(1):
            wins_white += 1
            result = 1
            break
        elif board.is_win(-1):
            wins_black += 1
            result = -1
            break

        s = time.time()
        white_move = white.make_move(board, 1)
        e = time.time()
        print('White move:', white_move)
        board.execute_move(white_move, 1)
        avg_move_time_white = (n_moves_white * avg_move_time_white + (e - s)) / (n_moves_white + 1)
        n_moves_white += 1

        if board.is_win(1):
            wins_white += 1
            result = 1
            break
        elif board.is_win(-1):
            wins_black += 1
            result = -1
            break

        s = time.time()
        black_move = black.make_move(board, -1)
        e = time.time()
        print('Black move:', black_move)
        board.execute_move(black_move, -1)
        avg_move_time_black = (n_moves_black * avg_move_time_black + (e - s)) / (n_moves_black + 1)
        n_moves_black += 1

    end = time.time()
    print('Game finished')

    results = [white, black, result, end - start, n_moves_white, n_moves_black, avg_move_time_white,
               avg_move_time_black]
    return results


# white, black, result, total_time, n_moves_w, n_moves_b, avg_move_time_white, avg_move_time_black:
def update_csv(results, name):
    with open(name, 'w', newline='\n') as file:
        w = csv.writer(file, delimiter=';')
        w.writerow(
            ['white', 'black', 'result', 'total_time', 'n_moves_white', 'n_moves_black', 'avg_move_time_white',
             'avg_move_time_black'])
        for row in results:
            w.writerow(row)


if __name__ == "__main__":
    main()
