from pysc2.lib import actions
from .base import action
from .registry import Unit
import numpy as np


@action(actions.FUNCTIONS.Move_screen.id)
def move(target):
    if type(target) is Unit:
        target = target.location

    if type(target) is list:
        ys, xs = [], []
        for u in target:
            x, y = u.location
            xs.append(x)
            ys.append(y)

        target = [int(np.mean(xs)), int(np.mean(ys))]

    return [[0], target]


@action(actions.FUNCTIONS.select_army.id)
def select(target):
    if target is "all":
        target = [0]
    return [target]
