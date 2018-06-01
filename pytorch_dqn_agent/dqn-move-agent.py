import random
import math
import time
import torch
import torch.optim as optim
import torch.nn.functional as F
from pysc2.agents import base_agent
from pysc2.lib import actions, features
import numpy as np
from dqn import DQN, ReplayMemory, Transition

BATCH_SIZE = 64
GAMMA = 0.9  # Discounting factor

# Actions
_NO_OP = actions.FUNCTIONS.no_op.id
_MOVE_SCREEN = actions.FUNCTIONS.Move_screen.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id

_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index

_NOT_QUEUED = [0]
_SELECT_ALL = [0]

_PLAYER_SELF = 1
_PLAYER_NEUTRAL = 3
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index


model = DQN(2, 3)
optimizer = optim.RMSprop(model.parameters(), 1e-3)
memory = ReplayMemory(10000)


class DQNAgent(base_agent.BaseAgent):
    def __init__(self):
        super(DQNAgent, self).__init__()
        self.previous_state = None
        self.previous_action = None
        self.model = model
        self.memory = memory
        self.optimizer = optimizer
        self.diagnostics = [0, 0, 0]

    def step(self, obs):
        super(DQNAgent, self).step(obs)

        ### State space ###

        # we need to define what subset of the current game state
        # that we want to observe for our given problem.

        player_relative = obs.observation['screen'][_PLAYER_RELATIVE]
        beacon_y, beacon_x = (player_relative == _PLAYER_NEUTRAL).nonzero()

        can_move = _MOVE_SCREEN in obs.observation["available_actions"]
        beacon_located = beacon_y.any()

        position = [int(beacon_x.mean()), int(beacon_y.mean())]

        # [1, n_states] tensor of states
        state = torch.FloatTensor([[float(can_move), float(beacon_located)]])

        # Send states through model, collect
        # [1, n_actions] tensor of actions
        # Maximum a posterori rule, pick action with highest probability
        action = self.select_action(state, self.episodes)

        if action == 0:
            function_action = _MOVE_SCREEN
            target = [_NOT_QUEUED, position]
        elif action == 1:
            function_action = _SELECT_ARMY
            target = [_SELECT_ALL]
        else:
            function_action = _NO_OP
            target = []

        if self.previous_state is None:
            self.previous_action = action
            self.previous_state = state
            return actions.FunctionCall(_NO_OP, [])

        # Store the transition in memory
        self.memory.push(self.previous_state,
                         self.previous_action, state, self.reward)

        # Sample transitions and transpose
        transitions = self.memory.sample(BATCH_SIZE)
        batch = Transition(*zip(*transitions))

        self.optimize(batch)

        self.previous_action = action
        self.previous_state = state

        self.diagnostics[action] += 1

        print(self.diagnostics)

        time.sleep(0.3)
        return actions.FunctionCall(function_action, target)

    def optimize(self, batch):
        # Compute a mask of non-final states and concatenate the batch elements
        non_final_mask = torch.tensor(
            tuple(map(lambda s: s is not None, batch.next_state)), dtype=torch.uint8)

        # We don't want to backprop through the expected action values and volatile
        # will save us on temporarily changing the model parameters'
        # requires_grad to False!
        non_final_next_states = torch.cat([s for s in batch.next_state
                                           if s is not None])

        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)

        reward_batch = torch.from_numpy(
            np.array([batch.reward], dtype=np.int64)).float()
        reward_batch = torch.cat((reward_batch,))

        # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
        # columns of actions taken

        state_action_values = self.model(state_batch).gather(1, action_batch)

        # Compute V(s_{t+1}) for all next states.
        next_state_values = torch.zeros(BATCH_SIZE)
        next_state_values[non_final_mask] = model(
            non_final_next_states).max(1)[0].detach()

        # Now, we don't want to mess up the loss with a volatile flag, so let's
        # clear it. After this, we'll just end up with a Variable that has
        # requires_grad=False
        # next_state_values.volatile = False

        # Compute the expected Q values
        expected_state_action_values = (
            next_state_values * GAMMA) + reward_batch

        # Compute Huber loss
        loss = F.smooth_l1_loss(state_action_values,
                                expected_state_action_values.unsqueeze(1))

        # Optimize the model
        optimizer.zero_grad()
        loss.backward()

        for param in filter(lambda g: g.grad is not None, self.model.parameters()):
            param.grad.data.clamp_(-1, 1)

        optimizer.step()

    def select_action(self, state, n):
        epsilon = 0.05 + (0.9 - 0.05) * math.exp(-1. * n / 200)

        if random.random() > epsilon:
            # Return action from model
            with torch.no_grad():
                return self.model(state).max(1)[1].view(1, 1)
        else:
            return torch.tensor([[random.randrange(2)]], dtype=torch.long)
