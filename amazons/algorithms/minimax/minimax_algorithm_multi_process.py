import random
import time
import multiprocessing as mp

from amazons.algorithms.minimax.minimax_algorithm import MinimaxAlgorithm, evaluate_mobility
from amazons.logic.amazons_logic import Board

"""
white - max
black - min
"""


class MinimaxAlgorithmMultiProcess(MinimaxAlgorithm):
    """
    Class for the Minimax algorithm multiprocess with mobility evaluation and

    Attributes:
        _max_depth: max depth of the search tree
        _max_time: max time for exploring the tree
        n_workers: number of worker processes

    Author: Gonzalo Rodríguez Rodríguez
    """

    def __init__(self, max_depth: int, max_time: int, n_workers: int) -> None:
        """
        Constructor of the class
        :param max_depth: max depth of the search tree
        :param max_time: max time for exploring the tree
        """
        super().__init__(max_depth, max_time)
        self.n_workers = n_workers

    def __str__(self) -> str:
        """
        Method that returns the string value of the class
        :return: name of the algorithm
        """
        return 'MinimaxMultiProcess'

    def make_move(self, board: Board, player: int) -> tuple:
        """
        Method to get the move chosen by the algorithm in a given position for a given player
        :param board: position of the game
        :param player: player to move
        :return: move chosen by the algorithm
        """
        super().make_move(board, player)

        best_move = None
        self._end = time.time() + self._max_time
        for depth in range(1, self._max_depth + 1):
            self._max_depth = depth
            if time.time() >= self._end:
                break
            best_move = self.get_best_move(board, player)
        return best_move

    def get_best_move(self, board: Board, player: int) -> tuple:
        """
        Method to get the best move, dividing load for a number of workers
        :param board: board state
        :param player: integer representing plyer
        :return: the best move
        """
        new_board = Board(board.board)

        moves = new_board.get_legal_moves(player)
        if len(moves) == 0:
            raise ValueError("no moves found for the position")

        random.shuffle(moves)
        scores = mp.Array('f', len(moves))

        divided_moves = [moves[i * (len(moves) // self.n_workers) + min(i, len(moves) % self.n_workers):
                               (i + 1) * (len(moves) // self.n_workers) + min(i + 1, len(moves) % self.n_workers)]
                         for i in range(self.n_workers)]

        processes = []
        for worker in range(self.n_workers):
            process = mp.Process(target=self.worker_load,
                                 args=(new_board, player, divided_moves[worker], scores, worker,))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        best_score = player * float('-inf')
        best_score_index = -1
        for i, score in enumerate(scores):
            if player == 1:
                if score > best_score:
                    best_score = score
                    best_score_index = i
            else:
                if score < best_score:
                    best_score = score
                    best_score_index = i

        return moves[best_score_index]

    def worker_load(self, board: Board, player: int, moves: list, scores: list, pid: int) -> None:
        """
        Method to contain the worker load
        :param board: board state
        :param player: integer representing player
        :param moves: moves for the worker
        :param scores: scores of the moves
        :param pid: process id for the worker
        :return:
        """
        for i, move in enumerate(moves):
            board.execute_move(move, player)
            score = self._minimax(board, player, float('-inf'), float('inf'), 1)
            board.undo_move(move, player)

            if player == 1:
                if score > scores[i + pid * len(moves)]:
                    scores[i + pid * len(moves)] = score
            else:
                if score < scores[i + pid * len(moves)]:
                    scores[i + pid * len(moves)] = score

    def _minimax(self, board: Board, player: int, alpha: float, beta: float, depth: int) -> float:
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
            return evaluate_mobility(board)
        else:
            best_score = player * float('-inf')

            moves = board.get_legal_moves(player)
            random.shuffle(moves)

            for move in moves:
                if time.time() >= self._end:
                    return best_score
                board.execute_move(move, player)
                score = self._minimax(board, -player, alpha, beta, depth + 1)
                board.undo_move(move, player)

                if player == 1:
                    if score > best_score:
                        best_score = score

                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
                else:
                    if score < best_score:
                        best_score = score

                    beta = min(beta, score)
                    if beta <= alpha:
                        break

            return best_score
