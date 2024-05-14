import gymnasium as gym
import numpy as np
from gymnasium import spaces
import random

MAX_TARGET_NUM = 100
MAX_GIVEN_NUM = 100
MAX_STEP = 50

class CalculateNumEnv(gym.Env):

    metadata = {"render_modes": ["human"], "render_fps": 0}

    def __init__(self, display=False):
        super().__init__()

        self.display = display

        self.action_space = spaces.Discrete(5) # +, -, *, /, give up

        self.observation_space = spaces.Box(low=-np.inf, high=np.inf,
                                            shape=(3, ), dtype=np.int64)

    def step(self, action):
        self.current_step += 1
        self.last_result = self.current_result
        # actions: 0 -> +,
        #          1 -> -,
        #          2 -> *,
        #          3 -> /,
        #          4 -> give up,
       
        match(action):
            case 0:
                self.current_result += self.given_num
                self.sign = "+"
                if (self.display):
                    print("Choose +")
            case 1:
                self.current_result -= self.given_num
                self.sign = "-"
                if (self.display):
                    print("Choose -")
            case 2:
                self.current_result *= self.given_num
                self.sign = "*"
                if (self.display):
                    print("Choose *")
            case 3:
                self.current_result /= self.given_num
                self.sign = "/"
                if (self.display):
                    print("Choose /")
            case 4:
                self.give_up = True
                if (self.display):
                    print("Choose give up")
        if (not self.give_up):
            self.history.append(f"{self.last_result} {self.sign} {self.given_num} = {self.current_result}")
        
        self.set_reward()
        self.check_done()

        self.given_num = random.randint(1, MAX_GIVEN_NUM)
        self.set_obs()

        self.display_game()

        info = { 
                    "target_num": self.target_num,
                    "given_num": self.given_num,
                    "current_result": self.current_result,
                    "history": self.history
               }

        return self.observation, self.reward, self.done, self.truncated, info

    def reset(self, seed=None, options=None):
        self.target_num = random.randint(1, MAX_TARGET_NUM)
        self.given_num = random.randint(1, MAX_GIVEN_NUM)
        self.current_result = random.randint(1, MAX_GIVEN_NUM)
        self.reward = 0
        self.done = False
        self.truncated = False
        self.current_step = 0
        self.give_up = False
        self.history = []
        self.sign = ""

        self.set_obs()
        info = {}

        self.display_game()

        return self.observation, info
    
    def set_obs(self):
        self.observation = np.array([self.target_num, self.given_num, self.current_result])

    def set_reward(self):
        if (abs(self.current_result - self.target_num) < 0.01):
                self.reward = 100
                return

        if (not self.give_up):
            divider = abs(self.target_num - self.current_result)
            self.reward = -0.1 + 1/divider
        else:
            divider = abs(self.target_num - self.current_result) / 10
            self.reward = -3.3 + 1/divider

        self.reward = float(self.reward)

    def display_game(self):
        if (self.display):
            if (not self.give_up):
                print("Target Number:", self.target_num)
                print("Given Number:", self.given_num)
                print("Result:", self.current_result)
                print("History:")
                for h in self.history:
                    print(h)
                print("------------------------------")

            if (self.done):
                print("------------------------------")
                print(f"Target number: {self.target_num}")
                print(f"Last result: {self.current_result}")
                print("------------------------------")

    def check_done(self):
        self.truncated = False
        if (abs(self.current_result - self.target_num) < 0.01 or self.give_up):
            self.done = True
        else:
            if (self.current_step > MAX_STEP):
                self.done = True
                self.truncated = True
            else:
                self.done = False