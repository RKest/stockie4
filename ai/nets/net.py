import torch.nn as nn
import torch.nn.functional as F
from torch import sigmoid

class LenNet(nn.Module):
    def __init__(self, t_len=50):
        super().__init__()
        self.fc1 = nn.Linear(2 + 2*t_len, 2 + 2*t_len)
        self.fc2 = nn.Linear(2 + 2*t_len, 1 + t_len)
        self.fc3 = nn.Linear(1 + t_len, 1 + t_len)
        self.fc4 = nn.Linear(1 + t_len, 1)

    def forward(self, x):
        x = F.leaky_relu(self.fc1(x))
        x = F.leaky_relu(self.fc2(x))
        x = F.leaky_relu(self.fc3(x))
        x = self.fc4(x)
        return x

class SlopeDirNet(nn.Module):
    def __init__(self, t_len=50):
        super().__init__()
        self.fc1 = nn.Linear(2 + 2*t_len, 2 + 2*t_len)
        self.fc2 = nn.Linear(2 + 2*t_len, 1 + t_len)
        self.fc3 = nn.Linear(1 + t_len, 1 + t_len)
        self.fc4 = nn.Linear(1 + t_len, 1)

    def forward(self, x):
        x = F.leaky_relu(self.fc1(x))
        x = F.leaky_relu(self.fc2(x))
        x = F.leaky_relu(self.fc3(x))
        x = self.fc4(x)
        return sigmoid(x)