from random import choice as _choice
from tictactoe.framework import InvalidStep
from tictactoe.real_ai.module import RealAI
from tictactoe import Player, Surrender, Board
from torch import load as _load, no_grad as _no_grad
from tictactoe.real_ai.boards import get_current, get_merged, get_default


class AI(Player):
    def __init__(self, model: RealAI, name: str, p_index: int):
        super().__init__(name, p_index)
        _no_grad()
        model.eval()
        self.model: RealAI = model
        self._a = self._b = None

    def step(self, board: Board):
        self._b = self._a
        self._a = get_current(board)

    def clear(self):
        self._a = self._b = None

    def decide(self, board: Board) -> [int, int]:
        if self._a is None or self._b is None:
            self._a = get_current(board)
            self._b = get_default(board)
        output = self.model(get_merged(board, a=self._a, b=self._b))
        d = output.max(1, keepdim=True)[1].item() - 1
        print(f"AI output: {d}.")
        if d == -1:
            raise Surrender(self._p_index)
        index = board.revert_index(d)
        try:
            board.check_index(*index)
        except InvalidStep:
            print(UserWarning("WARNING: AI performed unexpectedly. Randomization intervened."))
            return _choice(board.blanks())
        return index

    def go(self, board: Board):
        super().go(board)
        self.step(board)


def load_from(path: str, name: str, p_index: int) -> AI:
    model = RealAI()
    model.load_state_dict(_load(path))
    return AI(model, name, p_index)
