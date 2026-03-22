---
title: "[168] Proximal Policy Optimization Algorithms"
date: 2024-08-21
tags: ['2017', 'RL']
paper: "https://arxiv.org/pdf/1707.06347"
issue: 187
issueUrl: "https://github.com/long8v/PTIR/issues/187"
summary: "Backgrounder - Simple and Intuitive LOSS... Actually, it became intuitive just by looking at this paper, so I don't even think I should have known the previous contents... lol"
---
<img width="703" alt="image" src="https://github.com/user-attachments/assets/ad3ddfeb-d439-4c96-b841-2353465edc1a">

[paper](https://arxiv.org/pdf/1707.06347)

## TL;DR
- **I read this because.. :** Background Tea
- **task :** RL 
- **problem :** q-learning is too unstable, trpo is relatively complicated. Is there a data efficient and sclable arch?
- **idea :** Use clipping instead of KL divergence term. Vary step size $\beta$ adaptively.
- **input/output :** state -> action 
- **architecture :** MLP 
- **objective :** $L^{CLIP}(\theta) = \hat{\mathbb{E}}_t \left[ \min(r_t(\theta)\hat{A}_t, \text{clip}(r_t(\theta), 1 - \epsilon, 1 + \epsilon)\hat{A}_t) \right]$
- **baseline :** loss(no clipping, KL penalty), A2C, CEM, TRPO
- **data :** OpenAI Gym(Mujoco), human control task(Roboschool), Atari
- **evaluation :** don't know
- **result :** good
- **contribution :** Simple and intuitive loss... Actually, this paper alone makes intuitive sense, so I don't even think I should have known the previous content... ㅎㅎ
- **etc. :**

## Details
### preliminary 
- policy gradient method
<img width="232" alt="image" src="https://github.com/user-attachments/assets/764d9bf8-cacd-4c12-9437-9784439ede96">

Derivative of the gradient over the policy network weighted by advantage
where E is a form of sampling and just taking the average

<img width="272" alt="image" src="https://github.com/user-attachments/assets/b7cab011-36d4-423a-aa6b-79e3f1e849c5">

loss should maximize the expected value of the weighted sum of advantages for trajectories that follow these policies
However, performance is poor for large policy updates

- Trust Region methods
TRPO proved that a surrogate function can be used to update a policy with guaranteed performance improvement (https://github.com/long8v/PTIR/issues/154), and this creates a constraint on when the policy is updated, resulting in the following form of multiplying the importance weight and advantage of the new and old policy network
<img width="367" alt="image" src="https://github.com/user-attachments/assets/e1489535-f648-4625-aef6-f77c6c7a0b9d">

Adds a penalty term, not actually a constraint, where $beta$ is a hyperparameter.
<img width="460" alt="image" src="https://github.com/user-attachments/assets/610aa2b5-8f85-4906-a5a7-26f12bc02638">

The problem with TRPO in this paper is that $\beta$ can't be picked.

### Clipped Surrogate Objective
<img width="367" alt="image" src="https://github.com/user-attachments/assets/a7a3deb0-4cdc-4eb7-ba81-feb095a2dc3e">

<img width="415" alt="image" src="https://github.com/user-attachments/assets/f04bf66e-ec62-45b1-92dd-503eae6cf1b6">

In conclusion, we can say that we clipped $r_t(\theta) = \frac{\pi_\theta(a_t | s_t)}{\pi_{\theta_{old}}(a_t | s_t)}$ so that it is not too large or too small

<img width="703" alt="image" src="https://github.com/user-attachments/assets/f6307ca3-f047-4b01-befe-d245209c85d8">


This resulted in less fluctuation in the policy network.

<img width="724" alt="image" src="https://github.com/user-attachments/assets/c6337d1e-19bf-4381-9d65-d04f6c6c2eee">

#### Adaptive KL Penalty Coefficient

<img width="635" alt="image" src="https://github.com/user-attachments/assets/6b51ff1b-6408-4d9e-ab0a-1a298efa1919">

Wow, this is so intuitive and simple.

#### Algorithm
Above, we've decided how we want to update the gradient for the policy, and everything else is fine.
Reducing the variance of reward by introducing V(s), i.e. adding a policy surrogate and a value function error term. Adding an entropy bonus to incentivize more exploration.
<img width="699" alt="image" src="https://github.com/user-attachments/assets/f4cbd1e4-cfdb-4f1d-82c7-ffd458abde0a">

advantage is the sum of the current discounted Reward minus the current V and the discounted future V.
<img width="445" alt="image" src="https://github.com/user-attachments/assets/5911be64-718a-4253-a56b-d6e00104e3e7">

I don't remember, but I used a technique to optimize bias // vairance at a fixed time step to get something like this
<img width="372" alt="image" src="https://github.com/user-attachments/assets/b88e172e-c25e-489b-8fea-41d28be3d6d3">


### Experiments
- loss term
<img width="723" alt="image" src="https://github.com/user-attachments/assets/07cbe885-9056-4e59-ab1e-d74f0318112b">

-  other RL algorithms
I don't even know what to say
<img width="716" alt="image" src="https://github.com/user-attachments/assets/3cb58942-489f-4be1-97f6-e00cfecb2fd3">

