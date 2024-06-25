import pickle


class Recorder(type):
    """
    Metaclass for the MatchRecorder class
    This class exists in order to follow the singleton design pattern

    Author: Gonzalo Rodríguez Rodríguez
    """
    _instances = {}

    def __call__(cls, *args, **kwargs) -> {}:
        if cls not in cls._instances:
            cls._instances[cls] = super(Recorder, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MatchRecorder(metaclass=Recorder):
    """
    Class to record the moves during a set of games

    Author: Gonzalo Rodríguez Rodríguez
    """
    def __init__(self) -> None:
        """
        Constructor of the class
        :returns None
        """
        self.__match_moves = []
        self.__games = []

    def register_move(self, move: tuple) -> None:
        """
        Method to register a move
        :param move: move to be registered
        :return: None
        """
        self.__match_moves.append(move)

    def finish_game(self) -> None:
        """
        Method to save the moves of a game when it is over
        :return: None
        """
        self.__games.append(self.__match_moves)
        self.__match_moves = []

    def save_results(self, name: str) -> None:
        """
        Method to save the moves of a set of games when it is over
        :param name: name of the pickle file to save the moves to
        :return: None
        """
        with open(name, 'wb') as output:
            pickle.dump(self.__games, output)

        self.__games = []
