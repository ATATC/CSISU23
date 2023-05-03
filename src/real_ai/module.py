from torch import nn


class Network(nn.Module):
    def __init__(self):
        super(Network, self).__init__()
        self.fc1 = nn.Linear(108, 54)
        self.tanh = nn.Tanh()
        self.fc2 = nn.Linear(54, 9)

    def forward(self, x):
        x = self.fc1(x)
        x = self.tanh(x)
        return self.fc2(x)
