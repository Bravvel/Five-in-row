import matplotlib.pyplot as plt
import numpy as np
from agent import Agent
import time
from enviroment import GridWorldEnv
from collections import namedtuple

Transition = namedtuple(
    'Transition', ('state', 'action', 'reward',
                   'next_state', 'done'))

def play_control_game():
    total_rewards = []
    agent.epsilon = 0
    for e in range(EPISODES):
        state = env.reset()
        for i in range(1000):
            action = agent.choose_action(state)
            next_state, reward, done, _, info = env.step(action)
            agent.remember(Transition(state, action, reward,
                                      next_state, done))
            state = next_state
            if done:
                total_rewards.append(reward)
                # print(f'Episode: {e}/{EPISODES}, Total reward: {reward}')
                break

    # plot_learning_history(total_rewards)
    print("Разница с опонентом: ", total_rewards.count(1) - total_rewards.count(-1))
    print("Выиграно партий: ", total_rewards.count(1))
    print("Проиграно партий: ", total_rewards.count(-1))
    print("Исход НИЧЬЯ: ", total_rewards.count(0))
    print("Исход каждой партии: ", total_rewards)

def learning_session(total_moves, update_neuro_freq, learn_freq):
    state = env.reset()
    # Filling up the replay-memory
    for i in range(1, total_moves + 1):
        if i % 1000 == 0:
            print(i)
        action = agent.choose_action(state)
        next_state, reward, done, _, _ = env.step(action)
        agent.remember(Transition(state, action, reward,
                                  next_state, done))
        if done:
            state = env.reset()
        else:
            state = next_state[:]

        if i % learn_freq == 0:
            agent.replay(batch_size)
        if i % update_neuro_freq == 0:
            agent.update_model()
            agent.save_nn_model()



# General settings
EPISODES = 100
init_replay_memory_size = 100000
update_neuro = init_replay_memory_size /400
learn = update_neuro / 2
batch_size = int(learn * 0.8)

if __name__ == '__main__':
    env = GridWorldEnv("rgb_array", 9)
    agent = Agent(env, max_memory_size=int(learn))
    start_time = time.time()
    # learning_session(init_replay_memory_size, update_neuro, learn)
    # agent.save_nn_model()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Elapsed time: ', elapsed_time)
    play_control_game()



def plot_learning_history(history):
    fig = plt.figure(1, figsize=(14, 5))
    ax = fig.add_subplot(1, 1, 1)
    episodes = np.arange(len(history)) + 1
    plt.plot(episodes, history, lw=0,
             marker='o', markersize=2)
    ax.tick_params(axis='both', which='major', labelsize=15)
    plt.xlabel('Episodes', size=20)
    plt.ylabel('Total rewards', size=20)
    plt.show()

    # start_time = time.time()
    # Filling up the replay-memory
    # for i in range(1, init_replay_memory_size+1):
    #     if i % 1000 == 0:
    #         print(i)
    #     action = agent.choose_action(state)
    #     next_state, reward, done, _, _ = env.step(action)
    #     agent.remember(Transition(state, action, reward,
    #                               next_state, done))
    #     if done:
    #         state = env.reset()
    #     else:
    #         state = next_state[:]
    #
    #     if i % learn == 0:
    #         agent.replay(batch_size)
    #     if i % update_neuro == 0:
    #         agent.update_model()
