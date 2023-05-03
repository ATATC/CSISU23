from random import choice
from typing import Optional, Sequence, Callable
from tictactoe.framework import RuleSet, Player, Tied, GameOver, Board, ProgramedPlayer, classic_index


class TicTacToeRS(RuleSet):
    def __init__(self):
        self.board: Optional[TicTacToeBoard] = None

    def post_piece_down(self,
                        x: int,
                        y: int,
                        p_index: int):
        if self.board.get_round_counter() == self.board.get_width() * self.board.get_height():
            raise Tied()
        if (x + y) % 2 == 0 and (self.board.diagonal(0, True).count(p_index)
                                 == min(self.board.get_width(), self.board.get_height())
                                 or self.board.diagonal(2, False).count(p_index)
                                 == min(self.board.get_width(), self.board.get_height())):
            raise GameOver(p_index)
        if self.board.row(y) == [p_index] * self.board.get_width() \
                or self.board.column(x) == [p_index] * self.board.get_height():
            raise GameOver(p_index)


class TicTacToeBoard(Board):
    def __init__(self,
                 rule_set: TicTacToeRS,
                 horizontal_border: str = "-",
                 vertical_border: str = "|",
                 horizontal_unit_sl: int = 9,
                 vertical_unit_sl: int = 3):
        super().__init__(3, 3, rule_set, 2, horizontal_border, vertical_border, horizontal_unit_sl, vertical_unit_sl)
        rule_set.board = self

    def get_piece_symbol(self, p_index: int) -> str:
        return {
            -1: " ",
            0: "O",
            1: "X",
        }[p_index]


class HumanPlayer(Player):
    def decide(self, board: TicTacToeBoard) -> [int, int]:
        return board.revert_index(int(input(f"{self.name}, your turn: >>>")) - 1)


def valid_or_none(i: int) -> Optional[int]:
    return None if i < 0 else i


def attack(line: Sequence[int], *_) -> Optional[int]:
    return valid_or_none(classic_index(line, -1))


def defend(line: Sequence[int], pi: int, opi: int) -> Optional[int]:
    if line.count(pi) == 2 or line.count(opi) == 2:
        return attack(line)


def for_each_line(board: TicTacToeBoard, pi: int, opi: int, action: Callable) -> Optional[tuple[int, int]]:
    for i in range(3):
        x = action(board.row(i), pi, opi)
        if x is not None:
            return x, i
    for i in range(3):
        y = action(board.column(i), pi, opi)
        if y is not None:
            return i, y
    r = action(board.diagonal(0, True), pi, opi)
    if r is not None:
        return r, r
    r = action(board.diagonal(2, False), pi, opi)
    if r is not None:
        return 2 - r, r


class Bot(Player):
    """
    Works only when the board is 3x3.
    """

    def decide(self, board: TicTacToeBoard) -> [int, int]:
        if board.get_round_counter() == 0:
            return choice((0, 2)), choice((0, 2))
        opi = 1 - self._p_index
        if board.get_round_counter() > 2:
            r = for_each_line(board, self._p_index, opi, defend)
            if r is not None:
                return r
        corners = (board[(0, 0)], board[(2, 0)], board[(2, 2)], board[(0, 2)])
        if corners.count(self._p_index) == 3:
            return 1, 1
        i = classic_index(corners, -1)
        if i == 0:
            return 0, 0
        if i == 1:
            return 2, 0
        if i == 2:
            return 2, 2
        if i == 3:
            return 0, 2
        r = for_each_line(board, self._p_index, opi, attack)
        return (0, 0) if r is None else r


def rd2lines(rd: Sequence[tuple[int, int]]) -> list[str]:
    return [f"{x} {y}" for x, y in rd]


def lines2rd(lines: Sequence[str]) -> Sequence[tuple[int, int]]:
    r = []
    for line in lines:
        x, y = line.split()
        r.append((int(x), int(y)))
    return r


def choose_player(serial: str, p_index: int, ai_bot: bool = False) -> [Player, Optional[str]]:
    player = rd_dir = None
    serial = serial.upper()
    default_rd_dir = f"./recorded_decisions/{serial.lower()}.rd"
    while player is None:
        option = input(f"Would you like player {serial} to be a human or a bot? (H) Human (B) Bot >>>")
        if option == "H":
            name = input("Your name >>>")
            player = HumanPlayer(f"Player {serial}" if name == "" else name, p_index)
        elif option == "B":
            if ai_bot:
                from tictactoe.real_ai import load_from
                player = load_from("./model/23m05.pth", f"AI {serial}", p_index)
            else:
                player = Bot(f"Bot {serial}", p_index)
        else:
            print("Unknown option. Try again.")
    if input(f"Load previously recorded decisions? (Y) Yes (n) No >>>") == "Y":
        rd_dir = input(f"Load from file, `{default_rd_dir}` by default: >>>")
        if rd_dir == "":
            rd_dir = default_rd_dir
        with open(rd_dir, "r") as f:
            player = ProgramedPlayer(player, lines2rd(f.readlines()))
        rd_dir = None
    elif input(f"Record {player}'s decisions? (Y) Yes (n) No >>>") == "Y":
        player.record()
        rd_dir = input(f"Where to save {player}'s decisions? `{default_rd_dir}` by default: >>>")
        if rd_dir == "":
            rd_dir = default_rd_dir
    return player, rd_dir
