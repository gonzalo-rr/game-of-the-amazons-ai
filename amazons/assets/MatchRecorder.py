import pickle


class Recorder(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Recorder, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MatchRecorder(metaclass=Recorder):
    def __init__(self):
        self.__match_moves = []
        self.__games = []

    def register_move(self, move):
        self.__match_moves.append(move)

    def finish_game(self):
        self.__games.append(self.__match_moves)
        self.__match_moves = []

    def save_results(self, name):
        with open(name, 'wb') as output:
            pickle.dump(self.__games, output)

        self.__games = []