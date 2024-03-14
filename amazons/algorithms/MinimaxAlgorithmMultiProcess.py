import random
import sys
import time
import multiprocessing as mp

from amazons.AmazonsLogic import Board

"""
white - max
black - min
"""


def evaluate_mobility(board):
    if board.is_win(1):
        return float('inf')
    if board.is_win(-1):
        return float('-inf')

    white_moves = board.get_legal_moves(1)
    black_moves = board.get_legal_moves(-1)
    return len(white_moves) - len(black_moves)


class MinimaxAlgorithmMultiProcess:
    def __init__(self, max_depth, max_time, n_workers):
        self.max_depth = max_depth
        self.max_time = max_time
        self.n_workers = n_workers
        self.end = 0

    def make_move(self, board, player):
        best_move = None
        self.end = time.time() + self.max_time
        for depth in range(1, self.max_depth + 1):
            if time.time() >= self.end:
                break
            best_move = self.get_best_move(board, player)
        return best_move

    def get_best_move(self, board, player):
        new_board = Board(board.board)

        moves = new_board.get_legal_moves(player)
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

    def worker_load(self, board, player, moves, scores, pid):
        for i, move in enumerate(moves):
            board.execute_move(move, player)
            score = self.minimax(board, player, float('-inf'), float('inf'), 1)
            board.undo_move(move, player)

            if player == 1:
                if score > scores[i + pid * len(moves)]:
                    scores[i + pid * len(moves)] = score
            else:
                if score < scores[i + pid * len(moves)]:
                    scores[i + pid * len(moves)] = score

    def minimax(self, board, player, alpha, beta, depth):
        if board.is_win(player) or board.is_win(-player) or depth == self.max_depth:
            return evaluate_mobility(board)
        else:
            best_score = player * float('-inf')

            moves = board.get_legal_moves(player)
            random.shuffle(moves)

            for move in moves:
                if time.time() >= self.end:
                    return best_score
                board.execute_move(move, player)
                score = self.minimax(board, -player, alpha, beta, depth + 1)
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
