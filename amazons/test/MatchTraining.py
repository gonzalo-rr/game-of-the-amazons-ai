import csv
import time

from amazons.algorithms.mcts.MCTSAlgorithmEGreedyMod import MCTSAlgorithmEMod
from amazons.algorithms.minimax.MinimaxAlgorithmMobilityTable import MinimaxAlgorithmMobilityTable
from amazons.algorithms.minimax.MinimaxAlgorithmRelativeTerritoryTable import MinimaxAlgorithmRelativeTerritoryTable
from amazons.algorithms.minimax.MinimaxAlgorithmTerritoryMobilityTable import MinimaxAlgorithmTerritoryMobilityTable
from amazons.algorithms.minimax.MinimaxAlgorithmTerritoryTable import MinimaxAlgorithmTerritoryTable
from amazons.logic.AmazonsLogic import Board
from amazons.algorithms.RandomAlgorithm import RandomAlgorithm
from amazons.algorithms.greedy.GreedyAlgorithmTerritory import GreedyAlgorithmTerritory
from amazons.algorithms.mcts.MCTSAlgorithmEGreedy import MCTSAlgorithmE
from amazons.algorithms.mcts.MCTSAlgorithmUCB import MCTSAlgorithm
from amazons.algorithms.mcts.MCTSAlgorithmUCB_cut import MCTSAlgorithmCut
from amazons.algorithms.minimax.MinimaxAlgorithmMobility import MinimaxAlgorithmMobility
from amazons.algorithms.minimax.MinimaxAlgorithmRelativeTerritory import MinimaxAlgorithmRelativeTerritory
from amazons.algorithms.minimax.MinimaxAlgorithmTerritory import MinimaxAlgorithmTerritory
from amazons.algorithms.minimax.MinimaxAlgorithmTerritoryMobility import MinimaxAlgorithmTerritoryMobility
from assets.utilities.MatchRecorder import MatchRecorder


