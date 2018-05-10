# SwaggerBot-StarCraft2
A basic StarCraft agent operating in Deepmind's Pysc environment
# StarCraft II Project

Feel free to edit.




## Timeline


#### Week six : 5.10-5.17

##### Assume you have already completed all the tasks in Week one. Parkinson's law says that a task takes as much time as you allocate for it. Deadline is a productivity booster because we don't check the phone every 20 minutes or hang out with friends between now and the deadline. Aim to complete the task less than the estimated time. Sucess = Focus * Time

>##### If you have already mastered TensorFlow, then go ahead and write code. 

>##### For those of you who don't know TensorFlow, Keras or PyTorch. Why PyTorch instead of TensorFlow, which has multiple existing implementations of Starcraft agent? Four reasons. First, I used TensorFlow for a Udacity Self-driving project, it was a very unpleasant experience. TF is very verbose and hard to debug. Second, I went to a Kaggle Grandmaster panel last quarter, they told me that they all use PyTorch instead of TF. Third, PyTorch is beginner-friendly. It resembles Numpy. Four, there are plenty implementations of RL algorithms in PyTorch. We just need to translate TF implementations of Starcraft agent into PyTorch. If we can't learn things fast enough to build things in short period of time, then we can't survive the AI age. 

1. PyTorch is more beginner-friendly than TensorFlow and more flexible than Keras. Go through the official tutorials for beginners: [Deep Learning with PyTorch: A 60 Minute Blitz](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html),[Learning PyTorch with Examples](https://pytorch.org/tutorials/beginner/pytorch_with_examples.html) and [Data Loading and Processing Tutorial](https://pytorch.org/tutorials/beginner/data_loading_tutorial.html). ***Estimated time: 6-7 hrs.***

2. Go through PyTorch's official [Reinforcement Learning (DQN) tutorial](https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html). ***Estimated time: 1-2 hrs.***

3. Reference point: [Morvan's PyTorch tutorials  ](https://github.com/MorvanZhou/PyTorch-Tutorial/tree/master/tutorial-contents-notebooks). He breaks down PyTorch into individual topics, such as Activation, CNN. Each Jupyter notebook is super short and easily digestible. You can check out the individual topics when running into roadblocks. No need to go through all at once.


4. Please please read these two tutorials [Introduction to Various Reinforcement Learning Algorithms. Part I (Q-Learning, SARSA, DQN, DDPG)(at least read this)](https://towardsdatascience.com/introduction-to-various-reinforcement-learning-algorithms-i-q-learning-sarsa-dqn-ddpg-72a5e0cb6287) and [Introduction to Various Reinforcement Learning Algorithms. Part II (TRPO, PPO)](https://towardsdatascience.com/introduction-to-various-reinforcement-learning-algorithms-part-ii-trpo-ppo-87f2c5919bb9). Or else you won't understand step 5 onwards. ***Estimated time: 4-6 hrs.***
>  **Optional:**  Ideally, you should have a basic but comprehensive understanding of reinforcement learning as a field, but due to time constraint, just understand the gist of these two posts would suffice. Check out the links under each subtopic in [my blog post](http://www.dollyye.com/) if you want to have an in-depth understanding of RL. Estimated time: 8-10 hrs.

5. Have a basic idea of these three algorithms:
     An [OpenAI blog post](https://blog.openai.com/openai-baselines-ppo/) that gives you a broad overview.
     
   - [Advantage Actor Critic (A2C)](https://hackernoon.com/intuitive-rl-intro-to-advantage-actor-critic-a2c-4ff545978752) . This is the best introduction to A2C; and it is a cartoon story about a fox! Hooray! ***Estimated time: 0.5-1 hrs.***

   - [Proximal Policy Optimization (PPO)](https://towardsdatascience.com/introduction-to-various-reinforcement-learning-algorithms-part-ii-trpo-ppo-87f2c5919bb9) (this is hard, I think the author assumes that you already understand policy ...gradients. Estimated time: 8-10 hrs. ***Estimated time: 2 hrs.***

   -  [Scalable trust-region method for deep reinforcement learning using Kronecker-factored approximation (ACKTR)](https://arxiv.org/pdf/1708.05144.pdf). This the OpenAI paper, so you can just skim each sub-title. ***Estimated time: 0.5 hrs.***


6. Steps 1-5 prepares us for [PyTorch implementation of Advantage Actor Critic (A2C), Proximal Policy Optimization (PPO) and Scalable trust-region method for deep reinforcement learning using Kronecker-factored approximation (ACKTR)](https://github.com/ikostrikov/pytorch-a2c-ppo-acktr).Note how different modules work together (agent, model, etc). Don't be discouraged when you don't understand, keep going. ***Estimated time: 6-10 hrs.***
>  **Note:**  Understand the code is very challenging but this is the crux of how we are going to train the StarCraft agent. 


7. Translate this [TF implementation of A2C Starcraft agent](https://github.com/simonmeister/pysc2-rl-agents/blob/master/rl/agents/a2c/agent.py) into PyTorch. Culmination of Step 1 - 6.


This is a lot, spend a 20- 30 hours, prepare to pull all-nighters. If we don't learn it now, we will never learn it.



> Written with [StackEdit](https://stackedit.io/).

#### Week four : 4.22-4.29
1.Understand what PySC2 API allows us to do by reading [PySC2 implementations](https://github.com/deepmind/pysc2) and this [DeepMind paper](https://deepmind.com/documents/110/sc2le.pdf) . 

>  **Important:** Look at the [action.py](https://github.com/deepmind/pysc2/blob/cad5a011492372abf484bd7a8cc69e7ed24b8d8c/pysc2/lib/actions.py). <br/>

2.Understanding every line of the code in all the files in this [Github tutorial](https://github.com/skjb/pysc2-tutorial). This an accompany [Medium post](https://chatbotslife.com/building-a-basic-pysc2-agent-b109cde1477c) for the Github repo.
Get all the agents from aforementioned tutorial up and running in your computer, so that you figure out how to create a simplge agent.<br/>
3.Finish the proposal.

4.Implement [A-Guide-to-DeepMind-s-StarCraft-AI-Environment](https://github.com/llSourcell/A-Guide-to-DeepMinds-StarCraft-AI-Environment). This might be more time-consuming as you need to download all the maps, but it shows the graphical dashboard about how the agent works.



### Must read

1.  [DEMYSTIFYING DEEP REINFORCEMENT LEARNING](http://neuro.cs.ut.ee/demystifying-deep-reinforcement-learning/)

2.  [_Part 0 — Q-Learning Agents_](https://medium.com/@awjuliani/simple-reinforcement-learning-with-tensorflow-part-0-q-learning-with-tables-and-neural-networks-d195264329d0)

3.  [_Part 1 — Two-Armed Bandit_](https://medium.com/@awjuliani/super-simple-reinforcement-learning-tutorial-part-1-fd544fab149)

4.  [_Part 1.5 — Contextual Bandits_](https://medium.com/@awjuliani/simple-reinforcement-learning-with-tensorflow-part-1-5-contextual-bandits-bff01d1aad9c#.uzs1axw0s)

6.  [_Part 2 — Policy-Based Agents_](https://medium.com/@awjuliani/super-simple-reinforcement-learning-tutorial-part-2-ded33892c724)

6.  [_Part 3 — Model-Based RL_](https://medium.com/@awjuliani/simple-reinforcement-learning-with-tensorflow-part-3-model-based-rl-9a6fe0cce99)

7.  [_Part 4 — Deep Q-Networks and Beyond_](https://medium.com/@awjuliani/simple-reinforcement-learning-with-tensorflow-part-4-deep-q-networks-and-beyond-8438a3e2b8df#.i2zpbmre8)

8.  [_Part 5 — Visualizing an Agent’s Thoughts and Actions_](https://medium.com/@awjuliani/simple-reinforcement-learning-with-tensorflow-part-5-visualizing-an-agents-thoughts-and-actions-4f27b134bb2a)

9.  [_Part 6 — Partial Observability and Deep Recurrent Q-Networks_](https://medium.com/emergent-future/simple-reinforcement-learning-with-tensorflow-part-6-partial-observability-and-deep-recurrent-q-68463e9aeefc#.9djtshpqo)

10.  [_Part 7 — Action-Selection Strategies for Exploration_](https://medium.com/emergent-future/simple-reinforcement-learning-with-tensorflow-part-7-action-selection-strategies-for-exploration-d3a97b7cceaf#.qfg7lqxpr)

11.  [_Part 8 — Asynchronous Actor-Critic Agents (A3C)_](https://medium.com/@awjuliani/simple-reinforcement-learning-with-tensorflow-part-8-asynchronous-actor-critic-agents-a3c-c88f72a5e9f2#.hg13tn9zw)

12.  [Deep Deterministic Policy Gradients in TensorFlow](https://pemami4911.github.io/blog/2016/08/21/ddpg-rl.html#References)

### Github Repo

> **Authors of xhujoy/pysc2-agents [Reinforcement Learning Agent using Tensorflow (actorcritic)](https://github.com/xhujoy/pysc2-agents) and [pekaalto/sc2aibot (actorcritic)](https://github.com/pekaalto/sc2aibot) were the first to attempt replicating [1](https://deepmind.com/documents/110/sc2le.pdf) and their implementations were used as a general inspiration during development of this project, however their aim was more towards replicating results than architecture, missing key aspects, such as full feature and action space support. Authors of simonmeister/pysc2-rl-agents also aim to replicate both results and architecture, though their final goals seem to be in another direction. Their policy implementation was used as a loose reference for this project.**

 1.[Reinforcement Learning Agent using Tensorflow](https://github.com/xhujoy/pysc2-agents)
 
 2.[Supervised-End-to-end-Weight-sharing-for-StarCraft-II](https://github.com/tonybeltramelli/Supervised-End-to-end-Weight-sharing-for-StarCraft-II)
 
 3.[(D)RL Agent For PySC2 Environment. Close replication of DeepMind's SC2LE paper architecture.](https://github.com/Inoryy/pysc2-rl-agent)
reduced set of features (unified across all mini-games) or alternative approaches, such as HRL [3] or Auxiliary Tasks [4].
 
 4.[从头开始构建自己的星际二agent(Chinese)](https://github.com/wwxFromTju/sc2-101-zh) 
 
 5.[DQN agent](https://github.com/phraust1612/MinervaSc2)

 6.[Replay data documented here] (https://github.com/wuhuikai/MSC)
