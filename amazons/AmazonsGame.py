from Game import Game
from .AmazonsLogic import Board
import sys
import numpy as np

class AmazonsGame(Game):

    def getInitBoard(self):
        board = Board()
        return np.array(board.board)

    def getBoardSize(self):
        return (10, 10)

    def getActionSize(self):
        return self.b
