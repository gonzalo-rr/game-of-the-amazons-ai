import time
from copy import copy, deepcopy

import pygame

from amazons.AmazonsLogic import Board
from amazons.algorithms import RandomAlgorithm, GreedyAlgorithm
from ui.GameGUI import GameGUI


def main():
    # start = time.time_ns()
    #
    # board = Board()
    #
    # n_times = 1000
    #
    # for i in range(n_times):
    #     new_board = deepcopy(board)
    #
    # end = time.time_ns()
    #
    # print("Deepcopy = " + str(end - start) + " ns")
    #
    # start = time.time_ns()
    #
    # for i in range(n_times):
    #     new_board = Board(board)
    #
    # end = time.time_ns()
    #
    # print("Copy columns = " + str(end - start) + " ns")
    #
    # move = ((0, 6), (1, 6), (2, 6))
    # player = 1
    #
    # start = time.time_ns()
    #
    # for i in range(n_times):
    #     board.execute_move(move, player)
    #     board.undo_move(move, player)
    #
    # end = time.time_ns()
    #
    # print("Undo move = " + str(end - start) + " ns")

    # Basic configuration
    pygame.init()

    width = 1_000
    height = 1_000
    tile_size = 100
    gameGUI = GameGUI(width, height, tile_size)

    gameGUI.run()

    # white = RandomAlgorithm
    # black = GreedyAlgorithm
    #
    # total_matches = 100
    # wins_white = 0
    # wins_black = 0
    #
    # for game in range(total_matches):
    #     board = Board()
    #     playing = True
    #     while playing:
    #         white_move = white.make_move(board, 1)
    #         board.execute_move(white_move, 1)
    #         black_move = black.make_move(board, -1)
    #         board.execute_move(black_move, -1)
    #         if board.is_win(1):
    #             playing = False
    #             wins_white += 1
    #         elif board.is_win(-1):
    #             playing = False
    #             wins_black += 1
    #
    # print("Wins by white: " + str(wins_white))
    # print("Wins by black: " + str(wins_black))


if __name__ == "__main__":
    main()
