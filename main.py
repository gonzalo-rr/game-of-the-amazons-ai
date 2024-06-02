import time
from copy import copy, deepcopy

import pygame

from amazons.AmazonsLogic import Board
from amazons.algorithms.MCTSAlgorithm import MCTSAlgorithm
from amazons.algorithms.MinimaxAlgorithmTerritoryMobility import *
from amazons.algorithms.RandomAlgorithm import RandomAlgorithm
from amazons.algorithms.GreedyAlgorithmMobility import GreedyAlgorithmMobility
from amazons.algorithms.GreedyAlgorithmTerritory import GreedyAlgorithmTerritory
from amazons.algorithms.MinimaxAlgorithmTerritory import MinimaxAlgorithmTerritory
from amazons.algorithms.MinimaxAlgorithmMobility import MinimaxAlgorithmMobility
from amazons.algorithms.MinimaxAlgorithmMultiProcess import MinimaxAlgorithmMultiProcess
from amazons.algorithms.mcts_tree.Node import Node
from ui.GameGUI import GameGUI
import multiprocessing as mp
import csv


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


def match_training():
    n_matches = 2

    # First set of games: greedy (territory) vs greedy (mobility)

    p1 = GreedyAlgorithmTerritory()
    p2 = GreedyAlgorithmMobility()
    play_n_games(p1, p2, n_matches, 'resultsGreedy.csv')

    # Second set of games: minimax (mobility) vs minimax (territory) recursion limit 1

    p1 = MinimaxAlgorithmMobility(1, 10)
    p2 = MinimaxAlgorithmTerritory(1, 10)
    play_n_games(p1, p2, n_matches, 'resultsMinimax1rec.csv')

    # Second set of games: minimax (mobility) vs minimax (territory) recursion limit 3

    p1 = MinimaxAlgorithmMobility(3, 5)
    p2 = MinimaxAlgorithmTerritory(3, 5)
    play_n_games(p1, p2, n_matches, 'resultsMinimax3rec.csv')

    # Second set of games: minimax (mobility) vs minimax (territory) recursion limit 5

    p1 = MinimaxAlgorithmMobility(5, 5)
    p2 = MinimaxAlgorithmTerritory(5, 5)
    play_n_games(p1, p2, n_matches, 'resultsMinimax5rec.csv')

    # Third set of games: greedy (mobility) vs greedy (territory)

    # p1 =
    # p2 =

    # Fourth set of games: greedy vs minimax (mobility)


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

    results = [white, black, result, end-start, n_moves_white, n_moves_black, avg_move_time_white, avg_move_time_black]
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
