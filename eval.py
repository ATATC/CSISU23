from tictactoe.real_ai import load_from
from tictactoe.framework import RandomPlayer
from tictactoe import TicTacToeBoard, TicTacToeRS, GameOver, Surrender, Tied


class Tester(RandomPlayer):
    def step(self, *args): pass
    def clear(self): pass


PA = Tester("Tester", 0)
PB = load_from("./model/23mxx.pth", "AI", 1)

NUM_GAMES = 10000

if __name__ == '__main__':
    scoreboard = [0, 0]
    cases = [0, 0, 0]
    for i in range(NUM_GAMES):
        board = TicTacToeBoard(TicTacToeRS())
        try:
            while True:
                PA.go(board)
                PA.step(board)
                PB.go(board)
                PB.step(board)
        except Tied:
            cases[1] += 1
        except GameOver as e:
            cases[0] += 1
            scoreboard[e.winner] += 1
        except Surrender as e:
            cases[2] += 1
            scoreboard[1 - e.loser] += 1
        finally:
            PA.clear()
            PB.clear()
    print(f"{cases[0]} / {cases[1]} / {cases[2]}")
    print(f"{scoreboard[0]} : {scoreboard[1]} / {NUM_GAMES}")
