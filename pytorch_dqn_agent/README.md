# StarCraft agent PyTorch

While there has been plently of development in terms of environments for
StarCraft II, for example Deepmind's [pysc2](https://github.com/deepmind/pysc2) and Facebook's [TorchCraft](https://github.com/TorchCraft/TorchCraft), there have been relatively little development within usability of these APIs.

The goal of this project is to provide a higher level API to pysc2 for
the development of reinforcement learning agents. Initially with a focus on PyTorch, a framework agnostic library is to be preferred. The library will
contain:

* **startorch**: A high-level API for most basic states and actions
  present in the game

* **agents**: Example premade agents that make use of the startorch for
  common minigames such as *move to beacon* and *gather resources*.
