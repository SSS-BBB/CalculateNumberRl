from stable_baselines3.common.env_checker import check_env
from calculate_num_env import CalculateNumEnv

env = CalculateNumEnv()

check_env(env)