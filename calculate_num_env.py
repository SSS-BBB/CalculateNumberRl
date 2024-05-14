import gymnasium as gym
import numpy as np
from gymnasium import spaces
import random
from collections import deque

MAX_TARGET_NUM = 100
MAX_GIVEN_NUM = 100
MAX_STEP = 50

class GuessNumEnv(gym.Env):

    metadata = {"render_modes": ["human"], "render_fps": 0}

    def __init__(self, display=False):
        super().__init__()

        self.display = display

        self.action_space = spaces.Discrete(4) # +, -, *, /

        self.observation_space = spaces.Box(low=-np.inf, high=np.inf,
                                            shape=(3, ), dtype=np.int64)

    def step(self, action):
        if (self.display):
            self.display_game()
        self.current_step += 1
        # actions: 0 -> +,
        #          1 -> -,
        #          2 -> *,
        #          3 -> /,
        match(action):
            case 0:
                self.current_result += self.given_num
            case 1:
                self.current_result -= self.given_num
            case 2:
                self.current_result *= self.given_num
            case 3:
                self.current_result /= self.given_num

        if (self.display):
            self.display_game()
        
        self.set_obs()
        self.set_reward()
        self.check_done()

        info = { 
                    "num_state": self.num_state,
                    "last_guesses": list(self.last_guesses),
                    "last_states": list(self.last_states)
               }

        return self.observation, self.reward, self.done, self.truncated, info

    def reset(self, seed=None, options=None):
        self.target_num = random.randint(1, MAX_TARGET_NUM)
        self.given_num = random.randint(1, MAX_GIVEN_NUM)
        self.current_result = self.given_num
        self.reward = 0
        self.done = False
        self.truncated = False
        self.current_step = 0

        self.set_obs()
        info = {}

        return self.observation, info
    
    def set_obs(self):
        self.observation = np.array([self.target_num, self.given_num, self.current_result])

    def set_reward(self):
        pass

    def display_game(self):
        pass

    def check_done(self):
        self.truncated = False
        if (abs(self.current_result - self.target_num) < 0.01):
            self.done = True
        else:
            if (self.current_step > MAX_STEP):
                self.done = True
                self.truncated = True
            else:
                self.done = False