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
_SELECT_POINT = actions.FUNCTIONS.select_point.id
_BUILD_SUPPLY_DEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
_BUILD_BARRACKS = actions.FUNCTIONS.Build_Barracks_screen.id
_TRAIN_MARINE = actions.FUNCTIONS.Train_Marine_quick.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_ATTACK_MINIMAP = actions.FUNCTIONS.Attack_minimap.id


# Unit IDs
_TERRAN_COMMANDCENTER = 18
_TERRAN_SCV = 45
_TERRAN_SUPPLY_DEPOT = 19
_TERRAN_BARRACKS = 21


# Parameters
_PLAYER_SELF = 1
_PLAYER_NEUTRAL = 3
_SUPPLY_USED = 3
_SUPPLY_MAX = 4
_NOT_QUEUED = [0]
_QUEUED = [1]
_SELECT_ALL = [0]

_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
_PLAYER_ID = features.SCREEN_FEATURES.player_id.index

ACTION_DO_NOTHING = 'donothing'
ACTION_SELECT_SCV = 'selectscv'
ACTION_BUILD_SUPPLY_DEPOT = 'buildsupplydepot'
ACTION_BUILD_BARRACKS = 'buildbarracks'
ACTION_SELECT_BARRACKS = 'selectbarracks'
ACTION_BUILD_MARINE = 'buildmarine'
ACTION_SELECT_ARMY = 'selectarmy'
ACTION_ATTACK = 'attack'
ACTION_MOVE_SCREEN = 'movescreen'

smart_actions = [
    ACTION_MOVE_SCREEN,
    ACTION_SELECT_ARMY,
    ACTION_DO_NOTHING,
    ACTION_SELECT_SCV,
    ACTION_BUILD_SUPPLY_DEPOT,
    ACTION_BUILD_BARRACKS,
    ACTION_ATTACK,

    ACTION_SELECT_BARRACKS,
    ACTION_BUILD_MARINE,


]

KILL_UNIT_REWARD = 0.2
KILL_BUILDING_REWARD = 0.5


