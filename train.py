from torch import save
from torch.optim import Adam
from torch.nn import CrossEntropyLoss
from tictactoe.real_ai.boards import *
from tictactoe.real_ai.module import *


NUM_BATCHES = 80000
ZERO_LIMIT = .05 * NUM_BATCHES

# these control over-fitting
# (16, 8) (32, 7)
BATCH_SIZE = 16
ROUND_LIMIT = 8

if __name__ == '__main__':
    counter = 0
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
        if loss == 0:
            if counter > ZERO_LIMIT:
                epoch -= 1
                continue
            counter += 1
        print(loss.item())
        boards.go(suggestions)
        loss.backward()
        optimizer.step()
    print(f"{counter}/{NUM_BATCHES}")
    save(network.state_dict(), "./model/23m05.pth")
