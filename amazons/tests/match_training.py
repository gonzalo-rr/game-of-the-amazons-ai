import csv
import time

from amazons.algorithms.algorithm import Algorithm
from amazons.logic.amazons_logic import Board
from amazons.algorithms.random_algorithm import RandomAlgorithm
from amazons.algorithms.greedy.greedy_algorithm_territory import GreedyAlgorithmTerritory
from amazons.algorithms.mcts.mcts_algorithm_e_greedy import MCTSAlgorithmE
from amazons.algorithms.mcts.mcts_algorithm_ucb import MCTSAlgorithmUCB
from amazons.algorithms.mcts.mcts_algorithm_ucb_cut import MCTSAlgorithmCut
from amazons.algorithms.minimax.minimax_algorithm_mobility import MinimaxAlgorithmMobility
from amazons.algorithms.minimax.minimax_algorithm_relative_territory import MinimaxAlgorithmRelativeTerritory
from amazons.algorithms.minimax.minimax_algorithm_territory import MinimaxAlgorithmTerritory
from amazons.algorithms.minimax.minimax_algorithm_territory_mobility import MinimaxAlgorithmTerritoryMobility
from assets.utilities.match_recorder import MatchRecorder

"""
Script to train the algorithms by comparing them with simulated matches between them

Author: Gonzalo Rodríguez Rodríguez
"""


