from torch import load as _load
from random import choice as _choice
from tictactoe.framework import InvalidStep as _InvalidStep
from tictactoe.real_ai.module import Network as _Network
from tictactoe.real_ai.boards import get_current, get_merged
from tictactoe import Player as _Player, Surrender as _Surrender, Board as _Board


class AI(_Player):
    def __init__(self, network: _Network, name: str, p_index: int):
        super().__init__(name, p_index)
        self.network = network
        network.zero_grad()
        self._a = self._b = None

    def step(self, board: _Board):
        self._b = self._a
        self._a = get_current(board)

    def decide(self, board: _Board) -> [int, int]:
        if self._a is None or self._b is None:
            self._a = self._b = get_current(board)
        output = self.network(get_merged(board, a=self._a, b=self._b))
        d = output.max(1, keepdim=True)[1].item() - 1
        print(f"AI output: {d}.")
        if d == -1:
            raise _Surrender(self._p_index)
        index = board.revert_index(d)
        try:
            board.check_index(*index)
        except _InvalidStep:
            print(UserWarning("WARNING: AI performed unexpectedly. Randomization intervened."))
            return _choice(board.blanks())
        return index

    def go(self, board: _Board):
        super().go(board)
        self.step(board)


def load_from(path: str, name: str, p_index: int) -> AI:
    network = _Network()
    network.load_state_dict(_load(path))
    return AI(network, name, p_index)
