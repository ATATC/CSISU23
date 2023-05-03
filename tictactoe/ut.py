import unittest
from tictactoe import *


class MyTestCase(unittest.TestCase):
    def randomizationTest(self):
        pass

    def test(self):
        player = Bot("Bot", 1)
        board = TicTacToeBoard(TicTacToeRS())
        self.assertEqual(board._rc, 0)
        board._rc = 9
        self.assertEqual(board._p_map, [])
        board._p_map = [[1, 0, 1], [0, 1, 0], [1, 0, 0]]
        print(player.decide(board))


if __name__ == '__main__':
    unittest.main()