def match_training(n_matches: int) -> None:
    """
    Main function to start the training
    :param n_matches: number of matches for each set, each set consists of 2 algorithms playing against each other
    :return: None
    """
    match_recorder = MatchRecorder()

    # # Set 1
    # p1 = GreedyAlgorithmMobility()
    # p2 = RandomAlgorithm()
    # play_n_games(p1, p2, n_matches, 'resGMvR.csv')
    # match_recorder.save_results('resGMvR.pkl')
    #
    # # Set 2
    # p1 = GreedyAlgorithmTerritory()
    # p2 = RandomAlgorithm()
    # play_n_games(p1, p2, n_matches, 'resGTvR.csv')
    # match_recorder.save_results('resGTvR.pkl')
    #
    # # Set 3
    #
    # p1 = GreedyAlgorithmTerritory()
    # p2 = GreedyAlgorithmMobility()
    # play_n_games(p1, p2, n_matches, 'resGMvGT.csv')
    # match_recorder.save_results('resGMvGT.pkl')

    # Set 1: Minimax Mobility rec 2 & 3 vs Random & Greedy Territory

    p1 = MinimaxAlgorithmMobility(2, 10)
    p2 = RandomAlgorithm()
    play_n_games(p1, p2, n_matches, 'resMM2vR.csv')
    match_recorder.save_results('resMM2vR.pkl')

    p1 = MinimaxAlgorithmMobility(3, 10)
    p2 = RandomAlgorithm()
    play_n_games(p1, p2, n_matches, 'resMM3vR.csv')
    match_recorder.save_results('resMM3vR.pkl')

    p1 = MinimaxAlgorithmMobility(2, 10)
    p2 = GreedyAlgorithmTerritory()
    play_n_games(p1, p2, n_matches, 'resMM2vGT.csv')
    match_recorder.save_results('resMM2vGT.pkl')

    p1 = MinimaxAlgorithmMobility(3, 10)
    p2 = GreedyAlgorithmTerritory()
    play_n_games(p1, p2, n_matches, 'resMM3vGT.csv')
    match_recorder.save_results('resMM3vGT.pkl')

    # Set 2: Minimax Territory rec 2 & 3 vs Random & Greedy Territory

    p1 = MinimaxAlgorithmTerritory(2, 10)
    p2 = RandomAlgorithm()
    play_n_games(p1, p2, n_matches, 'resMT2vR.csv')
    match_recorder.save_results('resMT2vR.pkl')

    p1 = MinimaxAlgorithmTerritory(3, 10)
    p2 = RandomAlgorithm()
    play_n_games(p1, p2, n_matches, 'resMT3vR.csv')
    match_recorder.save_results('resMT3vR.pkl')

    p1 = MinimaxAlgorithmTerritory(2, 10)
    p2 = GreedyAlgorithmTerritory()
    play_n_games(p1, p2, n_matches, 'resMT2vGT.csv')
    match_recorder.save_results('resMT2vGT.pkl')

    p1 = MinimaxAlgorithmTerritory(3, 10)
    p2 = GreedyAlgorithmTerritory()
    play_n_games(p1, p2, n_matches, 'resMT3vGT.csv')
    match_recorder.save_results('resMT3vGT.pkl')

    # Set 3: Minimax Relative Territory rec 2 & 3 vs Random & Greedy Territory

    p1 = MinimaxAlgorithmRelativeTerritory(2, 10)
    p2 = RandomAlgorithm()
    play_n_games(p1, p2, n_matches, 'resMRT2vR.csv')
    match_recorder.save_results('resMRT2vR.pkl')

    p1 = MinimaxAlgorithmRelativeTerritory(3, 10)
    p2 = RandomAlgorithm()
    play_n_games(p1, p2, n_matches, 'resMRT3vR.csv')
    match_recorder.save_results('resMRT3vR.pkl')

    p1 = MinimaxAlgorithmRelativeTerritory(2, 10)
    p2 = GreedyAlgorithmTerritory()
    play_n_games(p1, p2, n_matches, 'resMRT2vGT.csv')
    match_recorder.save_results('resMT2vGT.pkl')

    p1 = MinimaxAlgorithmRelativeTerritory(3, 10)
    p2 = GreedyAlgorithmTerritory()
    play_n_games(p1, p2, n_matches, 'resMRT3vGT.csv')
    match_recorder.save_results('resMT3vGT.pkl')

    # Set 4: Minimax Territory Mobility rec 2 & 3 vs Random & Greedy Territory

    p1 = MinimaxAlgorithmTerritoryMobility(2, 10)
    p2 = RandomAlgorithm()
    play_n_games(p1, p2, n_matches, 'resMTM2vR.csv')
    match_recorder.save_results('resMTM2vR.pkl')

    p1 = MinimaxAlgorithmTerritoryMobility(3, 10)
    p2 = RandomAlgorithm()
    play_n_games(p1, p2, n_matches, 'resMTM3vR.csv')
    match_recorder.save_results('resMTM3vR.pkl')

    p1 = MinimaxAlgorithmTerritoryMobility(2, 10)
    p2 = GreedyAlgorithmTerritory()
    play_n_games(p1, p2, n_matches, 'resMTM2vGT.csv')
    match_recorder.save_results('resMTM2vGT.pkl')

    p1 = MinimaxAlgorithmTerritoryMobility(3, 10)
    p2 = GreedyAlgorithmTerritory()
    play_n_games(p1, p2, n_matches, 'resMTM3vGT.csv')
    match_recorder.save_results('resMTM3vGT.pkl')

    # Set 5: MCTS sim 1000 & 5000 vs Random & Greedy Territory

    p1 = MCTSAlgorithmUCB(1000, 10)
    p2 = RandomAlgorithm()
    play_n_games(p1, p2, n_matches, 'resMCTS1vR.csv')
    match_recorder.save_results('resMCTS1vR.pkl')

    p1 = MCTSAlgorithmUCB(1000, 10)
    p2 = GreedyAlgorithmTerritory()
    play_n_games(p1, p2, n_matches, 'resMCTS1vGT.csv')
    match_recorder.save_results('resMCTS1vGT.pkl')

    p1 = MCTSAlgorithmUCB(5000, 10)
    p2 = RandomAlgorithm()
    play_n_games(p1, p2, n_matches, 'resMCTS5vR.csv')
    match_recorder.save_results('resMCTS5vR.pkl')

    p1 = MCTSAlgorithmUCB(5000, 10)
    p2 = GreedyAlgorithmTerritory()
    play_n_games(p1, p2, n_matches, 'resMCTS5vGT.csv')
    match_recorder.save_results('resMCTS5vGT.pkl')

    # Set 6: MCTS_cut sim 1000, 5000 vs Random & Greedy Territory

    p1 = MCTSAlgorithmCut(1000, 10)
    p2 = RandomAlgorithm()
    play_n_games(p1, p2, n_matches, 'resMCTSC1vR.csv')
    match_recorder.save_results('resMCTSC1vR.pkl')

    p1 = MCTSAlgorithmCut(1000, 10)
    p2 = GreedyAlgorithmTerritory()
    play_n_games(p1, p2, n_matches, 'resMCTSC1vGT.csv')
    match_recorder.save_results('resMCTSC1vGT.pkl')

    p1 = MCTSAlgorithmCut(5000, 10)
    p2 = RandomAlgorithm()
    play_n_games(p1, p2, n_matches, 'resMCTSC5vR.csv')
    match_recorder.save_results('resMCTSC5vR.pkl')

    p1 = MCTSAlgorithmCut(5000, 10)
    p2 = GreedyAlgorithmTerritory()
    play_n_games(p1, p2, n_matches, 'resMCTSC5vGT.csv')
    match_recorder.save_results('resMCTSC5vGT.pkl')

    # Set 7: MCTS-E sim 1000, 5000 vs Random & Greedy Territory

    p1 = MCTSAlgorithmE(1000, 10)
    p2 = RandomAlgorithm()
    play_n_games(p1, p2, n_matches, 'resMCTSE1vR.csv')
    match_recorder.save_results('resMCTSE1vR.pkl')

    p1 = MCTSAlgorithmE(1000, 10)
    p2 = GreedyAlgorithmTerritory()
    play_n_games(p1, p2, n_matches, 'resMCTSE1vGT.csv')
    match_recorder.save_results('resMCTSE1vGT.pkl')

    p1 = MCTSAlgorithmE(5000, 10)
    p2 = RandomAlgorithm()
    play_n_games(p1, p2, n_matches, 'resMCTSE5vR.csv')
    match_recorder.save_results('resMCTSE5vR.pkl')

    p1 = MCTSAlgorithmE(5000, 10)
    p2 = GreedyAlgorithmTerritory()
    play_n_games(p1, p2, n_matches, 'resMCTSE5vGT.csv')
    match_recorder.save_results('resMCTSE5vGT.pkl')

    # Set 7: MCTS-E' sim 100, 1000, 10000 vs Random & Greedy Territory

    p1 = MCTSAlgorithmE(1000, 10)
    p2 = RandomAlgorithm()
    play_n_games(p1, p2, n_matches, 'resMCTSEm1vR.csv')
    match_recorder.save_results('resMCTSEm1vR.pkl')

    p1 = MCTSAlgorithmE(1000, 10)
    p2 = GreedyAlgorithmTerritory()
    play_n_games(p1, p2, n_matches, 'resMCTSEm1vGT.csv')
    match_recorder.save_results('resMCTSEm1vGT.pkl')

    p1 = MCTSAlgorithmE(5000, 10)
    p2 = RandomAlgorithm()
    play_n_games(p1, p2, n_matches, 'resMCTSEm5vR.csv')
    match_recorder.save_results('resMCTSEm5vR.pkl')

    p1 = MCTSAlgorithmE(5000, 10)
    p2 = GreedyAlgorithmTerritory()
    play_n_games(p1, p2, n_matches, 'resMCTSEm5vGT.csv')
    match_recorder.save_results('resMCTSEm5vGT.pkl')


