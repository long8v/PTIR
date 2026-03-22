---
title: "[207] MM-EUREKA: Exploring Visual Aha Moment with Rule-based Large-scale Reinforcement Learning"
date: 2025-03-12
tags: ['RL', 'MLLM', '2025Q1']
paper: "https://github.com/ModalMinds/MM-EUREKA/blob/main/MM_Eureka_paper.pdf"
issue: 228
issueUrl: "https://github.com/long8v/PTIR/issues/228"
---
<img width="859" alt="Image" src="https://github.com/user-attachments/assets/1a63b029-aa01-40b5-aeaf-7d5a44af2419" />

[paper](https://github.com/ModalMinds/MM-EUREKA/blob/main/MM_Eureka_paper.pdf), [code](https://github.com/ModalMinds/MM-EUREKA), [dataset](https://huggingface.co/datasets/FanqingM/MM-Eureka-Dataset/tree/main)

## TL;DR
- **I read this because.. :** vision rl 
- **task :** MLLM R1 replicate
- **problem :** MLLM R1 하자 
- **idea :** 열심히 GRPO 데이터 모아서 하자
- **input/output :** {image, Q} -> reasoning, A
- **architecture :** InternVL2.5-7B-Instruct(r1 style), InternVL2.5-Pretrained-38B (r1-zero style)
- **objective :** RLOO loss 
- **baseline :** SFT, CoT SFT(MAmmoTH-VL-8B), MPO(MMPR dataset)
- **data :** GeoQA-Plus, K12, CLEVR, Geometry3K, MATH, IconQA, M3CoT, DVQA, ScienceQA, ChartQA, AI2D, UniGeo, InfoVQA, GeoS, MapQA 
- **evaluation :** MathVista, MathVerse, MathVision, Olympiad 
- **result :** 평균적으로 개선된 수학 성능. data scale이 가장 적게 들음. 
- **contribution :** 빨리 열심히 했다 
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
advantage 계산은 RLOO

![Image](https://github.com/user-attachments/assets/45be0c5d-1af8-4e81-99fa-8f3ccd7eb360)

loss는 PPO-clip loss

![Image](https://github.com/user-attachments/assets/c2ddd8db-1a45-4448-96c7-37aa0f5ed115)

loss에 KL divergence term 추가 ablation

![Image](https://github.com/user-attachments/assets/1be0f7fa-a902-46aa-a6c6-4215164d8658)

- extra hparams
  - rollout bs 128 / training bs 64 (8 rollout per sample)
  - temperature 1 
  - loss term에 kl divergence 제외
  - format reward coefficient는 instruction 에서 시작한 경우 잘 따르기 때문에 0.5 / pretrained weight에서 시작한 경우엔 1.0
  - ![Image](https://github.com/user-attachments/assets/04de2ece-1ecb-4ed8-b81d-001d720eb756)


### key findings 
- data filtering is crucial 
InternVL2.5-8B-Instruct로 8번 생성하게 한 뒤 {0, 1} 제거 
![Image](https://github.com/user-attachments/assets/7c692945-23dd-4b05-a7b6-f51797010194)

하고 안하고는 차이가 컸다.

- KL divergence
![Image](https://github.com/user-attachments/assets/18e1ab37-9e77-4895-a27f-2ead3ebdb769)

KL divergence가 있을 때 length decrease 경향이 있었고, 정확도도 KL divergence 끄고 키고 차이가 있어서 끄게 되었다

- Visual Aha Moment 
![Image](https://github.com/user-attachments/assets/ff129daa-c065-4f70-a07d-8c68e3e2de8a)

### evaluation
- K12
  - 중학교~고등학교 수준의 500개의 fill-in-the-blank math question
  - greedy decoding with a temperature 0 

## Result 
- 학습 과정 
<img width="726" alt="Image" src="https://github.com/user-attachments/assets/1a2d51ed-0dde-4ef2-ae46-66fd710e8385" />


<img width="692" alt="Image" src="https://github.com/user-attachments/assets/0e80336a-f6aa-439e-bc9f-23f2567acf93" />

- 일단 MAmmoTH-VL-8B(https://mammoth-vl.github.io/) 를 제외하고 SFT나 MPO보다 성능이 좋음.
- training data scale로 비교해보았을 때 SFT와는 확실히 좋고 (SFT는 다 하락함) 데이터를 조금 더 쓴 MPO 보다 math average 개선. 대부분의 개선은 mathverse와 K12. olympiad는 높지않음.

<img width="693" alt="Image" src="https://github.com/user-attachments/assets/393660e0-9397-4a7f-ba38-9d0e1ee8b939" />

- 일단 각 벤치에 대해 평가해보았을 때 small model과 large model이 성능이 차이가 많이 나는 것은 Olympiad가 드라마틱하다
- Mathvista는 큰 scale이나 small scale 둘다 mm-eureka에서 좋지 않음. 왜인진 모르겠다. 

### discussion
시도했으나 효과가 없었던 것 
- curriculum learning 
  - K12 데이터에서 difficulty를 매긴 뒤 difficulty 순으로 data sort를 했다.
  - <img width="701" alt="Image" src="https://github.com/user-attachments/assets/9643001b-d9fb-432b-a913-5011df726100" />
  - curriculum learning을 하니 오히려 stable learning이 안되는 경향성이 보였다.
  - early~middle stage에서 어려운 문제에 대한 exploration을 못하고 고착화되는것 아닌가? 싶었다
- online data filtering
  - <img width="696" alt="Image" src="https://github.com/user-attachments/assets/fef37a2f-535c-41ab-acf2-ae89351c8c47" />
  - difficulty {0,1}을 제외하는 방식을 offline data filtering이라고 하고 PRIME과 비슷하게 하는 방식을 online data filtering이라고 할 때 성능 개선
  - online data filtering은 dynamically 모델이 개선됨에 따라 다른 데이터를 볼 수 있다고 기대할 수 있다
  - <img width="700" alt="Image" src="https://github.com/user-attachments/assets/afdae35c-32a5-44bb-a751-4bff51053719" />
  - 그러나 online이 성능 개선이 미비했는데 각 training round에서 batch size가 달라지면서 gradient instability가 생겨서?라고 생각했다
- model size
  - R1-zero 시나리오를 small model에서 성공했다는 사례들이 있지만 mm 상황에서는 stability가 높지 않았다
  - <img width="709" alt="Image" src="https://github.com/user-attachments/assets/ba3b7728-acc9-4886-acd7-3cb054cb42c1" />

 
