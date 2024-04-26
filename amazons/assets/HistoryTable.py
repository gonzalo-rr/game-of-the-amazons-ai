import _pickle as pickle
import os.path


class HistoryTable:
    def __init__(self):
        if os.path.isfile('history_table.pkl'):  # Load table if it exists
            self.load_table()
        else:  # Create the table if it doesn't
            self.moves_table = [[[[0 for _ in range(10)] for _ in range(10)] for _ in range(10)] for _ in range(10)]
            self.arrows_table = [[0 for _ in range(10)] for _ in range(10)]

    def get_rating(self, move):
        amazon = move[0]
        place = move[1]
        shoot = move[2]

        return self.moves_table[amazon[0]][amazon[1]][place[0]][place[1]] + self.arrows_table[shoot[0]][shoot[1]]

    def update_rating(self, move, weight):
        amazon = move[0]
        place = move[1]
        shoot = move[2]

        self.moves_table[amazon[0]][amazon[1]][place[0]][place[1]] += weight
        self.arrows_table[shoot[0]][shoot[1]] += weight

    def save_table(self):
        with open('history_table.pkl', 'wb') as output:
            pickle.dump(self, output)

    def load_table(self):
        with open('history_table.pkl', 'rb') as inp:
            history_table = pickle.load(inp)
            self.moves_table = history_table.moves_table
            self.arrows_table = history_table.arrows_table
