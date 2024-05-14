import gymnasium as gym
from calculate_num_env import CalculateNumEnv
from stable_baselines3 import PPO

env = CalculateNumEnv(display=True)

model_path = "models/PPO/1715687766/160000.zip"
model = PPO.load(model_path, env=env)

episodes = 10

for episode in range(episodes):
    obs, info = env.reset()
    done = False
    
    while not done:
        action, _ = model.predict(obs)
        obs, reward, done, _, info = env.step(action)
        # print(reward)
        input("Press any key to continue")

env.close()