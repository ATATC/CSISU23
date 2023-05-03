from typing import Sequence
from abc import abstractmethod
from copy import copy as _copy
from src.framework.board import Board as _Board
from random import choice as _choice


class Player(object):
    def __init__(self, name: str, p_index: int):
        self.name: str = name
        self._p_index: int = p_index
        self._record_mode: bool = False
        self._recorded_decisions: list[tuple[int, int]] = []

    def record(self):
        self._record_mode = True

    @abstractmethod
    def decide(self, board: _Board) -> [int, int]: pass

    def go(self, board: _Board):
        decision = self.decide(_copy(board))
        board.go(*decision, self._p_index, False)
        self._recorded_decisions.append(decision)

    def get_recorded_decisions(self) -> list[tuple[int, int]]:
        return self._recorded_decisions

    def __str__(self) -> str:
        return self.name


class ProgramedPlayer(Player):
    def __init__(self, player: Player, decisions: Sequence[tuple[int, int]]):
        super(ProgramedPlayer, self).__init__(player.name, player._p_index)
        self._player: Player = player
        self._decisions: Sequence[Sequence[int, int]] = decisions
        self._i: int = -1

    def decide(self, board: _Board) -> [int, int]:
        self._i += 1
        return self._decisions[self._i] if self._i < len(self._decisions) else self._player.decide(board)


class RandomPlayer(Player):
    """
    This is for the unit tests.
    """
    def decide(self, board: _Board) -> [int, int]:
        return _choice(board.blanks())
