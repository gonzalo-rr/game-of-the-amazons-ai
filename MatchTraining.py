import csv
import time

from amazons.AmazonsLogic import Board
from amazons.algorithms.RandomAlgorithm import RandomAlgorithm
from amazons.algorithms.GreedyAlgorithmMobility import GreedyAlgorithmMobility
from amazons.algorithms.GreedyAlgorithmTerritory import GreedyAlgorithmTerritory
from amazons.algorithms.MinimaxAlgorithmMobility import MinimaxAlgorithmMobility
from amazons.algorithms.MinimaxAlgorithmTerritory import MinimaxAlgorithmTerritory


def match_training(n_matches):
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