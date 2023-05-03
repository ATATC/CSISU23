from tictactoe import *
from torch import cat, Tensor
from framework import RandomPlayer


class Boards(object):
    def __init__(self, batch_size: int):
        self._batch_size: int = batch_size
        self._boards: list[Board] = [TicTacToeBoard(TicTacToeRS()) for _ in range(batch_size)]
        self._a: Tensor = self.get_current()
        self._b: Tensor = self.get_current()
        self._bot_a: RandomPlayer = RandomPlayer("Bot A", 0)
        self._bot_b: Bot = Bot("Bot B", 1)

    def get_current(self) -> Tensor:
        return Tensor([b.get_piece_map() for b in self._boards])

    def merge_tokens(self) -> Tensor:
        x = self.get_current()
        x = cat((x, self._a), dim=3)
        x = cat((x, self._b), dim=3)
        return x

    def go(self, y: Tensor):
        for i in range(self._batch_size):
            board = self._boards[i]
            board.go(*board.convert_index(y[i]), p_index=1)

    def get_suggestions(self) -> Tensor:
        return Tensor([self._bot_b.go(board) for board in self._boards])
