Github: https://github.com/rhyslee/PYSC2-Replay-Extractor

# PYSC2-replay-extractor

Build upon pysc2 pysc2-replay and parse-pysc2-replay-files.

This tool extracts player's cumulative score, resources, actions, minimap, and visibility.

require StarCraftII 3.16



# Example

This will execute a function `step` in `ObserverAgent.ObserverAgent` for each step in the replay.

	$ python3 transform_replay.py --replays ~/StarCraftII/Replays/ --agent ObserverAgent.ObserverAgent

Will put extracted files under `data/`

To inspect the extracted files, make use of `testLoadPickle.py`, remember to change the path variable in the file.

	$ python3 testLoadPickle.py

