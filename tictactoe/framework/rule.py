from typing import Any


class InvalidStep(Exception):
    pass


class GameOver(Exception):
    def __init__(self, winner: Any):
        self.winner: Any = winner

    def __str__(self) -> str:
        return f"{self.winner} won!"


class Surrender(Exception):
    def __init__(self, loser: Any):
        self.loser: Any = loser

    def __str__(self) -> str:
        return f"{self.loser} surrendered!"


class Tied(GameOver):
    def __init__(self):
        super(Tied, self).__init__(None)


class RuleSet(object):
    def on_piece_down(self, x: int, y: int, p_index: int):
        """
        Before the piece is applied.
        :param x: x-coordinate
        :param y: y-coordinate
        :param p_index: piece index
        """
        pass

    def post_piece_down(self, x: int, y: int, p_index: int):
        """
        After the piece is applied.
        :param x: x-coordinate
        :param y: y-coordinate
        :param p_index: piece index
        """
        pass
