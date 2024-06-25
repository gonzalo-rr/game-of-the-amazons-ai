import os.path
import pickle


class HistoryTable:
    """
    Table to register and recover evaluations of moves

    Attributes:
        name: name of the instance of the history table (also name to be saved with pickle module)
        moves_table: table to register amazons moves
        arrows_table: table to register arrow shots

    """

    def __init__(self, name: str) -> None:
        """
        Constructor of the class
        :param name: name of the instance
        """
        self.name = name + ".pkl"
        if os.path.isfile(self.name):  # Load table if it exists
            self.load_table()
        else:  # Create the table if it doesn't
            self.moves_table = [[[[0 for _ in range(10)] for _ in range(10)] for _ in range(10)] for _ in range(10)]
            self.arrows_table = [[0 for _ in range(10)] for _ in range(10)]

    def get_rating(self, move: tuple) -> float:
        """
        Method to recover the rating of a move
        :param move: move to recover its evaluation
        :return: evaluation for the move
        """
        amazon = move[0]
        place = move[1]
        shoot = move[2]

        return self.moves_table[amazon[0]][amazon[1]][place[0]][place[1]] + self.arrows_table[shoot[0]][shoot[1]]

    def update_rating(self, move: tuple, weight: int) -> None:
        """
        Method to update the rating of a move
        :param move:
        :param weight:
        :return:
        """
        amazon = move[0]
        place = move[1]
        shoot = move[2]

        self.moves_table[amazon[0]][amazon[1]][place[0]][place[1]] += weight
        self.arrows_table[shoot[0]][shoot[1]] += weight

    def save_table(self) -> None:
        """
        Method to serialize the table
        :return: None
        """
        with open(self.name, 'wb') as output:
            pickle.dump(self, output)

    def load_table(self) -> None:
        """
        Method to deserialize the table
        :return: None
        """
        with open(self.name, 'rb') as inp:
            history_table = pickle.load(inp)
            self.moves_table = history_table.moves_table
            self.arrows_table = history_table.arrows_table
