from torch import save
from torch.optim import Adam
from torch.nn import CrossEntropyLoss
from tictactoe.real_ai.boards import *
from tictactoe.real_ai.module import *
from tictactoe.framework import RandomPlayer


NUM_BATCHES = 100000
BATCH_SIZE = 4   # Maximum 362880


if __name__ == '__main__':
    network = Network()
    loss_function = CrossEntropyLoss()
    optimizer = Adam(params=network.parameters(), lr=1e-3)
    opponent = RandomPlayer("Whoever", 0)
    boards = Boards(BATCH_SIZE)
    for epoch in range(NUM_BATCHES):
        output = network(boards.get_merged())
        loss = loss_function(output, boards.get_suggestions().long())
        print(loss.item())
        loss.backward()
        optimizer.step()
    save(network.state_dict(), "./model/23m05.pth")
