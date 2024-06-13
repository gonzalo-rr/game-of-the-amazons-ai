from copy import deepcopy, copy

from amazons.AmazonsLogic import Board
from amazons.assets.UtilityFunctions import difference_territory, evaluate_territory


class GreedyAlgorithmTerritory:

    def __str__(self):
        return 'GreedyTer'

    def make_move(self, board, player):
        moves = board.get_legal_moves(player)
        best_score = player * float('-inf')
        best_move = moves[0]

        if len(moves) == 1:
            best_move = moves[0]

        for move in moves:
            new_board = Board(board)
            new_board.execute_move(move, player)
            score = evaluate_territory(new_board, difference_territory, player)

            if player == 1:
                if score > best_score:
                    best_move = move
                    best_score = score
            else:
                if score < best_score:
                    best_move = move
                    best_score = score

        return best_move

