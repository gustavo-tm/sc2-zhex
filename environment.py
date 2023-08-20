import gym
import numpy as np
from game import Game
import random

class Environment(gym.Env):
    def __init__(self, render_mode = None, default_settings = True, print_build = False, max_time = 600):
        self.actions = {
            0: "slow",
            1: "extractor",
            2: "strike"
        }
        self.default_setting = default_settings
        self.print_build = print_build
        self.max_time = max_time

    def observe(self):
        observation = np.array([
            self.game.income_m,
            self.game.nstructures_type0,
            self.game.nstructures_type1,
            self.game.supply,
            self.game.supply_cost,
            self.game.nsupply,
            #under construction
        ])

        return observation

    def reset(self, seed = None, show = False):

        if self.default_setting:
            self.game = Game(show = show)
        else:
            start_configs = {
                "supply_cost": 600,
                "supply": round(random.random() * (54 * 2)),
                "extractors": round(random.random() * (12 * 2) + 1),
                "spawners": round(random.random() * (24 * 2) + 1),
                "income_flat": 160,
                "spawner_buff": 30
            }
            self.game = Game(show = show, start_config = start_configs)

        return self.observe()

    def step(self, action):
        old_score = self.game.income_m
        self.game.build(self.actions[action])
        reward = self.game.income_m - old_score
        terminated = self.game.time > self.max_time
        info = {"time": self.game.time}

        if self.print_build:
            print(action)

        return self.observe(), reward, terminated, info
