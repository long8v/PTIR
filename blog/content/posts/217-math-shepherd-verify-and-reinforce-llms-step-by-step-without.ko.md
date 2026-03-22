---
title: "[196] Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations"
date: 2025-01-17
tags: ['ACL', 'RL', '2023Q4', 'reasoning']
paper: "https://arxiv.org/abs/2312.08935"
issue: 217
issueUrl: "https://github.com/long8v/PTIR/issues/217"
---
![Image](https://github.com/user-attachments/assets/cba61361-cdd2-4834-b487-318c02a7bf75)

[paper](https://arxiv.org/abs/2312.08935), [dataset](https://huggingface.co/datasets/peiyi9979/Math-Shepherd)

## TL;DR
- **I read this because.. :** 역시 많이 언급되어. PRM을 학습하기 위한 대표적인 방법 중 하나인듯.
- **task :** math solving
- **problem :** Process Reward Model 학습하고 싶은데 Human annotated 너무 비싸다
- **idea :** MCTS를 사용하여 특정 step의 value를 구하고 그걸 PRM의 label로 사용하여 학습 -- step-level PPO를 학습하자 
- **architecture :** LLaMA2-7B/13B/70B, LLemma-7B/34B, Mistral-7B, Deepseek-67B 
- **objective :** (PRM) bce loss (RL) PPO loss 
- **baseline :** (train/infer) ORM, Self-consistency, Self-consistency + ORM (data) rule-based, BART NLI 
- **data :** 170K solution for GSM8K / 270K for MATH
- **evaluation :** GSM8K, MATH accuracy
- **result :** 좋은 성능 
- **contribution :** 트위터를 보면 OAI 이후 첫 PRM paper라는듯? -> 이후 이걸 개선한게 OmeagPRM인듯?

## Details
- thumbnail

![Image](https://github.com/user-attachments/assets/c68bb960-c48e-4e54-81c9-b422e7ea91e6)

- PRM loss 

![Image](https://github.com/user-attachments/assets/9ef17ded-83c4-42a6-b265-ba4caf9788b8)


- automatic process annotation

![Image](https://github.com/user-attachments/assets/815611c6-8fb8-4521-b7a0-707b29df8dc7)

저 value estimation을 MCTS로 했다고 생각하면 됨! 
각 step별로 다 rollout한다고 생각하면 경우의 수가 너무 많아지니 이를 최적화한게 MCTS (https://gusals1620.tistory.com/3)

![Image](https://github.com/user-attachments/assets/c3f92543-1fbe-4e10-b01a-2f091373a6fe)

결론적으론 hard를 썼는데 hparam을 모델 별로 찾지 않아도 된다서라고? (mse로 해도 되는거 아닌감 ㅎ)

- parameter setting 
  - generator 와 completer는 metamath에 대해 3 epoch씩 학습 한 것 
  - ORM / PRM 학습데이터를 생성하기 위해서 GSM8K와 MATH training data를 학습 -> 이후 문제당 15개의 solution을 생성 
  -  completer는 Llemma-7B를 사용하여 decoded number N=8로 생성 (completer와 generator는 어떻게 다른가.. generator는 solution을 만드는거고 completer는 rollout을 하는 주체인건가? 이 두 모델이 다를수가 있나?)
  - verification을 위해서는 LLaMA-2 70B와 Llemma-34B 사용 
  - PPO학습의 policy 모델은 Llama2-7B와 Mistral-7B
  - 모델을 왜 이렇게 다양하게 쓴건지 잘 모르겠음

- result 

![Image](https://github.com/user-attachments/assets/3d8be9c4-2856-4394-bb4e-35a929a6da7f)

256개 sample 중 verification 방법론 중 가장 좋음. 

![Image](https://github.com/user-attachments/assets/e8a8caf0-e274-41d1-8618-e109af1c05ee)

다른 학습 방법론(ORM + PPO / RFT)와 비교했을 때 성능이 좋음

![Image](https://github.com/user-attachments/assets/535fe196-de24-44d0-952c-4ba2d49dcfc8)

![Image](https://github.com/user-attachments/assets/2827494d-de0f-4e57-aa3e-d947d2205b97)

![Image](https://github.com/user-attachments/assets/15367b02-ea50-4d08-9da8-5a2ac0455385)

![Image](https://github.com/user-attachments/assets/fdf67c4c-6e02-4045-8970-138ac9928cee)

- process의 label을 BART NLI로 하고자 하는 시도가 있었는데 이거에 대한 ablation (https://arxiv.org/abs/2206.02336) 

![Image](https://github.com/user-attachments/assets/126330e2-64ca-43cb-a171-5577ec9c03e0)

- (a)(b)를 보면 math-shepherd가 verifier / ORM보다 더 좋은 성능, model 둘다 커지면 성능도 좋아짐 
- (c) self-consistency와 비교했을 때, reward model이 generator 모델보다 너무 작으면 solution per problem이 커질수록 성능이 안좋아짐 -- reward model도 generator만큼 좋은걸 써야 함 
- (d) verifier가 더 클 때 (a) 보다 훨씬 좋은 성능. SC와의 차이가 많이 커짐 