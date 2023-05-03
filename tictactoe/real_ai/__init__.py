from torch import load as _load
from tictactoe.real_ai.module import Network as _Network
from tictactoe.real_ai.boards import get_current, get_merged
from tictactoe import Player as _Player, TicTacToeBoard as _TicTacToeBoard


class AI(_Player):
    def __init__(self, network: _Network, name: str, p_index: int):
        super().__init__(name, p_index)
        self.network = network
        self._a = self._b = None

    def decide(self, board: _TicTacToeBoard) -> [int, int]:
        if self._a is None or self._b is None:
            self._a = self._b = get_current(board)
        output = self.network(get_merged(board, a=self._a, b=self._b))
        return board.revert_index(output.max(1, keepdim=True)[1][0].item())


def load_from(path: str, name: str, p_index: int) -> AI:
    network = _Network()
    network.load_state_dict(_load(path))
    return AI(network, name, p_index)
