""" Runs the environment and trains the agents for a number of timesteps. """
import sys
import os
import json
import time

from env import Env


def main(settings):
    """ Main training loop. """

    env_config = settings["env"]
    width = env_config["width"]
    height = env_config["height"]
    sight_len = env_config["sight_len"]
    obj_types = env_config["obj_types"]
    num_agents = env_config["num_agents"]
    aging_rate = env_config["aging_rate"]
    food_density = env_config["food_density"]
    food_size_mean = env_config["food_size_mean"]
    food_size_stddev = env_config["food_size_stddev"]
    time_steps = env_config["time_steps"]

    rew_config = settings["rew"]
    n_layers = rew_config["n_layers"]
    hidden_dim = rew_config["hidden_dim"]
    reward_weight_mean = rew_config["weight_mean"]
    reward_weight_stddev = rew_config["weight_stddev"]

    consts = settings["constants"]

    env = Env(
        width,
        height,
        sight_len,
        obj_types,
        num_agents,
        aging_rate,
        food_density,
        food_size_mean,
        food_size_stddev,
        n_layers,
        hidden_dim,
        reward_weight_mean,
        reward_weight_stddev,
        consts,
    )
    env.reset()
    print(env)
    time.sleep(0.2)

    for _ in range(time_steps):

        action_dict = env.get_action_dict()
        _obs, _rew, done, _info = env.step(action_dict)

        # Print out environment state
        os.system("clear")
        print(env)
        time.sleep(1)
        if all(done.values()):
            print("All agents have died.")
            break


# pylint: disable=invalid-name
if __name__ == "__main__":

    settings_file = sys.argv[1]
    with open(settings_file, "r") as f:
        SETTINGS = json.load(f)
    main(SETTINGS)
