import numpy as np
import random
import torch
import torch.nn as nn
from collections import deque
from collections import namedtuple
from copy import deepcopy

np.random.seed(1)
torch.manual_seed(1)

Transition = namedtuple(
    'Transition', ('state', 'action', 'reward',
                   'next_state', 'done'))


class Agent:
    def __init__(
            self, env,
            learning_rate=0.07,
            discount_factor=0.95,
            epsilon_greedy=0.9,
            epsilon_min=0.1,
            epsilon_decay=0.9996,
            max_memory_size=300):
        self.env = env
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon_greedy
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

        self.memory = deque(maxlen=max_memory_size) # переходы в памяти

        self.board_size = 9
        self.state_size = self.board_size**2  # self.n_knights + 2
        self.state = [0]*self.state_size
        self._build_nn_model()

    def _build_nn_model(self, is_prev_model=False):
        neurons = 128
        self.model = nn.Sequential(nn.Linear(self.state_size, neurons),
                                    nn.ReLU(),
                                    nn.Linear(neurons, 128), # слои
                                    nn.ReLU(),
                                    nn.Linear(neurons, 128),
                                    nn.ReLU(),
                                    nn.Linear(neurons, 1))

        if is_prev_model:
            self.model.load_state_dict(torch.load('my_model.pth'))

        self.target_model = deepcopy(self.model)

        self.loss_fn = nn.MSELoss()
        self.optimizer = torch.optim.Adam(
            self.model.parameters(), self.lr)

    def save_nn_model(self):
        torch.save(self.model.state_dict(), 'my_model.pth')

    def remember(self, transition):
        self.memory.append(transition)

#info это поле state
    def choose_action(self, info): # менять
        all_variants = self.get_all_possible_moves(info)
        # print(info)
        if np.random.uniform() < self.epsilon:
            return random.choice(all_variants)

        with torch.no_grad():
            q_a_values = [self.model(torch.tensor(self.convert_to_nn_input(info, q_a), dtype=torch.float32))[0]
                          for q_a in all_variants]

        selected_move = np.argmax(q_a_values)

        return all_variants[selected_move]  # returns action

    def _learn(self, batch_samples): #немного менять
        batch_states, batch_targets = [], []
        for transition in batch_samples:
            s, a, r, next_s, done = transition
            # print(s)
            # print(a)
            # print(next_s)
            # print(r)
            if done:

                target = r
            else:
                target = r + self.gamma*self.state_value(next_s)

            state = self.convert_to_nn_input(s, a)

            batch_states.append(state)
            batch_targets.append(torch.tensor([target], dtype=torch.float32))
            self._adjust_epsilon()

        pred = self.model(torch.tensor(batch_states, dtype=torch.float32))

        self.optimizer.zero_grad()

        loss = self.loss_fn(pred, torch.stack(batch_targets))
        loss.backward()
        self.optimizer.step()

        return loss.item()

    def replay(self, batch_size):
        samples = random.sample(self.memory, batch_size)
        return self._learn(samples)

    def _adjust_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def get_all_possible_moves(self, state): #переделал #можно улучшить для 10 лучших
        possible_moves = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if state[i][j] == 0:
                    possible_moves.append((i, j))

        return possible_moves

    def state_value(self, info):
        if len(info) == 0:
            return 0
        all_variants = self.get_all_possible_moves(info)
        with torch.no_grad():
            q_a_values = [self.target_model(torch.tensor(self.convert_to_nn_input(info, q_a), dtype=torch.float32))[0]
                          for q_a in all_variants
                          ]

        return np.max(q_a_values)

    def update_model(self):
        self.target_model = deepcopy(self.model)

    def value(self, inf, action):
        return self.model(torch.tensor(self.convert_to_nn_input(inf, action), dtype=torch.float32)) #ценность состояния и действия

    def convert_to_nn_input(self, info, action): #переделать

        for i in range(self.state_size):
            self.state[i] = 0

        for i in range(self.board_size):
            for j in range(self.board_size):
                self.state[i*self.board_size + j] = info[i][j]

        row, col = action
        self.state[row*self.board_size + col] = 3

        return self.state[:]

