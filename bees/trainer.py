""" Example of using two different training methods at once in multi-agent. """
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import json

from typing import Dict, Tuple, Any

import gym
import ray
from ray.rllib.agents.ppo.ppo import PPOTrainer
from ray.rllib.agents.ppo.ppo_policy import PPOTFPolicy
from ray.tune.logger import pretty_print
from ray.tune.registry import register_env

from main import create_env

# pylint: disable=invalid-name
if __name__ == "__main__":
    ray.init()

    # Get ``settings`` file for now.
    settings_file = sys.argv[1]
    with open(settings_file, "r") as f:
        settings = json.load(f)

    env_config = settings["env"]
    time_steps = env_config["time_steps"]

    space_env = create_env(settings)
    env = create_env(settings)

    # Register environment
    register_env("bee_world", lambda _: env)

    # Build environment instance to get ``obs_space``.
    obs_space = space_env.observation_space
    act_space = space_env.action_space

    # You can also have multiple policies per trainer, but here we just
    # show one each for PPO and DQN.
    policies: Dict[str, Tuple[Any, gym.Space, gym.Space, Dict[Any, Any]]] = {
        "0": (PPOTFPolicy, obs_space, act_space, {}),
        "1": (PPOTFPolicy, obs_space, act_space, {}),
        "2": (PPOTFPolicy, obs_space, act_space, {}),
        "3": (PPOTFPolicy, obs_space, act_space, {}),
        "4": (PPOTFPolicy, obs_space, act_space, {}),
        "5": (PPOTFPolicy, obs_space, act_space, {}),
        "6": (PPOTFPolicy, obs_space, act_space, {}),
        "7": (PPOTFPolicy, obs_space, act_space, {}),
        "8": (PPOTFPolicy, obs_space, act_space, {}),
        "9": (PPOTFPolicy, obs_space, act_space, {}),
    }
    
    def policy_mapping_fn(agent_id: int) -> str:
        """ Returns the given agent's policy identifier. """
        return str(agent_id)
    
    ppo_trainer = PPOTrainer(
        env="bee_world",
        config={
            "multiagent": {
                "policies": policies,
                "policy_mapping_fn": policy_mapping_fn,
                "policies_to_train": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
            },
            "simple_optimizer": True,
            # Disable filters, otherwise we would need to synchronize those
            # as well to the DQN agent.
            "observation_filter": "NoFilter",
            "num_workers": 2,
            "num_gpus": 1,
            "train_batch_size": 2,
            "sample_batch_size": 1,
            "sgd_minibatch_size": 2,
        },
    )
    # You should see both the printed X and Y approach 200 as this trains:
    # info:
    #   policy_reward_mean:
    #     dqn_policy: X
    #     ppo_policy: Y
    for i in range(time_steps):
        print("== Iteration", i, "==")

        # Improve the PPO policy.
        print("-- PPO --")
        print(pretty_print(ppo_trainer.train()))
