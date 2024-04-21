import math
import random
import gym
import pygame
import numpy as np


class GridWorldEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 0.01}

    def __init__(self, render_mode="rgb_array", size=5):
        self.board_size = size
        self.board = None               # desk, numbers of knight in each cell, and knight images
        self.cells = [[0]*self.board_size for i in range(self.board_size)]
        self.type_env_agent = "random"
        self.query = 0
        self.plus = [0, 1, 9, 81, 729, 6561]
        self.minus = [0, 3, 27, 243, 2187, 19683]


    def reset(self, seed=None, options=None):
        # super().reset(seed=seed)
        np.random.seed()
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.cells[i][j] = 0
        # for i in self.cells.keys():
        #     self.cells[i] = 0

        return self._get_obs()

    def step(self, action):
        self.take_action(action)
        terminated = False
        if self.check_winner():
            reward = 1
            terminated = True
        else:
            if self.check_draw():
                reward = 0
                terminated = True
        if not terminated:
            self.get_move_from_env()
            if self.check_winner():
                terminated = True
                reward = -1
            else:
                if self.check_draw():
                    reward = 0
                    terminated = True
                else:
                    reward = 0

        observation = self._get_obs()

        info = False
        return observation, reward, terminated, False, info

    def _init_pygame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

    def _get_obs(self):
        return [x[:] for x in self.cells]

    def check_winner(self):
        board = self.cells
        if (self.query-1) % 2 == 0: # +1 чтобы проверить предыдущий ход
            symbol = 1
        else:
            symbol = -1
        zeroes = 0
        for row in self.cells:
            zeroes += row.count(0)
        # Проверка по горизонтали
        for row in range(self.board_size):
            for col in range(self.board_size - 4):
                if board[row][col] == symbol and board[row][col + 1] == symbol and board[row][col + 2] == symbol and \
                        board[row][col + 3] == symbol and board[row][col + 4] == symbol:
                    return True

        # Проверка по вертикали
        for col in range(self.board_size):
            for row in range(self.board_size - 4):
                if board[row][col] == symbol and board[row + 1][col] == symbol and board[row + 2][col] == symbol and \
                        board[row + 3][col] == symbol and board[row + 4][col] == symbol:
                    return True

        # Проверка по главной диагонали
        for row in range(self.board_size - 4):
            for col in range(self.board_size - 4):
                if board[row][col] == symbol and board[row + 1][col + 1] == symbol and board[row + 2][col + 2] == symbol and \
                        board[row + 3][col + 3] == symbol and board[row + 4][col + 4] == symbol:
                    return True

        # Проверка по побочной диагонали
        for row in range(self.board_size - 4):
            for col in range(4, self.board_size):
                if board[row][col] == symbol and board[row + 1][col - 1] == symbol and board[row + 2][col - 2] == symbol and \
                        board[row + 3][col - 3] == symbol and board[row + 4][col - 4] == symbol:
                    return True

        return False

    def take_action(self, action):
        row, col = action
        self.cells[row][col] = 1 if self.query % 2 == 0 else -1
        self.query += 1


    def get_move_from_env(self):
        match self.type_env_agent:
            case "random":
                move = self.random_agent_decision()
            case "smart":
                move = self.smart_agent_decision()
            case "neuro":
                move = self.random_agent_decision()

        self.take_action(move)

    def check_draw(self):
        zeroes = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.cells[i][j] == 0:
                    zeroes += 1
        return zeroes == 0

    def random_agent_decision(self):
        empty = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.cells[row][col] == 0:
                    empty.append((row, col))
        return random.choice(empty)

    def esctimate(self, cells1):
        score = 0
        i = 0
        for row in range(self.board_size):
            for col in range(self.board_size):
                if cells1[row][col] != 0:
                    i += 1
                for a in range(-1, 2):
                    for b in range(-1, 2):
                        if not (a == 0 and b == 0):
                            score += self.plus[self.score_(row, col, a, b, 1, cells1)] - self.minus[self.score_(row, col, a, b, -1, cells1)]
        return score

    def score_(self, x, y, a, b, symbol, cells1):
        score = 0
        for i in range(5):
            flag = self.border(x + a * i, y + b * i)
            if flag == -1 or (cells1[x + a * i][y + b * i] != symbol and cells1[x + a * i][y + b * i] != 0):
                return 0
            else:
                if cells1[x + a * i][y + b * i] == symbol:
                    score += 1
        return score

    def border(self, x, y):
        if x >= 0 and x < self.board_size and y >= 0 and y < self.board_size:
            return True
        return -1

    def best_move(self, cells1):
        tmp_cells = cells1.copy()
        score = -100000
        maxScore = -100000
        best_row = -1
        best_col = -1
        for row in range(self.board_size):
            for col in range(self.board_size):
                if tmp_cells[row][col] == 0:
                    tmp_cells[row][col] = 1
                    score = self.esctimate(tmp_cells)
                    if score > maxScore:
                        maxScore = score
                        best_row = row
                        best_col = col
                    tmp_cells[row][col] = 0
        return (best_row, best_col)

    def smart_agent_decision(self):
        action = self.best_move(self.cells)
        return action