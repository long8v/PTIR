---
title: "Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations"
date: 2025-01-17
tags: ['ACL', 'RL', '2023Q4', 'reasoning']
paper: "https://arxiv.org/abs/2312.08935"
issue: 217
issueUrl: "https://github.com/long8v/PTIR/issues/217"
summary: "It's been mentioned a lot, too. It seems to be one of the main ways to learn PRM. - Twitter says it's the first PRM paper after OAI? -> OmeagPRM is the one that improved it afterwards?"
---
![Image](https://github.com/user-attachments/assets/cba61361-cdd2-4834-b487-318c02a7bf75)

[paper](https://arxiv.org/abs/2312.08935), [dataset](https://huggingface.co/datasets/peiyi9979/Math-Shepherd)

## TL;DR
- **I read this because.. :** It's also mentioned a lot. as if it's one of the main ways to learn PRM.
- **task :** math solving
- **problem :** I want to learn Process Reward Model, but Human annotated is too expensive
- **idea:** Use MCTS to get the value of a specific step and use that as the label for PRM -- learn step-level PPOs
- **architecture :** LLaMA2-7B/13B/70B, LLemma-7B/34B, Mistral-7B, Deepseek-67B 
- **objective :** (PRM) bce loss (RL) PPO loss 
- **baseline :** (train/infer) ORM, Self-consistency, Self-consistency + ORM (data) rule-based, BART NLI 
- **data :** 170K solution for GSM8K / 270K for MATH
- **evaluation :** GSM8K, MATH accuracy
- **result :** Good performance
- **contribution :** Twitter says it's the first PRM paper after OAI? 

## Details
- thumbnail

![Image](https://github.com/user-attachments/assets/c68bb960-c48e-4e54-81c9-b422e7ea91e6)

- PRM loss 

![Image](https://github.com/user-attachments/assets/9ef17ded-83c4-42a6-b265-ba4caf9788b8)


- automatic process annotation

![Image](https://github.com/user-attachments/assets/815611c6-8fb8-4521-b7a0-707b29df8dc7)

Think of that value estimation as being done with MCTS!
If you think about rolling out each step, the number of cases will be too large, so we optimized it with MCTS (https://gusals1620.tistory.com/3).

![Image](https://github.com/user-attachments/assets/c3f92543-1fbe-4e10-b01a-2f091373a6fe)

In conclusion, I used HARD because I don't need to find HPARAMs by model? (I guess I could do it with MSE, huh?)

- parameter setting 
- generator and completer learned about metamath for 3 epochs each
- Learn GSM8K and MATH training data to generate ORM / PRM training data -> generate 15 solutions per problem afterwards
- completer is generated with decoded number N=8 using Llemma-7B (how is a completer different from a generator... is a generator the entity that creates the solution and a completer the entity that does the rollout? Can these two models be different?)
- Use LLaMA-2 70B and Llemma-34B for verification
- The policy model for PPO learning is based on Llama2-7B and Mistral-7B
- I'm not sure why the models are so different.

- result 

![Image](https://github.com/user-attachments/assets/3d8be9c4-2856-4394-bb4e-35a929a6da7f)

Best verification methodology out of 256 samples.

![Image](https://github.com/user-attachments/assets/e8a8caf0-e274-41d1-8618-e109af1c05ee)

Good performance compared to other learning methodologies (ORM + PPO / RFT)

![Image](https://github.com/user-attachments/assets/535fe196-de24-44d0-952c-4ba2d49dcfc8)

![Image](https://github.com/user-attachments/assets/2827494d-de0f-4e57-aa3e-d947d2205b97)

![Image](https://github.com/user-attachments/assets/15367b02-ea50-4d08-9da8-5a2ac0455385)

![Image](https://github.com/user-attachments/assets/fdf67c4c-6e02-4045-8970-138ac9928cee)

- There was an attempt to label the process as a BART NLI, and there is an ablation for this (https://arxiv.org/abs/2206.02336)

![Image](https://github.com/user-attachments/assets/126330e2-64ca-43cb-a171-5577ec9c03e0)

- Looking at (a)(b), math-shepherd performs better than verifier / ORM, performance also improves as model gets larger for both
- (c) Compared to self-consistency, if the reward model is too smaller than the generator model, the performance gets worse as the solution per problem gets larger -- the reward model should be as good as the generator
- (d) Much better performance than (a) when the verifier is larger. Difference with SC becomes much larger