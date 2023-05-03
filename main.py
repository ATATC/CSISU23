from time import sleep
from tictactoe import *
# from os import linesep
from tictactoe.framework import InvalidStep


linesep = "\n"


if __name__ == '__main__':
    scale = input("Scale, 1 by default: >>>")
    if scale.isnumeric():
        scale = int(scale)
    else:
        scale = 1
    board = TicTacToeBoard(TicTacToeRS(), horizontal_unit_sl=6 * scale + 3, vertical_unit_sl=2 * scale + 1)
    while True:
        player_a, rd_dir_a = choose_player("A", 0, True)
        player_b, rd_dir_b = choose_player("B", 1, True)
        print("Indexes are shown as below:")
        print(board.show_indexes())
        try:
            while True:
                try:
                    (player_a if board.get_round_counter() % 2 == 0 else player_b).go(board)
                    print(board)
                    sleep(.8)
                except InvalidStep:
                    print("Invalid index. Try again.")
        except Tied:
            print(board)
            print(f"Tied.")
        except GameOver as e:
            print(board)
            print(f"{player_a if e.winner == 0 else player_b} won!")
        except Surrender as e:
            print(board)
            print(f"{player_a if e.loser == 0 else player_b} surrendered!")
        if rd_dir_a is not None:
            with open(rd_dir_a, "w") as f:
                f.write(linesep.join(rd2lines(player_a.get_recorded_decisions())))
            print(f"Successfully recorded {player_a}'s decisions to `{rd_dir_a}`.")
        if rd_dir_b is not None:
            with open(rd_dir_b, "w") as f:
                f.write(linesep.join(rd2lines(player_b.get_recorded_decisions())))
            print(f"Successfully recorded {player_b}'s decisions to `{rd_dir_b}`.")
        if input("Restart or exit? (R) Restart (e) Exit >>>") != "R":
            break
        board.clear()
