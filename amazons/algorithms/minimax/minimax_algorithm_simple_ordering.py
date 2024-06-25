import random
import time

from amazons.algorithms.minimax.minimax_algorithm import MinimaxAlgorithm, evaluate_mobility, sort_moves
from amazons.logic.amazons_logic import Board


"""
white - max
black - min
"""


class MinimaxAlgorithmSimpleOrdering(MinimaxAlgorithm):
    """
    Deprecated class for the Minimax algorithm with mobility evaluation and simple ordering

    Attributes:
        _max_depth: max depth of the search tree
        _max_time: max time for exploring the tree
        ratings: rating of moves for ordering

    Author: Gonzalo Rodríguez Rodríguez
    """

    def __init__(self, max_depth: int, max_time: int) -> None:
        """
        Constructor of the class
        :param max_depth: max depth of the search tree
        :param max_time: max time for exploring the tree
        """
        super().__init__(max_depth, max_time)
        self.ratings = [{} for _ in range(max_depth)]

    def __str__(self) -> str:
        """
        Method that returns the string value of the class
        :return: name of the algorithm
        """
        return 'MinimaxSimpleOrdering'

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

        self.ratings = [{} for _ in range(self._max_depth)]

        self._end = time.time() + self._max_time
        for depth in range(1, self._max_depth + 1):
            self._max_depth = depth
            if time.time() >= self._end:
                break
            _, best_move = self._minimax(new_board, player, float('-inf'), float('inf'), 0)

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
            return evaluate_mobility(board), None
        else:
            best_score = player * float('-inf')
            best_move = None

            moves = board.get_legal_moves(player)
            if len(self.ratings[depth]) != 0:
                moves = sort_moves(moves, self.ratings[depth])
            else:
                random.shuffle(moves)

            for move in moves:
                board.execute_move(move, player)
                score, _ = self._minimax(board, -player, alpha, beta, depth + 1)
                self.ratings[depth][hash(move)] = score  # Give a rating to the move
                board.undo_move(move, player)

                if player == 1:
                    if score > best_score:
                        best_move = move
                        best_score = score

                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
                else:
                    if score < best_score:
                        best_move = move
                        best_score = score

                    beta = min(beta, score)
                    if beta <= alpha:
                        break

            return best_score, best_move

