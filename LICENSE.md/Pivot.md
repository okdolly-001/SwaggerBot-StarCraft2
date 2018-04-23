# [Projects suggested by DeepMind](https://github.com/deepmind/pysc2/blob/master/docs/mini_games.md)

>This is our current project statement:
>*"The agent uses iterations where the state of the game will be determined by a set of parameters that describe the current units/building/tech status of the player, then learn the most effective action to maximize its score at each of the states through reinforcement learning."*
>
>I think "maximize its score at each of the states" is not concrete enough.  What states and what actions are we talking about? 
>Here, "**spend your resources and what to build at what time,**"
>This is vague and ambitiou, which agent and what are we building.
>We want to create a very specific agent that does one task spectacularly well.

### I suggest we choose one of these mini-projects suggested by DeepMind to work. DeepMind suggest these mini-games precisely because they now how complex it is to create a general agent that can master all the tasks involved in the game. These two are most relevant to what we talked about, but if you think another one in this file [Projects suggested by DeepMind](https://github.com/deepmind/pysc2/blob/master/docs/mini_games.md) is realistic, let's have a group vote.

###
## MoveToBeacon

#### Description

A map with 1 Marine and 1 Beacon. Rewards are earned by moving the marine to the
beacon. Whenever the Marine earns a reward for reaching the Beacon, the Beacon
is teleported to a random location (at least 5 units away from Marine).

#### Initial State

*   1 Marine at random location (unselected)
*   1 Beacon at random location (at least 4 units away from Marine)

#### Rewards

*   Marine reaches Beacon: +1

#### End Condition

*   Time elapsed

#### Time Limit

*   120 seconds

#### Additional Notes

*   Fog of War disabled
*   No camera movement required (single-screen)


## CollectMineralShards

#### [](https://github.com/deepmind/pysc2/blob/master/docs/mini_games.md#description-1)Description

A map with 2 Marines and an endless supply of Mineral Shards. Rewards are earned by moving the Marines to collect the Mineral Shards, with optimal collection requiring both Marine units to be split up and moved independently. Whenever all 20 Mineral Shards have been collected, a new set of 20 Mineral Shards are spawned at random locations (at least 2 units away from all Marines).

#### [](https://github.com/deepmind/pysc2/blob/master/docs/mini_games.md#initial-state-1)Initial State

-   2 Marines at random locations (unselected)
-   20 Mineral Shards at random locations (at least 2 units away from all Marines)

#### [](https://github.com/deepmind/pysc2/blob/master/docs/mini_games.md#rewards-1)Rewards

-   Marine collects Mineral Shard: +1

#### [](https://github.com/deepmind/pysc2/blob/master/docs/mini_games.md#end-condition-1)End Condition

-   Time elapsed

#### [](https://github.com/deepmind/pysc2/blob/master/docs/mini_games.md#time-limit-1)Time Limit

-   120 seconds

#### [](https://github.com/deepmind/pysc2/blob/master/docs/mini_games.md#additional-notes-1)Additional Notes

-   Fog of War disabled
-   No camera movement required (single-screen)
-   This is the only map in the set to require the Liberty (Campaign) mod, which is needed for the Mineral Shard unit.
