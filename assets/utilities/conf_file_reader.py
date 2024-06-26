from amazons.algorithms.greedy.greedy_algorithm_mobility import GreedyAlgorithmMobility
from amazons.algorithms.greedy.greedy_algorithm_territory import GreedyAlgorithmTerritory
from amazons.algorithms.mcts.mcts_algorithm_e_greedy import MCTSAlgorithmE
from amazons.algorithms.mcts.mcts_algorithm_e_greedy_mod import MCTSAlgorithmEMod
from amazons.algorithms.mcts.mcts_algorithm_ucb import MCTSAlgorithmUCB
from amazons.algorithms.mcts.mcts_algorithm_ucb_cut import MCTSAlgorithmCut
from amazons.algorithms.minimax.minimax_algorithm_mobility import MinimaxAlgorithmMobility
from amazons.algorithms.minimax.minimax_algorithm_mobility_table import MinimaxAlgorithmMobilityTable
from amazons.algorithms.minimax.minimax_algorithm_relative_territory import MinimaxAlgorithmRelativeTerritory
from amazons.algorithms.minimax.minimax_algorithm_relative_territory_table import MinimaxAlgorithmRelativeTerritoryTable
from amazons.algorithms.minimax.minimax_algorithm_territory import MinimaxAlgorithmTerritory
from amazons.algorithms.minimax.minimax_algorithm_territory_mobility import MinimaxAlgorithmTerritoryMobility
from amazons.algorithms.minimax.minimax_algorithm_territory_mobility_table import MinimaxAlgorithmTerritoryMobilityTable
from amazons.algorithms.minimax.minimax_algorithm_territory_table import MinimaxAlgorithmTerritoryTable
from amazons.algorithms.random_algorithm import RandomAlgorithm

"""
Set of functions to read configuration files and parse them

Author: Gonzalo Rodríguez Rodríguez
"""


def read_gui_file(file: str) -> list:
    """
    Reads and parses gui configuration file and returns the algorithms specified in it
    Args:
        file: file name

    Returns: list of algorithms

    """
    algorithms = []
    with open(file, 'r') as inp:
        lines = inp.readlines()
        for line in lines:
            algorithms.append(get_algorithm_from_line(line))

    return algorithms


