---
title: "[142] Trust Region Policy Optimization"
date: 2023-12-17
tags: ['2015', 'RL']
paper: "https://arxiv.org/pdf/1502.05477.pdf"
issue: 154
issueUrl: "https://github.com/long8v/PTIR/issues/154"
---
<img width="884" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2b21adb8-8f9b-4769-ad3a-13bb14c61d38">

[paper](https://arxiv.org/pdf/1502.05477.pdf)

## TL;DR
- **I read this because.. :** CS285 기말과제 
- **task :** reinforcement learning 
- **problem :** 이론적으로 무조건 성능이 개선되는 policy update 방식이 있을까
- **idea :** conservative policy iteration에서 증명한 lower bound를 일반적인 policy network에 대해 구하고 이 lower bound를 surrogate function으로 해서 maximization하자 
- **input/output :** {s, a, r, ... } -> policy 
- **architecture :** conv+ linear
- **baseline :** deep Q-learning
- **result :** 나쁘지 않은 성능. Deep Q-learning보다 별로 좋진 않음 
- **contribution :** PPO의 전신 
- **etc. :**

## Details
# [TRPO.pptx](https://github.com/long8v/PTIR/files/13765816/TRPO.pptx)

- objective 
<img width="574" alt="스크린샷 2023-12-25 오후 8 53 45" src="https://github.com/long8v/PTIR/assets/46675408/378c099e-7bd7-4434-8e6f-05fe250dedd4">

