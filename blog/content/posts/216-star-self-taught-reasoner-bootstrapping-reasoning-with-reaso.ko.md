---
title: "[195] STaR: Self-Taught Reasoner Bootstrapping Reasoning With Reasoning"
date: 2025-01-09
tags: ['2022Q1', 'google', '25min', 'reasoning']
paper: "https://arxiv.org/abs/2203.14465"
issue: 216
issueUrl: "https://github.com/long8v/PTIR/issues/216"
---

<img width="1196" alt="image" src="https://github.com/user-attachments/assets/fd8c2a2e-a15e-4ea7-b8df-c5080cb54d01" />

[paper](https://arxiv.org/abs/2203.14465)

## TL;DR
- **I read this because.. :** q*의 star가 이거다 등등 많이 언급되어
- **task :** problem solving
- **problem :** rationale을 학습하면 모델 성능이 더 좋지 않을까?
- **idea :** 휴리스틱으로는 한계가 있으니 모델에게 rationale을 생성하게 하자. 못 생성하면 정답을 hint로 주자. 
- **input/output :** Q -> rationale - A
- **architecture :** GPT-J
- **objective :** CE loss 
- **baseline :** direct answer tuned GPT-J, Few-shot GPT-J, Few-shot LaMDA 137B
- **data :** (source) GSM, CommonsenceQA, arithmetic problem 
- **evaluation :** accuracy
- **result :** 더 빠르게 정확도가 올라감. 못 풀던 문제도 품(최종 정확도가 올라감). 
- **contribution :** self-improvement? self-evolvement? rationale 강조?
- **etc. :**

## Details
### STaR
 
<img width="1134" alt="image" src="https://github.com/user-attachments/assets/5d900a1a-dcf2-4b61-b854-80bda068e446" />

<img width="1076" alt="image" src="https://github.com/user-attachments/assets/68e0c73d-cc27-4218-bb86-82cc6fb1cbcd" />

디테일은 1) 정답을 맞추지 않은 문제에 대해서만 hint를 줌 2) model finetune을 할 때 iterative하게 하는게 아니라 base model에서 했다고 함. 음 이렇게 하면서 점점 rationale이 좋아지는건가? 이건 다른 모델들이랑 방식이 좀 다른듯..

정답이 틀린 rationale에 대해서 filtering하는 프로세스가 RL objectvie랑 비슷하다고 주장 

<img width="1034" alt="image" src="https://github.com/user-attachments/assets/df3346be-7712-4521-9dd7-1b47c2f9b733" />


### Result
<img width="1121" alt="image" src="https://github.com/user-attachments/assets/bf6fd52e-560d-4671-8d63-e578fb219f32" />

color는 몇자리 digit problem인지

<img width="524" alt="image" src="https://github.com/user-attachments/assets/d852e10f-295c-4be2-a74e-ddf387a21a23" />

못본 digit에 대해도 풀수 있는 능력이 발현

<img width="1066" alt="image" src="https://github.com/user-attachments/assets/4658b20a-b089-4c0e-bbdd-113455bf9319" />

<img width="1123" alt="image" src="https://github.com/user-attachments/assets/4d3e2a38-a8b5-4e0d-bf93-a9357816d831" />


