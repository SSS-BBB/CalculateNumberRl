import gymnasium as gym
from calculate_num_env import CalculateNumEnv

env = CalculateNumEnv(display=True)

episodes = 1

for episode in range(episodes):
    env.reset()
    done = False
    
    while True:
        action = int(input("Choose an operation: "))
        obs, reward, done, _, info = env.step(action)
        print(reward)
        print("------------------------")
        if done:
            break