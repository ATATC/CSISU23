# from os import linesep
from time import sleep
from tictactoe import *


linesep = "\n"


if __name__ == '__main__':
    while True:
        board = TicTacToeBoard(TicTacToeRS())
        player_a, rd_dir_a = choose_player("A", 0)
        player_b, rd_dir_b = choose_player("B", 1)
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
