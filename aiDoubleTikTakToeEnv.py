import base64
import os
import time
from collections import deque
from io import BytesIO

import sys
import time

from doubletiktaktoe import DoubleTikTakToe

from stable_baselines3.common.policies import ActorCriticPolicy

import gym
import numpy as np
from PIL import Image
from gym import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.vec_env import SubprocVecEnv

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

class EnvironmentNoVsDoubleTikTakToe(gym.Env): # TikTakToe Trainingsumgebung
    """Custom Environment that follows gym interface"""

    def __init__(self, rendering): # Trainingseinheit initialisieren
        super(EnvironmentNoVsDoubleTikTakToe, self).__init__()
        self.action_space = spaces.Discrete((2,2,2,2),)
        self.observation_space = spaces.Box(low=-255, high=+255, shape=(3,3,3,3), dtype=np.uint8)
        self.ttt = DoubleTikTakToe()

    def step(self, action: int): # Einen Move machen
        state, forceField, game_board, event = self.ttt.place(action)
        self.done = False
        if state == 10:
            self.reward = 30
            self.done = True
        elif state == 8:
            self.reward = -1
        elif state == 7:
            self.reward = 1
        elif state == 9:
            self.reward = -1
        elif state == 1:
            self.reward = 2000
            self.done = True
        state, forceField, game_board, event = self.ttt.rndPlace()
        if state == 10:
            self.reward = self.reward -30
            self.done = True
        elif state == 8:
            self.reward = self.reward + 1
        elif state == 7:
            self.reward = self.reward -1
        elif state == 9:
            self.reward = self.reward + 1
        elif state == 1:
            self.reward = self.reward -2000
            self.done = True

        self.observation = game_board
        self.observation = np.array(self.observation)

        self.board = game_board

        info = {}
        return self.observation, self.reward, self.done, info

    def reset(self): # Zurücksetzung der Trainingsumgebung für nächsten Durchgang
        self.ttt.settings()
        game_board = [[[[0 for l in range(3)] for k in range(3)] for j in range(3)] for i in range(9)]
        self.board = game_board
        self.observation = game_board
        self.observation = np.array(self.observation)
        return self.observation  # reward, done, info can't be included

    def render(self, mode: str = 'human'): # Gibt Feld aus
        if mode == 'human':
            """
            Print the board on console
            :param state: current state of the board
            """
            chars = {
                +1: "X",
                -1: "O",
                0: ' '
            }
            str_line = '---------------'
            print('\n' + str_line)
            for row in self.board:
                for cell in row:
                    symbol = chars[cell]
                    print(f'| {symbol} |', end='')
                print('\n' + str_line)

    def close (self): # Nicht verwendet
        ...

from tqdm import tqdm

if __name__ == '__main__': # Ausführung des Trainingsprozesses oder Testen der KI
    env_lambda = lambda: EnvironmentNoVsDoubleTikTakToe(False)
    do_train = True # Legt fest ob die KI Trainiert wird
    num_cpu = 24 # Anzahl Trainingsinstanzen
    save_path = "cli_ttt_ppo_cnn_1980000_rnd_steps.zip"
    load_path = "cli_ttt_ppo_cnn_1980000_rnd_steps"
    if do_train == True:
        env = SubprocVecEnv([env_lambda for i in range(num_cpu)]) # Trainiert mit der festgelegten Anzahl Trainingsinstanzen
    else:
        env = EnvironmentNoVsDoubleTikTakToe(True) # Führt eine einzelne Distanz zu demonstrationszwecken aus
# Training
    if do_train:
        checkpoint_callback = CheckpointCallback(
            save_freq=196608,
            save_path='./.checkpoints/',
            name_prefix=save_path,
        )
        model = PPO(
            ActorCriticPolicy,
            env,
            verbose=1,
            tensorboard_log="./.tb_clittt_env/",
        )
        model.learn(
            total_timesteps=196608,
            callback=[checkpoint_callback]
        )
        model.save(save_path)

    model = PPO.load('./.checkpoints/'+save_path, env=env)

    print(model)
# Demonstration
    obs = env.reset()

    model.env.render()

    for i in tqdm(range(500)):
        time.sleep(4)
        action, _states = model.predict(obs, deterministic=True)
        obs, rewards, dones, info = env.step(action)

        env.render()

        # img = env.render(mode='rgb_array')

    # imageio.mimsave('dino.gif', [np.array(img) for i, img in enumerate(images)], fps=15)
    time.sleep(5)
    exit()
