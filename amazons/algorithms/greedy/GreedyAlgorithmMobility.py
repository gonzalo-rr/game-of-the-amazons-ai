from amazons.algorithms.minimax.MinimaxAlgorithm import evaluate_mobility
from amazons.logic.AmazonsLogic import Board


class GreedyAlgorithmMobility:

    def __str__(self):
        return 'GreedyMob'

    def make_move(self, board, player):
        moves = board.get_legal_moves(player)
        if len(moves) == 0:
            raise ValueError("no moves found for the position")

        best_score = player * float('-inf')
        best_move = moves[0]

        if len(moves) == 0:
            raise ValueError("no moves found for the position")

        if len(moves) == 1:
            best_move = moves[0]

        new_board = Board(board)

        for move in moves:
            new_board.execute_move(move, player)
            score = evaluate_mobility(new_board)
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