def play_n_games(p1: Algorithm, p2: Algorithm, n_matches: int, name: str) -> None:
    """
    Function to play a number of moces
    :param p1: first player
    :param p2: second player
    :param n_matches: number of matches
    :param name: name to save the results
    :return: None
    """
    full_results = []  # Each element is the results of a single game

    for game in range(n_matches // 2):
        results = play_game(p1, p2)
        full_results.append(results)

    for game in range(n_matches // 2):
        results = play_game(p2, p1)
        full_results.append(results)

    update_csv(full_results, name)


def play_game(white: Algorithm, black: Algorithm) -> []:
    """
    Function to simulate one single match
    :param white: white player
    :param black: black player
    :return: results with the following format:
        [white, black, result, total_time, n_moves_w, n_moves_b, avg_move_time_white, avg_move_time_black]
    """
    match_recorder = MatchRecorder()

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
        match_recorder.register_move(white_move)
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
        match_recorder.register_move(black_move)
        board.execute_move(black_move, -1)
        avg_move_time_black = (n_moves_black * avg_move_time_black + (e - s)) / (n_moves_black + 1)
        n_moves_black += 1

    end = time.time()
    print('Game finished')
    match_recorder.finish_game()

    results = [white, black, result, end - start, n_moves_white, n_moves_black, avg_move_time_white,
               avg_move_time_black]
    return results


# white, black, result, total_time, n_moves_w, n_moves_b, avg_move_time_white, avg_move_time_black:
def update_csv(results: [], name: str) -> None:
    """
    Function to update the csv where the results are registered
    :param results: results of the matches
    :param name: name of the csv file
    :return: None
    """
    with open(name, 'w', newline='\n') as file:
        w = csv.writer(file, delimiter=';')
        w.writerow(
            ['white', 'black', 'result', 'total_time', 'n_moves_white', 'n_moves_black', 'avg_move_time_white',
             'avg_move_time_black'])
        for row in results:
            w.writerow(row)
