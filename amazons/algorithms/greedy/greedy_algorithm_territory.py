from amazons.algorithms.algorithm import Algorithm
from amazons.algorithms.minimax.minimax_algorithm import evaluate_territory, difference_territory
from amazons.logic.amazons_logic import Board


class GreedyAlgorithmTerritory(Algorithm):
    """
    Algorithm based on a greedy approach that uses a territory heuristic function

    Author: Gonzalo Rodríguez Rodríguez
    """

    def __str__(self) -> str:
        """
        Returns the name of the algorithm
        :return: name of the algorithm
        """
        return 'GreedyTer'

    def make_move(self, board: Board, player: int) -> ((int, int), (int, int), (int, int)):
        """
        Returns the move that the algorithm chooses
        :param board: state of the board
        :param player: int that represents the player
        :return: chosen move
        """

        moves = board.get_legal_moves(player)
        if len(moves) == 0:
            raise ValueError("no moves found for the position")

        best_score = player * float('-inf')
        best_move = moves[0]

        if len(moves) == 1:
            best_move = moves[0]

        new_board = Board(board)

        for move in moves:
            new_board.execute_move(move, player)
            score = evaluate_territory(new_board, difference_territory, player)
            new_board.undo_move(move, player)

            if player == 1:
                if score > best_score:
                    best_move = move
                    best_score = score
            else:
                if score < best_score:
                    best_move = move
                    best_score = score

        return best_move

