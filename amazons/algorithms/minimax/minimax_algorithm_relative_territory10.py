import time

from amazons.algorithms.minimax.minimax_algorithm import MinimaxAlgorithm, evaluate_territory, \
    difference_relative_territory_10, sort_moves, weight
from amazons.algorithms.minimax.history_table.history_table import HistoryTable
from amazons.logic.amazons_logic import Board


"""
white - max
black - min
"""


class MinimaxAlgorithmRelativeTerritory(MinimaxAlgorithm):
    """
    Deprecated class for the Minimax algorithm with relative territory evaluation

    Attributes:
        _max_depth: max depth of the search tree
        _max_time: max time for exploring the tree

    Author: Gonzalo Rodríguez Rodríguez
    """

    def __init__(self, max_depth: int, max_time: int) -> None:
        """
        Constructor of the class
        :param max_depth: max depth of the search tree
        :param max_time: max time for exploring the tree
        """
        super().__init__(max_depth, max_time)
        self.history_table = HistoryTable("history_table10")

    def __str__(self) -> str:
        """
        Method that returns the string value of the class
        :return: name of the algorithm
        """
        return 'MinimaxRTerritory10'

    def make_move(self, board: Board, player: int) -> tuple:
        """
        Method to get the move chosen by the algorithm in a given position for a given player
        :param board: position of the game
        :param player: player to move
        :return: move chosen by the algorithm
        """
        super().make_move(board, player)

        new_board = Board(board)
        moves = new_board.get_legal_moves(player)
        if len(moves) == 0:
            raise ValueError("no moves found for the position")

        best_move = moves[0]

        self._end = time.time() + self._max_time
        for depth in range(1, self._max_depth + 1):
            self._max_depth = depth
            if time.time() >= self._end:
                break
            _, new_best_move = self._minimax(new_board, player, float('-inf'), float('inf'), 0)
            if new_best_move is not None:
                best_move = new_best_move

        self.history_table.save_table()
        return best_move

    def _minimax(self, board: Board, player: int, alpha: float, beta: float, depth: int) -> tuple:
        """
        Minimax recursive search algorithm
        :param board: board with the current state of the game
        :param player: player with the turn
        :param alpha: alpha pruning parameter
        :param beta: beta pruning parameter
        :param depth: depth where the minimax algorithm is executed
        :return: (evaluation, move)
        """
        if board.is_win(player) or board.is_win(-player) or depth == self._max_depth:
            return evaluate_territory(board, difference_relative_territory_10, player), None
        else:
            best_score = player * float('-inf')
            best_move = None

            moves = board.get_legal_moves(player)
            if len(moves) == 1:
                best_move = moves[0]

            rating = [0 for _ in range(len(moves))]

            for i, move in enumerate(moves):  # Rating all moves
                rating[i] = self.history_table.get_rating(move) / 4  # ??

            moves = sort_moves(moves, rating)

            for move in moves:
                board.execute_move(move, player)
                score, _ = self._minimax(board, -player, alpha, beta, depth + 1)
                board.undo_move(move, player)

                if player == 1:
                    if score > best_score:
                        best_move = move
                        best_score = score

                    alpha = max(alpha, score)
                    if beta <= alpha:
                        self.history_table.update_rating(best_move, weight(self._max_depth - depth))
                        break
                else:
                    if score < best_score:
                        best_move = move
                        best_score = score

                    beta = min(beta, score)
                    if beta <= alpha:
                        self.history_table.update_rating(best_move, weight(self._max_depth - depth))
                        break

            return best_score, best_move
