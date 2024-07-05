import os.path
import sys
import time
from copy import deepcopy

import pygame

from amazons.algorithms.minimax.minimax_algorithm import *
from amazons.algorithms.minimax.minimax_algorithm_mobility import MinimaxAlgorithmMobility
from amazons.logic.amazons_logic import Board
from amazons.tests.match_training import match_training
from assets.utilities import conf_file_reader

from ui.game_gui import GameGUI
import multiprocessing as mp

"""
File that contains the main function of the system

Author: Gonzalo Rodríguez Rodríguez
"""


def main():
    # Check if arguments are correct
    args = sys.argv[1:]
    if len(args) > 2:
        raise ValueError("too many arguments")

    # Check mode
    mode = 'graphic'

    if len(args) != 0:
        mode = args[0]
        if mode == '-t' or mode == '--training':
            mode = 'training'
        elif mode == '-g' or mode == '--graphic':
            mode = 'graphic'
        else:
            raise ValueError(f"unsupported mode {mode}, possible modes: -g, -t")

    # Check additional file
    file = ''
    if len(args) == 2:
        file = args[1]
        if not os.path.isfile(file):
            raise ValueError(f"file {file} does not exist")

    # Execute
    if mode == 'training':
        train_ais(file)
    elif mode == 'graphic':
        run_gui(file)


def compare_for_tests():
    b = Board()
    p1 = MinimaxAlgorithmMobility(2, 10)
    start = time.time()
    p1.make_move(b, 1)
    end = time.time()
    print(f"Time taken: {end - start}")


def test_parallelization():
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
    """
    Function to compare copy times of the board
    :return: None
    """
    start = time.time_ns()

    board = Board(False)

    n_times = 1000

    for i in range(n_times):
        new_board = deepcopy(board)

    end = time.time_ns()

    print("Deepcopy = " + str(end - start) + " ns")

    start = time.time_ns()

    for i in range(n_times):
        new_board = [[] for _ in range(board.n)]
        for col in range(len(board.board)):
            new_board[col] = copy(board.board[col])
        b = Board(False)
        b.board = new_board

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


def run_gui(file: str) -> None:  # 5
    """
    Function to run the interface
    :param file: file with the algorithms
    :return: None
    """
    if file == '':
        file = './gui_conf.txt'
    algorithms = conf_file_reader.read_gui_file(file)

    # Basic configuration
    pygame.init()
    info = pygame.display.Info()
    tile_size = info.current_w // 25

    gameGUI = GameGUI(tile_size, algorithms)

    gameGUI.run()


def train_ais(file: str) -> None:
    """
    Function to run the training
    :param file: file with the parameters of training
    :return: None
    """
    if file == '':
        file = './training_conf.txt'
    matches = conf_file_reader.read_training_file(file)

    match_training(matches)


if __name__ == "__main__":
    main()
