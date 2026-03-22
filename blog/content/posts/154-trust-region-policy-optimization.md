---
title: "[142] Trust Region Policy Optimization"
date: 2023-12-17
tags: ['2015', 'RL']
paper: "https://arxiv.org/pdf/1502.05477.pdf"
issue: 154
issueUrl: "https://github.com/long8v/PTIR/issues/154"
summary: "CS285 Final Project - Predecessor to PPOs"
---
<img width="884" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2b21adb8-8f9b-4769-ad3a-13bb14c61d38">

[paper](https://arxiv.org/pdf/1502.05477.pdf)

## TL;DR
- **I read this because.. :** CS285 Final Assignment
- **task :** reinforcement learning 
- **problem :** Is there a policy update method that theoretically improves performance unconditionally?
- **idea :** Find the lower bound proved by the conservative policy iteration for the general policy network and maximize this lower bound as a surrogate function.
- **input/output :** {s, a, r, ... } -> policy 
- **architecture :** conv+ linear
- **baseline :** deep Q-learning
- **result :** Not bad performance. Not much better than Deep Q-learning
- contribution :** Predecessor of PPO
- **etc. :**

## Details
# [TRPO.pptx](https://github.com/long8v/PTIR/files/13765816/TRPO.pptx)

- objective 
<img width="574" alt="스크린샷 2023-12-25 오후 8 53 45" src="https://github.com/long8v/PTIR/assets/46675408/378c099e-7bd7-4434-8e6f-05fe250dedd4">

