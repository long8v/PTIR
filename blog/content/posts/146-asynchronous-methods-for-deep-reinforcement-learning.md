---
title: "[134] Asynchronous Methods for Deep Reinforcement Learning"
date: 2023-10-18
tags: ['2016', 'DeepMind', 'RL']
paper: "https://arxiv.org/pdf/1602.01783.pdf"
issue: 146
issueUrl: "https://github.com/long8v/PTIR/issues/146"
summary: "Recommended reading for my fall class at Namjong University - seemingly simple idea at this point, good performance"
---
<img width="679" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8fbd0472-8614-4760-8eb5-bf50b1cbfad7">

[paper](https://arxiv.org/pdf/1602.01783.pdf)

## TL;DR
- **I read this because.. :** Recommended for my fall semester class at Namjong University
- **task :** Deep Reinforcement Learning 
- **problem :** online RL is unstable. To solve this, things like replay buffer (getting s, a, s' from the previous trasition) were devised, but they are specific to off-line RL algorithms
- **IDEA :** Let's run multiple agents in parallel and batch update them!
- **input/output :** trajectory / policy 
- **architecture :** one-step Q-learning, one-step Sarsa, multi-step Q-learning, proposed A3C(actor-critic). Value or policy network is configured as FFN or LSTM
- **objective :** advantage (value based) when following policy $\phi$, expectation of reward (policy based) when following policy + entropy of policy is added to loss term, which is more stable.
- **baseline :** one-step Q-learning, one-step Sarsa, multi-step Q-learning, advantage actor-critic
- **data :** Atari 2600, TORCS, Mujoco, Labyrinth
- **evaluation :** score, data efficiency, stability 
- **result :** High score. Fast convergence. Higher performance (data efficiency) with fewer training steps. He only uses CPU multi core while others only use GPU.
- **contribution :** A seemingly simple idea with good performance at this point.
- **etc. :** The famous A3C is this... RL is a model name that is full of individuality.. gorilla, REINFORCE, A3C, ...

## Details
### introduction
- Problems with data encountered by online RL agents
- non-stationary: Normality in a time series? Does the distribution vary with time step?
- strongly correlated: This is also what we say in time series: how is t related to the previous time step (t-1)?
The solution to this was to use a replay buffer, data batched, and randomly sample for different time steps.
But this naturally limits us to off-policy methods. Because the previous transition is the result of following the previous policy

### Reinforcement Learning Background 
What we want to do in RL is to maximize $R_t=\sum_{k=0}^{\infty} Maximize $\gamma^k r_{t+k}$!

The action value Q is then expressed as $Q^\pi (s) = \mathbb{E}[R_t|s_t =s, a]$, which is the expected value of the sum of rewards for taking action a in state s when following policy $\pi$.
The value of state s is similarly expressed as follows $V^\pi (s) = \mathbb{E}[R_t|s_t =s ] $ is the expected value of the sum of reward in state s when policy $\pi$ is followed.

That's it for the basic settings in RL!
Here, a value-based model-free method would directly approximate $Q(s,a;\theta)$ as an NN. This is Q-learning.
Then we can directly approximate the optimal $Q^*(s,a)$ with the NN's parameter $\theta$. In this case, our loss is
<img width="310" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2072ea7e-9276-4121-9ee5-cdbf6101b009">
~Ah, I'm a little confused... If I find $\theta$ that maximizes a' that transitions from state s, a, to s', which maximizes a, can I also find policy, or just find Q and use it for what? If I find Q, then policy is automatically found (because I just need to find a that maximizes Q?)~.
~RL always has a policy network! Q is an approximation of the reward after time (t+1)!
In q-learning, network is set implicitly. Not that there is a separate policy network. My original understanding is correct (24.08.21)

The disadvantage of Q-learning is that only the (s, a) pairs that get rewards are directly affected, while other (s, a) pairs are indirectly affected, resulting in slow learning. To solve this problem, n-step Q-learning is proposed, which is like applying a discount ratio $\gamma$ to influence the current reward until another time step.
<img width="318" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/455bc139-d2f9-48c3-bf2c-fafa89ab6412">

This will allow a single reward $r$ to directly affect the previous state action pair as well.

In contrast, policy-based models directly parametrize the policy $\pi(a|s, \theta)$. The loss in this case is $\mathbb{E}[R_t]$ (gradient ascent)
REINFOCE-like functions do this, where $\theta$ is obtained as follows, and
<img width="120" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/412a224b-5ed1-423a-b1cc-6514b93b92bc">

This is a high variance, so we subtract the bias term to lower it.
<img width="184" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/99ed0561-014a-4f1f-a080-79029cfbfd96">

If we approximate this bias term with V, we get even lower variance, which is the actor-critic architecture.
<img width="103" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a56151e3-9b38-4bee-89bc-16413aa6ac2a">

### Asynchronous RL Framework
You can use multi-thread to make it asynchronous.
- The pseudo-code for one-step Q-learning is shown below.
<img width="335" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4d0931b2-ec47-4638-a494-3e6c9733cd6b">

Nothing much, just grad accum until there are T threads and then update them all at once~.

- n-step Q-Learning 
<img width="596" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/81028dd4-2ff8-4835-a7bf-449245933539">

<img width="328" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9b67ab52-42b3-4c23-95a7-738a0b7a525b">

I don't know what the above means, it goes to the future when it should go to the past...?
It seems to explore until $t_max$ and then update all at once.

- Asynchronous advantage actor-critic
Add multi-thread to advantage actor-critic + Add entropy from policy to Loss
<img width="596" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ca3623a3-982c-4bdc-b97d-ed1623ce0cd5">

Learning uses RMSProp

### Result 
<img width="685" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0168e7bf-8e1a-49bf-9b9f-b420f765acc6">

- Data Efficiency
<img width="673" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5a1963fe-eef8-409e-946f-6fd2208100ec">

In theory, the same performance should be achieved with the same number of samples. But we use multi-threaded, so using 4 threads reduces the wall-clock time by 4 times!
An additional surprise was that the Q-learning and sarsa algorithms performed better for the same number of samples. by reducing bias than the one-step method?