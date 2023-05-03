from torch import load as _load
from random import choice as _choice
from tictactoe.framework import InvalidStep as _InvalidStep
from tictactoe.real_ai.module import Network as _Network
from tictactoe.real_ai.boards import get_current, get_merged
from tictactoe import Player as _Player, TicTacToeBoard as _TicTacToeBoard, Surrender as _Surrender


class AI(_Player):
    def __init__(self, network: _Network, name: str, p_index: int):
        super().__init__(name, p_index)
        self.network = network
        network.zero_grad()
        self._a = self._b = None

    def decide(self, board: _TicTacToeBoard) -> [int, int]:
        if self._a is None or self._b is None:
            self._a = self._b = get_current(board)
        output = self.network(get_merged(board, a=self._a, b=self._b))
        d = output.max(1, keepdim=True)[1] - 1
        if d == -1:
            raise _Surrender(self._p_index)
        index = board.revert_index(d)
        print(f"AI's decision: {index}.")
        try:
            board.check_index(*index)
        except _InvalidStep:
            print(UserWarning("WARNING: AI performed unexpectedly."))
            return _choice(board.blanks())
        return index


def load_from(path: str, name: str, p_index: int) -> AI:
    network = _Network()
    network.load_state_dict(_load(path))
    return AI(network, name, p_index)
