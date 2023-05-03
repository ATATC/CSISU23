from boards import *
from tictactoe import *
from real_ai.module import *
from torch.optim import Adam
from torch.nn import CrossEntropyLoss


NUM_BATCHES = 8
BATCH_SIZE = 36   # Maximum 362880


if __name__ == '__main__':
    network = Network()
    loss_function = CrossEntropyLoss()
    optimizer = Adam(params=network.parameters(), lr=1e-3)
    opponent = RandomPlayer("Whoever", 0)
    boards = Boards(BATCH_SIZE)
    for epoch in range(NUM_BATCHES):
        output = network(boards.get_current())
        loss = loss_function(output, boards.get_suggestions().long())
        print(loss)
        optimizer.step()
