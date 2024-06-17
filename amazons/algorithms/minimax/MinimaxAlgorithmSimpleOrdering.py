import random
import time

from amazons.algorithms.minimax.MinimaxAlgorithm import MinimaxAlgorithm, evaluate_mobility, sort_moves
from amazons.logic.AmazonsLogic import Board


"""
white - max
black - min
"""


class MinimaxAlgorithmSimpleOrdering(MinimaxAlgorithm):

    def __init__(self, max_depth, max_time):
        super().__init__(max_depth, max_time)
        self.ratings = [{} for _ in range(max_depth)]

    def make_move(self, board: Board, player: int) -> ((int, int), (int, int), (int, int)):
        super().make_move(board, player)

        new_board = Board(board.board)
        best_move = None
        self.ratings = [{} for _ in range(self._max_depth)]

        self._end = time.time() + self._max_time
        for depth in range(1, self._max_depth + 1):
            self._max_depth = depth
            if time.time() >= self._end:
                break
            _, best_move = self._minimax(new_board, player, float('-inf'), float('inf'), 0)

        return best_move

    def _minimax(self, board: Board, player: int, alpha: float, beta: float, depth: int) -> \
            (float, ((int, int), (int, int), (int, int))):
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

