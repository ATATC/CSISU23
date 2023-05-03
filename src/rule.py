from typing import Any


class InvalidStep(Exception):
    pass


class GameOver(Exception):
    def __init__(self, winner: Any):
        self.winner: Any = winner


class Tied(GameOver):
    def __init__(self):
        super(Tied, self).__init__(None)


class RuleSet(object):
    def on_piece_down(self,
                      x: int,
                      y: int,
                      p_index: int): pass

    def post_piece_down(self,
                        x: int,
                        y: int,
                        p_index: int): pass
