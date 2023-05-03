from tictactoe.framework import RandomPlayer
from tictactoe import TicTacToeBoard as _TicTacToeBoard, TicTacToeRS as _TicTacToeRS, Bot as _Bot
from torch import cat as _cat, Tensor as _Tensor


def get_current(*boards: _TicTacToeBoard) -> _Tensor:
    return _Tensor([b.get_piece_map() for b in boards]).view(-1, 3, 3, 1)


def get_merged(*boards: _TicTacToeBoard, a: _Tensor, b: _Tensor) -> _Tensor:
    x = get_current(*boards)
    x = _cat((x, a), dim=3)
    x = _cat((x, b), dim=3)
    return x


class Boards(object):
    def __init__(self, batch_size: int):
        self._batch_size: int = batch_size
        self._boards: list[_TicTacToeBoard] = [_TicTacToeBoard(_TicTacToeRS()) for _ in range(batch_size)]
        self._a: _Tensor = self.get_current()
        self._b: _Tensor = self.get_current()
        self._bot_a: RandomPlayer = RandomPlayer("Bot A", 0)
        self._bot_b: _Bot = _Bot("Bot B", 1)

    def get_current(self) -> _Tensor:
        return get_current(*self._boards)

    def get_merged(self) -> _Tensor:
        return get_merged(*self._boards, a=self._a, b=self._b)

    def go(self, y: _Tensor):
        for i in range(self._batch_size):
            board = self._boards[i]
            board.go(*board.revert_index(y[i]), p_index=1)

    def get_suggestions(self) -> _Tensor:
        self._b = self._a
        self._a = self.get_current()
        return _Tensor([board.convert_index(self._bot_b.decide(board)) for board in self._boards])