def get_algorithm_from_line(line):
    """
    Parses a line and returns an algorithm from the line

    Args:
        line: line of text

    Returns: algorithm

    """
    line = line.split(" ")
    line = [s.strip() for s in line]
    alg = line[0]

    if alg == "human":
        return None

    if alg == 'random':
        return RandomAlgorithm()

    if alg == 'greedy_mobility':
        return GreedyAlgorithmMobility()

    if alg == 'greedy_territory':
        return GreedyAlgorithmTerritory()

    if alg == 'minimax_mobility':
        if len(line) != 3:
            raise ValueError("incorrect file format")
        if not (line[1].isdigit() and line[2].isdigit()):
            raise ValueError("incorrect file format")
        param1 = int(line[1])
        param2 = int(line[2])
        return MinimaxAlgorithmMobility(param1, param2)

    if alg == 'minimax_territory':
        if len(line) != 3:
            raise ValueError("incorrect file format")
        if not (line[1].isdigit() and line[2].isdigit()):
            raise ValueError("incorrect file format")
        param1 = int(line[1])
        param2 = int(line[2])
        return MinimaxAlgorithmTerritory(param1, param2)

    if alg == 'minimax_relative_territory':
        if len(line) != 3:
            raise ValueError("incorrect file format")
        if not (line[1].isdigit() and line[2].isdigit()):
            raise ValueError("incorrect file format")
        param1 = int(line[1])
        param2 = int(line[2])
        return MinimaxAlgorithmRelativeTerritory(param1, param2)

    if alg == 'minimax_territory_mobility':
        if len(line) != 3:
            raise ValueError("incorrect file format")
        if not (line[1].isdigit() and line[2].isdigit()):
            raise ValueError("incorrect file format")
        param1 = int(line[1])
        param2 = int(line[2])
        return MinimaxAlgorithmTerritoryMobility(param1, param2)

    if alg == 'minimax_mobility_table':
        if len(line) != 3:
            raise ValueError("incorrect file format")
        if not (line[1].isdigit() and line[2].isdigit()):
            raise ValueError("incorrect file format")
        param1 = int(line[1])
        param2 = int(line[2])
        return MinimaxAlgorithmMobilityTable(param1, param2)

    if alg == 'minimax_territory_table':
        if len(line) != 3:
            raise ValueError("incorrect file format")
        if not (line[1].isdigit() and line[2].isdigit()):
            raise ValueError("incorrect file format")
        param1 = int(line[1])
        param2 = int(line[2])
        return MinimaxAlgorithmTerritoryTable(param1, param2)

    if alg == 'minimax_relative_territory_table':
        if len(line) != 3:
            raise ValueError("incorrect file format")
        if not (line[1].isdigit() and line[2].isdigit()):
            raise ValueError("incorrect file format")
        param1 = int(line[1])
        param2 = int(line[2])
        return MinimaxAlgorithmRelativeTerritoryTable(param1, param2)

    if alg == 'minimax_territory_mobility_table':
        if len(line) != 3:
            raise ValueError("incorrect file format")
        if not (line[1].isdigit() and line[2].isdigit()):
            raise ValueError("incorrect file format")
        param1 = int(line[1])
        param2 = int(line[2])
        return MinimaxAlgorithmTerritoryMobilityTable(param1, param2)

    if alg == 'mcts_ucb':
        if len(line) != 3 and len(line) != 4:
            raise ValueError("incorrect file format")
        if not (line[1].isdigit() and line[2].isdigit()):
            raise ValueError("incorrect file format")
        param1 = int(line[1])
        param2 = int(line[2])
        if len(line) == 4:
            try:
                param3 = float(line[3])
            except ValueError:
                raise ValueError("incorrect file format")
            return MCTSAlgorithmUCB(param1, param2, param3)
        else:
            return MCTSAlgorithmUCB(param1, param2)

    if alg == 'mcts_ucb_cut':
        if len(line) != 3 and len(line) != 4:
            raise ValueError("incorrect file format")
        if not (line[1].isdigit() and line[2].isdigit()):
            raise ValueError("incorrect file format")
        param1 = int(line[1])
        param2 = int(line[2])
        if len(line) == 4:
            try:
                param3 = float(line[3])
            except ValueError:
                raise ValueError("incorrect file format")
            return MCTSAlgorithmCut(param1, param2, param3)
        else:
            return MCTSAlgorithmCut(param1, param2)

    if alg == 'mcts_epsilon':
        if len(line) != 3 and len(line) != 4:
            raise ValueError("incorrect file format")
        if not (line[1].isdigit() and line[2].isdigit()):
            raise ValueError("incorrect file format")
        param1 = int(line[1])
        param2 = int(line[2])
        if len(line) == 4:
            try:
                param3 = float(line[3])
            except ValueError:
                raise ValueError("incorrect file format")
            return MCTSAlgorithmE(param1, param2, param3)
        else:
            return MCTSAlgorithmE(param1, param2)

    if alg == 'mcts_epsilon_mod':
        if len(line) != 3 and len(line) != 4:
            raise ValueError("incorrect file format")
        if not (line[1].isdigit() and line[2].isdigit()):
            raise ValueError("incorrect file format")
        param1 = int(line[1])
        param2 = int(line[2])
        if len(line) == 4:
            try:
                param3 = float(line[3])
            except ValueError:
                raise ValueError("incorrect file format")
            return MCTSAlgorithmEMod(param1, param2, param3)
        else:
            return MCTSAlgorithmEMod(param1, param2)

    raise ValueError("incorrect file format")


def read_training_file(file: str) -> list:
    """
    Reads and parses training configuration file and returns a list with the matches
    Args:
        file: file name

    Returns: list of matches, each element containing a tuple of 3 elements that are both algorithms and the number
    of matches to play between them
    """
    matches = []  # Format: (player1, player2, num_matches)
    with open(file, 'r') as inp:
        lines = inp.readlines()
        for line in lines:
            matches.append(get_matchup_from_line(line))

    return matches


def get_matchup_from_line(line):
    line = line.split(":")
    match_up = line[0]
    players = match_up.split(" v ")
    player1 = players[0].strip()
    player2 = players[1].strip()
    n_matches = line[1].strip()
    if n_matches % 2 != 0:
        raise ValueError("number of matches must always be even")

    player1 = get_algorithm_from_line(player1)
    player2 = get_algorithm_from_line(player2)

    return player1, player2, n_matches
