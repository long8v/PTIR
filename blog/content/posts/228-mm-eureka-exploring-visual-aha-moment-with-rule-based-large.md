---
title: "MM-EUREKA: Exploring Visual Aha Moment with Rule-based Large-scale Reinforcement Learning"
date: 2025-03-12
tags: ['RL', 'MLLM', '2025Q1']
paper: "https://github.com/ModalMinds/MM-EUREKA/blob/main/MM_Eureka_paper.pdf"
issue: 228
issueUrl: "https://github.com/long8v/PTIR/issues/228"
summary: "VISION RL - Quick and Hard"
---
<img width="859" alt="Image" src="https://github.com/user-attachments/assets/1a63b029-aa01-40b5-aeaf-7d5a44af2419" />

[paper](https://github.com/ModalMinds/MM-EUREKA/blob/main/MM_Eureka_paper.pdf), [code](https://github.com/ModalMinds/MM-EUREKA), [dataset](https://huggingface.co/datasets/FanqingM/MM-Eureka-Dataset/tree/main)

## TL;DR
- **I read this because.. :** vision rl 
- **task :** MLLM R1 replicate
- Problem :** MLLM R1 Letdown
- **idea :** Let's work hard to collect GRPO data
- **input/output :** {image, Q} -> reasoning, A
- **architecture :** InternVL2.5-7B-Instruct(r1 style), InternVL2.5-Pretrained-38B (r1-zero style)
- **objective :** RLOO loss 
- **baseline :** SFT, CoT SFT(MAmmoTH-VL-8B), MPO(MMPR dataset)
- **data :** GeoQA-Plus, K12, CLEVR, Geometry3K, MATH, IconQA, M3CoT, DVQA, ScienceQA, ChartQA, AI2D, UniGeo, InfoVQA, GeoS, MapQA 
- **evaluation :** MathVista, MathVerse, MathVision, Olympiad 
- **result :** Improved math performance on average. Least data scale.
- **contribution :** worked hard and fast
- **etc. :**

## Details

### Dataset 
![Image](https://github.com/user-attachments/assets/32f145ae-ef4d-4a59-8bdd-51181ad21134)

- chart comprehension: ChartQA, DVQA, ...
- General Scientific Reasoning: AI2D, ScienceQA, ...
- Mathematical Reasoning: K12(proposed), GeoQA

### training 
- reward
format + `<think>...</think><answer>...</answer>` parsing accuracy reward 

- loss
The advantage calculation is based on the RLOO

![Image](https://github.com/user-attachments/assets/45be0c5d-1af8-4e81-99fa-8f3ccd7eb360)

loss is the PPO-clip loss

![Image](https://github.com/user-attachments/assets/c2ddd8db-1a45-4448-96c7-37aa0f5ed115)

Add KL divergence term to loss ablation

![Image](https://github.com/user-attachments/assets/1be0f7fa-a902-46aa-a6c6-4215164d8658)

- extra hparams
  - rollout bs 128 / training bs 64 (8 rollout per sample)
  - temperature 1 
- Exclude KL divergence from loss term
- The format reward coefficient follows the instruction well, so if you start at 0.5 / pretrained weight, it will be 1.0
  - ![Image](https://github.com/user-attachments/assets/04de2ece-1ecb-4ed8-b81d-001d720eb756)


### key findings 
- data filtering is crucial 
Let InternVL2.5-8B-Instruct generate 8 times, then remove {0, 1} Remove
![Image](https://github.com/user-attachments/assets/7c692945-23dd-4b05-a7b6-f51797010194)

was a big difference.

- KL divergence
![Image](https://github.com/user-attachments/assets/18e1ab37-9e77-4895-a27f-2ead3ebdb769)

The length tended to decrease when there was KL divergence, and the accuracy was different with KL divergence off and on, so I turned it off.

- Visual Aha Moment 
![Image](https://github.com/user-attachments/assets/ff129daa-c065-4f70-a07d-8c68e3e2de8a)

### evaluation
- K12
- 500 fill-in-the-blank math questions at the middle to high school level
  - greedy decoding with a temperature 0 

## Result 
- The learning process
<img width="726" alt="Image" src="https://github.com/user-attachments/assets/1a2d51ed-0dde-4ef2-ae46-66fd710e8385" />


<img width="692" alt="Image" src="https://github.com/user-attachments/assets/0e80336a-f6aa-439e-bc9f-23f2567acf93" />

- First of all, it performs better than SFT or MPO, except for MAmmoTH-VL-8B (https://mammoth-vl.github.io/).
- Compared to SFT with training data scale, it is definitely better than SFT (SFT is all down) and math average is better than MPO with slightly more data. Most of the improvement is in mathverse and K12. olympiad is not high.

<img width="693" alt="Image" src="https://github.com/user-attachments/assets/393660e0-9397-4a7f-ba38-9d0e1ee8b939" />

- Once we evaluate each bench, the difference in performance between the small and large models is dramatic for the Olympiad
- Mathvista is not good with mm-eureka, neither large scale nor small scale. I don't know why.

### discussion
What you tried and it didn't work
- curriculum learning 
- We assigned difficulty to the K12 data and then sorted the data by difficulty.
  - <img width="701" alt="Image" src="https://github.com/user-attachments/assets/9643001b-d9fb-432b-a913-5011df726100" />
- Curriculum learning tends to make learning less stable.
- I wondered if we were getting stuck in the early to middle stages without exploring hard problems.
- online data filtering
  - <img width="696" alt="Image" src="https://github.com/user-attachments/assets/fef37a2f-535c-41ab-acf2-ae89351c8c47" />
- Improved performance when excluding difficulty {0,1} is called offline data filtering and PRIME-like is called online data filtering.
- Online data filtering dynamically allows you to expect to see different data as your model improves.
  - <img width="700" alt="Image" src="https://github.com/user-attachments/assets/afdae35c-32a5-44bb-a751-4bff51053719" />
- However, online didn't perform as well as it should have because of the gradient instability caused by varying batch size in each training round.
- model size
- There are examples of R1-zero scenarios being successful in small models, but not very stable in mm situations
  - <img width="709" alt="Image" src="https://github.com/user-attachments/assets/ba3b7728-acc9-4886-acd7-3cb054cb42c1" />

 
