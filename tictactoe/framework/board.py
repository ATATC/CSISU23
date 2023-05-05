from abc import abstractmethod
from copy import copy as _copy
# from os import linesep as _linesep
from typing import Optional, Callable
from tictactoe.framework.utils import AtomicInteger as _AtomicInteger
from tictactoe.framework.rule import RuleSet as _RuleSet, InvalidStep as _InvalidStep


_linesep = "\n"


class Board(object):
    def __init__(self,
                 width: int,
                 height: int,
                 rule_set: _RuleSet,
                 p_classes: int = 2,
                 horizontal_border: str = "-",
                 vertical_border: str = "|",
                 horizontal_unit_sl: int = 3,
                 vertical_unit_sl: int = 3,
                 horizontal_margin: int = 4,
                 vertical_margin: int = 1):
        """
        Create a board.
        :param width: width in plaids
        :param height: height in plaids
        :param rule_set: the rule set
        :param p_classes: the number of classes of pieces
        :param horizontal_border: a punctuation of horizontal border
        :param vertical_border: a punctuation of vertical border
        :param horizontal_unit_sl: horizontal unit side length
        :param vertical_unit_sl: vertical unit side length
        :param horizontal_margin: horizontal margin one on each side
        :param vertical_margin: vertical margin one at the top and one at the bottom
        """
        self._width: int = width
        self._height: int = height
        self._rs: _RuleSet = rule_set
        self._p_classes: int = p_classes
        self._p_map: list[list[int]] = Board.new_p_map(width, height)
        self._hb: str = horizontal_border
        self._vb: str = vertical_border
        if horizontal_unit_sl % 2 != 1:
            raise ValueError("Horizontal unit side length should be an odd number.")
        self._husl: int = horizontal_unit_sl
        if vertical_unit_sl % 2 != 1:
            raise ValueError("Vertical unit side length should be an odd number.")
        self._vusl: int = vertical_unit_sl
        self._hm: int = horizontal_margin
        self._vm: int = vertical_margin
        self._rc: int = 0

    @staticmethod
    def new_p_map(width: int, height: int) -> list[list[int]]:
        return [([-1] * width) for _ in range(height)]

    def revert_index(self, index: int) -> [int, int]:
        """
        Convert 1-D index to 2-D index.
        :param index: 1-D index
        :return: 2-D index
        """
        return index % self._width, index // self._width

    def convert_index(self, index: [int, int]) -> int:
        """
        Convert 2-D index to 1-D index.
        :param index: 2-D index
        :return: 1-D index
        """
        return index[1] * self._width + index[0]

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def get_piece_map(self) -> list[list[int]]:
        return self._p_map

    def get_round_counter(self) -> int:
        return self._rc

    @abstractmethod
    def get_piece_symbol(self, p_index: int) -> str:
        """
        Convert the piece index into a character.
        :param p_index: the piece index
        :return: the character, a string with a length of 1
        """
        pass

    def check_index(self, x: int, y: int, override: bool = False):
        if x >= self._width or y >= self._height or (not override and self._p_map[y][x] != -1):
            raise _InvalidStep

    def go(self, x: int, y: int, p_index: int, override: bool = False):
        self._check_p_index(p_index)
        self._rs.on_piece_down(x, y, p_index)
        self.check_index(x, y, override)
        self._p_map[y][x] = p_index
        self._rc += 1
        self._rs.post_piece_down(x, y, p_index)

    def row(self, index: int) -> list[int]:
        return _copy(self._p_map[index])

    def column(self, index: int) -> list[int]:
        return [self._p_map[i][index] for i in range(self._height)]

    def diagonal(self, from_x: int, towards_right: bool = True) -> list[int]:
        r = []
        y = 0
        for x in (range(from_x, self._width) if towards_right else range(from_x, -1, -1)):
            r.append(self[(x, y)])
            y += 1
            if y >= self._height:
                break
        return r

    def blanks(self) -> list[tuple[int, int]]:
        """
        Finds the indexes where the piece index equals -1.
        :return: a list of 2-D indexes
        """
        i = 0
        r = []
        for row in self._p_map:
            for p in row:
                if p == -1:
                    r.append(self.revert_index(i))
                i += 1
        return r

    def show_indexes(self) -> str:
        """
        Return a graph in string that displays the board filled with 1-D indexes.
        :return: graph string
        """
        i = _AtomicInteger(1)
        return self._show(lambda p_index: str(i.get_and_increment()), self._husl // 2, self._vusl // 2)

    def _check_p_index(self, p_index: int):
        """
        Check the piece index's legality.
        :param p_index: the piece index
        :raise: IndexError
        """
        if p_index < 0 or p_index >= self._p_classes:
            raise IndexError(f"Piece index out of range (p_classes={self._p_classes}).")

    def _show(self,
              symbolization: Optional[Callable] = None,
              horizontal_margin: int = 4,
              vertical_margin: int = 1) -> str:
        """
        Return a graph in string that displays the board.
        :param symbolization: the function that converts piece indexes into characters
        :param horizontal_margin: horizontal margin one on each side
        :param vertical_margin: vertical margin one at the top and one at the bottom
        :return: graph string
        """
        s = r = (" " + self._hb * self._husl) * self._width + _linesep
        for row in self._p_map:
            b = ((self._vb + " " * self._husl) * self._width + self._vb + _linesep) * vertical_margin
            s += b
            sp = ""
            for p_index in row:
                sp += self._vb + " " * horizontal_margin + (
                    self.get_piece_symbol
                    if symbolization is None
                    else symbolization
                )(p_index) * (self._husl - 2 * horizontal_margin) + " " * horizontal_margin
            sp += self._vb + _linesep
            s += sp * (self._vusl - 2 * vertical_margin) + b + r
        return s

    def __setitem__(self, key: [int, int], value: int):
        self.go(*key, value, True)

    def __getitem__(self, key: [int, int]) -> int:
        x, y = key
        return self._p_map[y][x]

    def __str__(self) -> str:
        return self._show(horizontal_margin=self._hm, vertical_margin=self._vm)