model = DQN(6, 9)
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
        self.diagnostics = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.base_top_left = None
        self.supply_depot_built = False
        self.scv_selected = False
        self.barracks_built = False
        self.barracks_selected = False
        self.barracks_rallied = False
        self.army_selected = False
        self.army_rallied = False

        self.previous_killed_unit_score = 0
        self.previous_killed_building_score = 0

        self.previous_action = None
        self.previous_state = None

    def transformLocation(self, x, x_distance, y, y_distance):
        if not self.base_top_left:
            return [x - x_distance, y - y_distance]

        return [x + x_distance, y + y_distance]

    def step(self, obs):
        super().step(obs)

        ### State space ###

        # we need to define what subset of the current game state
        # that we want to observe for our given problem.

        player_y, player_x = (
            obs.observation['minimap'][_PLAYER_RELATIVE] == _PLAYER_SELF).nonzero()
        self.base_top_left = 1 if player_y.any() and player_y.mean() <= 31 else 0

        can_move = _MOVE_SCREEN in obs.observation["available_actions"]
        player_located = player_y.any()


        unit_type = obs.observation['screen'][_UNIT_TYPE]

        depot_y, depot_x = (unit_type == _TERRAN_SUPPLY_DEPOT).nonzero()
        supply_depot_count = supply_depot_count = 1 if depot_y.any() else 0

        barracks_y, barracks_x = (unit_type == _TERRAN_BARRACKS).nonzero()
        barracks_count = 1 if barracks_y.any() else 0

        supply_limit = obs.observation['player'][4]
        army_supply = obs.observation['player'][5]
        function_action = None
      
        # [1, n_states] tensor of states
        state = torch.FloatTensor([[float(can_move), float(player_located),
                                    float(supply_depot_count), float(
                                        barracks_count), float(supply_limit),
                                    float(army_supply)

                                    ]])

        # Store the transition in memory
        temp_action = self.select_action(state, self.episodes)
        smart_action = smart_actions[temp_action]

        if check_available(obs, _MOVE_SCREEN) and smart_action == ACTION_MOVE_SCREEN:
            function_action = _MOVE_SCREEN
            target = [_NOT_QUEUED, position]

        elif check_available(obs, _NO_OP) and smart_action == ACTION_DO_NOTHING:
            function_action = _NO_OP
            target = []

        elif check_available(obs, _SELECT_POINT) and smart_action == ACTION_SELECT_SCV:
            unit_type = obs.observation['screen'][_UNIT_TYPE]
            unit_y, unit_x = (unit_type == _TERRAN_SCV).nonzero()

            if unit_y.any():
                i = random.randint(0, len(unit_y) - 1)
                function_action = _SELECT_POINT
                target = [_NOT_QUEUED, [unit_x[i], unit_y[i]]]

        elif check_available(obs, _BUILD_SUPPLY_DEPOT) and smart_action == ACTION_BUILD_SUPPLY_DEPOT:
            unit_type = obs.observation['screen'][_UNIT_TYPE]
            unit_y, unit_x = (unit_type == _TERRAN_COMMANDCENTER).nonzero()

            if unit_y.any():
                function_action = _BUILD_SUPPLY_DEPOT
                target = self.transformLocation(
                    int(unit_x.mean()), 0, int(unit_y.mean()), 20)

                target = [_NOT_QUEUED, target]

        elif check_available(obs, _BUILD_BARRACKS) and smart_action == ACTION_BUILD_BARRACKS:
            unit_type = obs.observation['screen'][_UNIT_TYPE]
            unit_y, unit_x = (unit_type == _TERRAN_COMMANDCENTER).nonzero()

            if unit_y.any():
                target = self.transformLocation(
                    int(unit_x.mean()), 20, int(unit_y.mean()), 0)
                function_action = _BUILD_BARRACKS
                target = [_NOT_QUEUED, target]

        elif smart_action == ACTION_ATTACK:
            if _ATTACK_MINIMAP in obs.observation["available_actions"]:
                if self.base_top_left:
                    function_action = _ATTACK_MINIMAP,
                    target = [_NOT_QUEUED, [39, 45]]
                function_action = _ATTACK_MINIMAP
                target = [_NOT_QUEUED, [21, 24]]

        elif smart_action == ACTION_SELECT_ARMY:
            if _SELECT_ARMY in obs.observation['available_actions']:
                function_action = _SELECT_ARMY
                target = [_NOT_QUEUED]

        elif smart_action == ACTION_BUILD_MARINE:
            if _TRAIN_MARINE in obs.observation['available_actions']:
                function_action = _TRAIN_MARINE
                target = [_QUEUED]

        elif smart_action == ACTION_SELECT_BARRACKS:
            unit_type = obs.observation['screen'][_UNIT_TYPE]
            unit_y, unit_x = (unit_type == _TERRAN_BARRACKS).nonzero()
            if unit_y.any():
                position = [int(unit_x.mean()), int(unit_y.mean())]
                function_action = _SELECT_POINT
                target = [_NOT_QUEUED, position]

        else:
            function_action = _NO_OP
            target = []

        if function_action is None:
            function_action = _NO_OP
            target = []

        if self.previous_state is None:
            self.previous_action = temp_action
            self.previous_state = state
            return actions.FunctionCall(_NO_OP, [])

        # Store the transition in memory
        self.memory.push(self.previous_state,
                         self.previous_action, state, self.reward)

        # Sample transitions and transpose
        transitions = self.memory.sample(BATCH_SIZE)
        batch = Transition(*zip(*transitions))

        self.optimize(batch)

        self.previous_action = temp_action
        self.previous_state = state

        self.diagnostics[temp_action] += 1

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
                                expected_state_action_values.view(64, 1))

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
            return torch.tensor([[random.randrange(9)]], dtype=torch.long)


def check_available(obs, action):
    return action in obs.observation["available_actions"]
