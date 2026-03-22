---
title: "[175] Dense Reward for Free in Reinforcement Learning from Human Feedback"
date: 2024-09-04
tags: ['ICML', 'LLM', 'RL', '2024Q3']
paper: "https://arxiv.org/abs/2402.00782"
issue: 194
issueUrl: "https://github.com/long8v/PTIR/issues/194"
summary: "I'm interested in dense RLHF - dense RLHF rewards cheaply! Improved stability!"
---

<img width="716" alt="image" src="https://github.com/user-attachments/assets/2164412e-b719-4134-929d-239e8d5b8ff7">

[paper](https://arxiv.org/abs/2402.00782), [code](https://github.com/XanderJC/attention-based-credit)

## TL;DR
- **I read this because.. :** I'm interested in dense RLHF.
- **task :** RLHF
- **problem :** sparse reward in RL is a problem
- **idea :** split reward into the attention map of the reward model, not just at the end
- **input/output :** Q -> A
- **architecture :** GPT-2 , openLLaMA
- **objective :** PPO objective // reward formula changes
- **baseline :** RLHF (as if it were PPO), evenly distributed by token length, ABC-D (utilizing attention map from actor model, not reward model)
- **data :** IMDb(GPT-2), RedPajama / Antrophic helpful + harmless preference data
- **evaluation :** average of reward reached by action model over time step -> MMLU I don't evaluate this stuff.
- **result :** Theoretically has the same solution as RLHF. Converges faster and seems to reach a better local optima.
- **contribution :** RLHF's dense rewards cheaply! Improved instability!
- **etc. :** Can I just evaluate the average of the rewards?!

## Details
### motivation
<img width="341" alt="image" src="https://github.com/user-attachments/assets/b3444ec2-19d1-492a-9948-0fa35c650b56">

LLM's sparse rewards are a problem
<img width="865" alt="image" src="https://github.com/user-attachments/assets/9f657c7c-39bd-4c4c-ae6b-b184d70e91c6">

This is especially unreliable for longer sequences.

### preliminary
<img width="421" alt="image" src="https://github.com/user-attachments/assets/7f7656dd-19c4-46c1-9b2b-e2ef29139d14">

### proposed ABC
LLM problems can be viewed as a kind of sequential decision making.
It can be expressed as a finite-state (because sentences always end...) MDP problem.

We can see that our goal is to find an action that maximizes the discounted reward below.
<img width="258" alt="image" src="https://github.com/user-attachments/assets/e73e2545-677e-4042-9e0b-c5fc8137c04d">

What we want to do is know the reward for the last token selection.
<img width="167" alt="image" src="https://github.com/user-attachments/assets/cd7d278a-fddf-44ef-82d4-15ab6fa8b8c3">

where $\alpha_i$ is the head average of the attention map of the last layer when the reward model predicts the reward at the last token. (vector indexed by the last token row)
<img width="171" alt="image" src="https://github.com/user-attachments/assets/acb63b5b-56ab-47ec-bc46-867d8bdc3128">

If the reward at time step t is divided into an attention map and made into a vector, this is the ABC
<img width="317" alt="image" src="https://github.com/user-attachments/assets/c1ff0629-e6b5-48a0-b58b-5d936eed83a5">

- $R_\phi$ : reward model 이라고 하는뎅.... Maybe it's a sparse reward with predicted reward in the last step?!
- $r_C$ : predicted reward of the last token


<img width="409" alt="image" src="https://github.com/user-attachments/assets/c2ccde1a-f374-4e53-8ad0-decc14d05c62">

- In practice, we use $\beta$, 1 - $\beta$ interpolation of $R_\phi$ and $\alpha \times r_C$.
- Observed that as $\beta$ gets larger, performance gets better.

### result
<img width="427" alt="image" src="https://github.com/user-attachments/assets/e984a4f1-ce1c-40a1-8d94-e3d8acd2dba1">

- ABC-D: write attention map as policy network



### Limitation
- tokenize issues
reward model tokenizer == action model tokenize, not currently possible
- over optimized RM 
It is also possible that the ABC method is more overfitting for RM, which I haven't fully explored.
- only positive
All rewards are positive. Let's do negatives with something like DeepLIFT
