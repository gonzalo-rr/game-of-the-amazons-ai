from abc import ABC, abstractmethod


class Player(ABC):

    @abstractmethod
    def is_human(self) -> bool:
        ...

    @abstractmethod
    def make_move(self) -> None:
        ...
