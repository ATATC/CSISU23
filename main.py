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
    player_a, rd_dir_a = choose_player("A", 0)
    player_b, rd_dir_b = choose_player("B", 1)
    # player_a, rd_dir_a = choose_player("A", 0, True)
    # player_b, rd_dir_b = choose_player("B", 1, True)
    while True:
        board = TicTacToeBoard(TicTacToeRS(), horizontal_unit_sl=6 * scale + 3, vertical_unit_sl=2 * scale + 1)
        print("Indexes are shown as below:")
        print(board.show_indexes())
        try:
            while True:
                try:
                    (player_a if board.get_round_counter() % 2 == 0 else player_b).go(board)
                    # if type(player_a) != HumanPlayer:
                    #     player_a.step(board)
                    # if type(player_b) != HumanPlayer:
                    #     player_b.step(board)
                    print(board)
                    sleep(.8)
                except InvalidStep:
                    print("Invalid index. Try again.")
        except Tied:
            print(board)
            print(f"Tied.")
        except GameOver as e:
            print(board)
            player = player_a if e.winner == 0 else player_b
            player.score += 1
            print(f"{player} won!")
        except Surrender as e:
            print(board)
            player = player_b if e.loser == 0 else player_a
            player.score += 1
            print(f"{player} won because the other surrendered!")
        print(f"{player_a.score} ({player_a}) : {player_b.score} ({player_b})")
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
        # if type(player_a) != HumanPlayer:
        #     player_a.clear()
        # if type(player_b) != HumanPlayer:
        #     player_b.clear()
