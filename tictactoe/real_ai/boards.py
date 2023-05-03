from torch import cat as _cat, Tensor as _Tensor
from tictactoe.framework import RandomPlayer as _RandomPlayer
from tictactoe import TicTacToeBoard as _TicTacToeBoard, TicTacToeRS as _TicTacToeRS, Bot as _Bot, \
    Surrender as _Surrender, GameOver as _GameOver


def get_current(*boards: _TicTacToeBoard) -> _Tensor:
    return _Tensor([b.get_piece_map() for b in boards]).view(-1, 3, 3, 1)


def get_merged(*boards: _TicTacToeBoard, a: _Tensor, b: _Tensor) -> _Tensor:
    x = get_current(*boards)
    x = _cat((x, a * .5), dim=3)
    x = _cat((x, b * .25), dim=3)
    return x


class Boards(object):
    def __init__(self, batch_size: int):
        self._batch_size: int = batch_size
        self._boards: list[_TicTacToeBoard] = [_TicTacToeBoard(_TicTacToeRS()) for _ in range(batch_size)]
        self._a: _Tensor = self.get_current()
        self._b: _Tensor = self.get_current()
        self._opponent: _RandomPlayer = _RandomPlayer("Opponent", 0)
        self._teacher: _Bot = _Bot("Teacher", 1)

    def get_current(self) -> _Tensor:
        return get_current(*self._boards)

    def get_merged(self) -> _Tensor:
        return get_merged(*self._boards, a=self._a, b=self._b)

    def opponent_go(self):
        for b in self._boards:
            try:
                self._opponent.go(b)
            except _GameOver:
                pass
        self.step()

    def go(self, y: _Tensor):
        for i in range(self._batch_size):
            board = self._boards[i]
            d = y[i].item()
            if d == 0:
                continue
            try:
                board.go(*board.revert_index(d - 1), p_index=1)
            except _GameOver:
                pass
        self.step()

    def get_suggestions(self) -> _Tensor:
        r = []
        for board in self._boards:
            try:
                r.append(board.convert_index(self._teacher.decide(board)) + 1)
            except _Surrender:
                r.append(0)
        return _Tensor(r).long()

    def step(self):
        self._b = self._a
        self._a = self.get_current()