def match_training(n_matches):
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

    # p1 = MinimaxAlgorithmMobility(2, 10)
    # p2 = RandomAlgorithm()
    # play_n_games(p1, p2, n_matches, 'resMM2vR.csv')
    # match_recorder.save_results('resMM2vR.pkl')
    #
    # p1 = MinimaxAlgorithmMobility(3, 10)
    # p2 = RandomAlgorithm()
    # play_n_games(p1, p2, n_matches, 'resMM3vR.csv')
    # match_recorder.save_results('resMM3vR.pkl')
    #
    # p1 = MinimaxAlgorithmMobility(2, 10)
    # p2 = GreedyAlgorithmTerritory()
    # play_n_games(p1, p2, n_matches, 'resMM2vGT.csv')
    # match_recorder.save_results('resMM2vGT.pkl')
    #
    # p1 = MinimaxAlgorithmMobility(3, 10)
    # p2 = GreedyAlgorithmTerritory()
    # play_n_games(p1, p2, n_matches, 'resMM3vGT.csv')
    # match_recorder.save_results('resMM3vGT.pkl')
    #
    # # Set 2: Minimax Territory rec 2 & 3 vs Random & Greedy Territory
    #
    # p1 = MinimaxAlgorithmTerritory(2, 10)
    # p2 = RandomAlgorithm()
    # play_n_games(p1, p2, n_matches, 'resMT2vR.csv')
    # match_recorder.save_results('resMT2vR.pkl')
    #
    # p1 = MinimaxAlgorithmTerritory(3, 10)
    # p2 = RandomAlgorithm()
    # play_n_games(p1, p2, n_matches, 'resMT3vR.csv')
    # match_recorder.save_results('resMT3vR.pkl')
    #
    # p1 = MinimaxAlgorithmTerritory(2, 10)
    # p2 = GreedyAlgorithmTerritory()
    # play_n_games(p1, p2, n_matches, 'resMT2vGT.csv')
    # match_recorder.save_results('resMT2vGT.pkl')
    #
    # p1 = MinimaxAlgorithmTerritory(3, 10)
    # p2 = GreedyAlgorithmTerritory()
    # play_n_games(p1, p2, n_matches, 'resMT3vGT.csv')
    # match_recorder.save_results('resMT3vGT.pkl')
    #
    # # Set 3: Minimax Relative Territory rec 2 & 3 vs Random & Greedy Territory
    #
    # p1 = MinimaxAlgorithmRelativeTerritory(2, 10)
    # p2 = RandomAlgorithm()
    # play_n_games(p1, p2, n_matches, 'resMRT2vR.csv')
    # match_recorder.save_results('resMRT2vR.pkl')
    #
    # p1 = MinimaxAlgorithmRelativeTerritory(3, 10)
    # p2 = RandomAlgorithm()
    # play_n_games(p1, p2, n_matches, 'resMRT3vR.csv')
    # match_recorder.save_results('resMRT3vR.pkl')
    #
    # p1 = MinimaxAlgorithmRelativeTerritory(2, 10)
    # p2 = GreedyAlgorithmTerritory()
    # play_n_games(p1, p2, n_matches, 'resMRT2vGT.csv')
    # match_recorder.save_results('resMT2vGT.pkl')
    #
    # p1 = MinimaxAlgorithmRelativeTerritory(3, 10)
    # p2 = GreedyAlgorithmTerritory()
    # play_n_games(p1, p2, n_matches, 'resMRT3vGT.csv')
    # match_recorder.save_results('resMT3vGT.pkl')
    #
    # # Set 4: Minimax Territory Mobility rec 2 & 3 vs Random & Greedy Territory
    #
    # p1 = MinimaxAlgorithmTerritoryMobility(2, 10)
    # p2 = RandomAlgorithm()
    # play_n_games(p1, p2, n_matches, 'resMTM2vR.csv')
    # match_recorder.save_results('resMTM2vR.pkl')
    #
    # p1 = MinimaxAlgorithmTerritoryMobility(3, 10)
    # p2 = RandomAlgorithm()
    # play_n_games(p1, p2, n_matches, 'resMTM3vR.csv')
    # match_recorder.save_results('resMTM3vR.pkl')
    #
    # p1 = MinimaxAlgorithmTerritoryMobility(2, 10)
    # p2 = GreedyAlgorithmTerritory()
    # play_n_games(p1, p2, n_matches, 'resMTM2vGT.csv')
    # match_recorder.save_results('resMTM2vGT.pkl')
    #
    # p1 = MinimaxAlgorithmTerritoryMobility(3, 10)
    # p2 = GreedyAlgorithmTerritory()
    # play_n_games(p1, p2, n_matches, 'resMTM3vGT.csv')
    # match_recorder.save_results('resMTM3vGT.pkl')
    #
    # # Set 5: MCTS sim 1000 & 5000 vs Random & Greedy Territory
    #
    # p1 = MCTSAlgorithm(1000, 10)
    # p2 = RandomAlgorithm()
    # play_n_games(p1, p2, n_matches, 'resMCTS1vR.csv')
    # match_recorder.save_results('resMCTS1vR.pkl')
    #
    # p1 = MCTSAlgorithm(1000, 10)
    # p2 = GreedyAlgorithmTerritory()
    # play_n_games(p1, p2, n_matches, 'resMCTS1vGT.csv')
    # match_recorder.save_results('resMCTS1vGT.pkl')
    #
    # p1 = MCTSAlgorithm(5000, 10)
    # p2 = RandomAlgorithm()
    # play_n_games(p1, p2, n_matches, 'resMCTS5vR.csv')
    # match_recorder.save_results('resMCTS5vR.pkl')
    #
    # p1 = MCTSAlgorithm(5000, 10)
    # p2 = GreedyAlgorithmTerritory()
    # play_n_games(p1, p2, n_matches, 'resMCTS5vGT.csv')
    # match_recorder.save_results('resMCTS5vGT.pkl')
    #
    # # Set 6: MCTS_cut sim 1000, 5000 vs Random & Greedy Territory
    #
    # p1 = MCTSAlgorithmCut(1000, 10)
    # p2 = RandomAlgorithm()
    # play_n_games(p1, p2, n_matches, 'resMCTSC1vR.csv')
    # match_recorder.save_results('resMCTSC1vR.pkl')
    #
    # p1 = MCTSAlgorithmCut(1000, 10)
    # p2 = GreedyAlgorithmTerritory()
    # play_n_games(p1, p2, n_matches, 'resMCTSC1vGT.csv')
    # match_recorder.save_results('resMCTSC1vGT.pkl')
    #
    # p1 = MCTSAlgorithmCut(5000, 10)
    # p2 = RandomAlgorithm()
    # play_n_games(p1, p2, n_matches, 'resMCTSC5vR.csv')
    # match_recorder.save_results('resMCTSC5vR.pkl')
    #
    # p1 = MCTSAlgorithmCut(5000, 10)
    # p2 = GreedyAlgorithmTerritory()
    # play_n_games(p1, p2, n_matches, 'resMCTSC5vGT.csv')
    # match_recorder.save_results('resMCTSC5vGT.pkl')
    #
    # # Set 7: MCTS-E sim 1000, 5000 vs Random & Greedy Territory
    #
    # p1 = MCTSAlgorithmE(1000, 10)
    # p2 = RandomAlgorithm()
    # play_n_games(p1, p2, n_matches, 'resMCTSE1vR.csv')
    # match_recorder.save_results('resMCTSE1vR.pkl')
    #
    # p1 = MCTSAlgorithmE(1000, 10)
    # p2 = GreedyAlgorithmTerritory()
    # play_n_games(p1, p2, n_matches, 'resMCTSE1vGT.csv')
    # match_recorder.save_results('resMCTSE1vGT.pkl')
    #
    # p1 = MCTSAlgorithmE(5000, 10)
    # p2 = RandomAlgorithm()
    # play_n_games(p1, p2, n_matches, 'resMCTSE5vR.csv')
    # match_recorder.save_results('resMCTSE5vR.pkl')
    #
    # p1 = MCTSAlgorithmE(5000, 10)
    # p2 = GreedyAlgorithmTerritory()
    # play_n_games(p1, p2, n_matches, 'resMCTSE5vGT.csv')
    # match_recorder.save_results('resMCTSE5vGT.pkl')
    #
    # # Set 8: MCTS-E' sim 100, 1000, 10000 vs Random & Greedy Territory
    #
    # p1 = MCTSAlgorithmE(1000, 10)
    # p2 = RandomAlgorithm()
    # play_n_games(p1, p2, n_matches, 'resMCTSEm1vR.csv')
    # match_recorder.save_results('resMCTSEm1vR.pkl')
    #
    # p1 = MCTSAlgorithmE(1000, 10)
    # p2 = GreedyAlgorithmTerritory()
    # play_n_games(p1, p2, n_matches, 'resMCTSEm1vGT.csv')
    # match_recorder.save_results('resMCTSEm1vGT.pkl')
    #
    # p1 = MCTSAlgorithmE(5000, 10)
    # p2 = RandomAlgorithm()
    # play_n_games(p1, p2, n_matches, 'resMCTSEm5vR.csv')
    # match_recorder.save_results('resMCTSEm5vR.pkl')
    #
    # p1 = MCTSAlgorithmE(5000, 10)
    # p2 = GreedyAlgorithmTerritory()
    # play_n_games(p1, p2, n_matches, 'resMCTSEm5vGT.csv')
    # match_recorder.save_results('resMCTSEm5vGT.pkl')

    # Set 9: MCTS [IMPORTANT]
    p1 = MCTSAlgorithm(10_000, 25)
    p2 = MCTSAlgorithmCut(10_000, 25)
    play_n_games(p1, p2, n_matches, 'resMCTSvMCTSC.csv')
    match_recorder.save_results('resMCTSvMCTSC.pkl')

    p1 = MCTSAlgorithmE(10_000, 25)
    p2 = MCTSAlgorithmEMod(10_000, 25)
    play_n_games(p1, p2, n_matches, 'resMCTSEvMCTSEM.csv')
    match_recorder.save_results('resMCTSEvMCTSEM.pkl')

    p1 = MCTSAlgorithmE(10_000, 25)
    p2 = MCTSAlgorithmCut(10_000, 25)
    play_n_games(p1, p2, n_matches, 'resMCTSEvMCTSC.csv')
    match_recorder.save_results('resMCTSEvMCTSC.pkl')

    # Set 10: Minimax [IMPORTANT]
    p1 = MinimaxAlgorithmTerritory(2, 10)
    p2 = MinimaxAlgorithmRelativeTerritory(2, 10)
    play_n_games(p1, p2, n_matches, 'resMTvMRT.csv')
    match_recorder.save_results('resMTvMRT.pkl')

    p1 = MinimaxAlgorithmMobility(2, 10)
    p2 = MinimaxAlgorithmTerritory(2, 10)
    play_n_games(p1, p2, n_matches, 'resMMvMT.csv')
    match_recorder.save_results('resMMvMT.pkl')

    p1 = MinimaxAlgorithmMobility(2, 10)
    p2 = MinimaxAlgorithmTerritoryMobility(2, 10)
    play_n_games(p1, p2, n_matches, 'resMMvMTM.csv')
    match_recorder.save_results('resMMvMTM.pkl')

    p1 = MinimaxAlgorithmTerritory(2, 10)
    p2 = MinimaxAlgorithmTerritoryMobility(2, 10)
    play_n_games(p1, p2, n_matches, 'resMTvMTM.csv')
    match_recorder.save_results('resMTvMTM.pkl')

    # # Set 11: Minimax vs MCTS [IMPORTANT]
    # p1 = MinimaxAlgorithmMobility(2, 10)
    # p2 = MinimaxAlgorithmMobilityTable(2, 10)
    # play_n_games(p1, p2, n_matches, 'resMMvMCTSUCB.csv')
    # match_recorder.save_results('resMMvMCTSUCB.pkl')
    #
    # # Set 12: Table vs NoTable (MinimaxMobility, MinimaxTerritory, MinimaxRelativeTerritory, MinimaxTerritoryMobility)
    # p1 = MinimaxAlgorithmMobility(2, 10)
    # p2 = MinimaxAlgorithmMobilityTable(2, 10)
    # play_n_games(p1, p2, n_matches, 'resMMvMMT.csv')
    # match_recorder.save_results('resMMvMMT.pkl')
    #
    # p1 = MinimaxAlgorithmTerritory(2, 10)
    # p2 = MinimaxAlgorithmTerritoryTable(2, 10)
    # play_n_games(p1, p2, n_matches, 'resMTvMTT.csv')
    # match_recorder.save_results('resMTvMTT.pkl')
    #
    # p1 = MinimaxAlgorithmRelativeTerritory(2, 10)
    # p2 = MinimaxAlgorithmRelativeTerritoryTable(2, 10)
    # play_n_games(p1, p2, n_matches, 'resMRTvMRT.csv')
    # match_recorder.save_results('resMRTvMRT.pkl')
    #
    # p1 = MinimaxAlgorithmTerritoryMobility(2, 10)
    # p2 = MinimaxAlgorithmTerritoryMobilityTable(2, 10)
    # play_n_games(p1, p2, n_matches, 'resMTMvMTMT.csv')
    # match_recorder.save_results('resMTMvMTMT.pkl')


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
def update_csv(results, name):
    with open(name, 'w', newline='\n') as file:
        w = csv.writer(file, delimiter=';')
        w.writerow(
            ['white', 'black', 'result', 'total_time', 'n_moves_white', 'n_moves_black', 'avg_move_time_white',
             'avg_move_time_black'])
        for row in results:
            w.writerow(row)