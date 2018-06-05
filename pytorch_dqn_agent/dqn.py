import random
import torch.nn as nn
import torch.nn.functional as F
from collections import namedtuple


Transition = namedtuple(
    'Transition', ('state', 'action', 'next_state', 'reward'))


class ReplayMemory(object):
    def __init__(self, buffersize):
        self.buffersize = buffersize
        self.memory = []
        self.index = 0

    def push(self, *args):
        if len(self.memory) < self.buffersize:  # Still room
            self.memory.append(None)
        self.memory[self.index] = Transition(*args)
        self.index = (self.index + 1) % self.buffersize  # Next or wrap around

    def sample(self, batch_size):
        return random.choices(self.memory, k=batch_size)

    def __len__(self):
        return len(self.memory)


class DQN(nn.Module):
    def __init__(self, n_states, n_actions):
        super().__init__()
        self.linear1 = nn.Linear(n_states, 64)
        self.batchn1 = nn.BatchNorm1d(64)
        self.linear2 = nn.Linear(64, 64)
        self.batchn2 = nn.BatchNorm2d(64)
        self.linear3 = nn.Linear(64, n_actions)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        return F.softmax(self.linear3(x), -1)
