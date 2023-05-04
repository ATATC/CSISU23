from torch import save
from torch.optim import Adam
from torch.nn import CrossEntropyLoss
from tictactoe.real_ai.boards import *
from tictactoe.real_ai.module import *


NUM_BATCHES = 80000
BATCH_SIZE = 8

# this controls over-fitting
ROUND_LIMIT = 8


if __name__ == '__main__':
    network = Network()
    loss_function = CrossEntropyLoss()
    optimizer = Adam(params=network.parameters(), lr=1e-3)
    boards = None
    for epoch in range(NUM_BATCHES):
        if epoch % ROUND_LIMIT == 0:
            boards = Boards(BATCH_SIZE)
        boards.opponent_go()
        output = network(boards.get_merged())
        suggestions = boards.get_suggestions()
        loss = loss_function(output, suggestions)
        print(loss.item())
        boards.go(suggestions)
        loss.backward()
        optimizer.step()
    save(network.state_dict(), "./model/23m05.pth")
