from pysc2.lub import features
import numpy as np


class Unit(object):
    def __init__(self, location=(0, 0)):
        self.location = np.array(location)


class RegistryException(Exception):
    def __init__(self):
        super().__init__()


class Registry(object):
    def __init__(self, obs):
        self.objects = {}
        self.obs = obs

    def __enter__(self):
        self.update(self.obs)
        return self

    def __exit__(self, type, value, traceback):
        pass

    def update(self, obs):
        selection = obs.observation["screen"][features.SCREEN_FEATURES.selected.index]
        self.objects["selection"] = selection

        player_relative = obs.observation["screen"][features.SCREEN_FEATURES.player_relative.index]

        player_y, player_x = (player_relative == 1).nonzero()
        self.objects["self"] = [Unit(x, y) for x, y in zip(player_x, player_y)]

        player_y, player_x = (player_relative == 2).nonzero()
        self.objects["ally"] = [Unit(x, y) for x, y in zip(player_x, player_y)]

        player_y, player_x = (player_relative == 3).nonzero()
        self.objects["neutrals"] = [Unit(x, y)
                                    for x, y in zip(player_x, player_y)]

        player_y, player_x = (player_relative == 3).nonzero()
        self.objects["hostile"] = [Unit(x, y)
                                   for x, y in zip(player_x, player_y)]

    def query(self, object_type):
        try:
            return self.objects[object_type]
        except Exception:
            print("Object not in Registry")
            return None
