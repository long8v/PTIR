---
title: "[175] Dense Reward for Free in Reinforcement Learning from Human Feedback"
date: 2024-09-04
tags: ['ICML', 'LLM', 'RL', '2024Q3']
paper: "https://arxiv.org/abs/2402.00782"
issue: 194
issueUrl: "https://github.com/long8v/PTIR/issues/194"
---

<img width="716" alt="image" src="https://github.com/user-attachments/assets/2164412e-b719-4134-929d-239e8d5b8ff7">

[paper](https://arxiv.org/abs/2402.00782), [code](https://github.com/XanderJC/attention-based-credit)

## TL;DR
- **I read this because.. :** dense RLHF에 관심 있어서 
- **task :** RLHF
- **problem :** RL에서 sparse reward가 문제다 
- **idea :** reward를 마지막에서만이 아니라 reward model의 attention map으로 나누어주자 
- **input/output :** Q -> A
- **architecture :** GPT-2 , openLLaMA
- **objective :** PPO objective // reward 산출식이 변경 
- **baseline :** RLHF(PPO인듯), 토큰 길이별로 균등하게 나눠주는 것, ABC-D(reward model이 아니라 actor model의 attention map 활용) 
- **data :** IMDb(GPT-2), RedPajama / Antrophic helpful + harmless preference data
- **evaluation :** time step 대비 action model이 도달한 reward의 평균 -> MMLU 이런건 평가 안했넹
- **result :** 이론적으로 RLHF와 같은 해를 가짐. 더 빠르게 수렴하며 better local optima에 도달하는듯 
- **contribution :** RLHF의 dense reward를 싸게! instability 개선! 
- **etc. :** reward의 평균으로만 평가해도 되나?! 

## Details
### motivation
<img width="341" alt="image" src="https://github.com/user-attachments/assets/b3444ec2-19d1-492a-9948-0fa35c650b56">

LLM의 sparse reward가 문제다 
<img width="865" alt="image" src="https://github.com/user-attachments/assets/9f657c7c-39bd-4c4c-ae6b-b184d70e91c6">

특히 sequence 길이가 길어질 때 더더욱 stability가 떨어진다. 

### preliminary
<img width="421" alt="image" src="https://github.com/user-attachments/assets/7f7656dd-19c4-46c1-9b2b-e2ef29139d14">

### proposed ABC
LLM 문제를 일종의 sequential한 decision making이라고 볼 수 있고 
finite-state(문장은 언제나 끝나니까..) MDP 문제로 표현할 수 있다.

우리의 목표는 아래의 discounted reward를 최대화하는 action을 찾는 것이라고 볼 수 있다.
<img width="258" alt="image" src="https://github.com/user-attachments/assets/e73e2545-677e-4042-9e0b-c5fc8137c04d">

우리가 하는 것은 마지막 토큰 선택에 대한 reward를 아는 것이다. 
<img width="167" alt="image" src="https://github.com/user-attachments/assets/cd7d278a-fddf-44ef-82d4-15ab6fa8b8c3">

여기서 $\alpha_i$는 reward model이 마지막 토큰에서 reward를 예측할 때의 마지막 레이어의 attention map의 head 평균이다. (마지막 token row를 인덱싱해서 벡터) 
<img width="171" alt="image" src="https://github.com/user-attachments/assets/acb63b5b-56ab-47ec-bc46-867d8bdc3128">

time step t의 reward에 대해서 attention map으로 나누어져서 벡터로 만들면 이게 ABC
<img width="317" alt="image" src="https://github.com/user-attachments/assets/c1ff0629-e6b5-48a0-b58b-5d936eed83a5">

- $R_\phi$ : reward model 이라고 하는뎅.. 마지막 step에 predicted reward가 있는 sparse reward가 아닐까 싶음?!
- $r_C$ : 마지막 토큰의 predicted reward 


<img width="409" alt="image" src="https://github.com/user-attachments/assets/c2ccde1a-f374-4e53-8ad0-decc14d05c62">

- 실제로는 $R_\phi$와 $\alpha \times r_C$ 의 $\beta$, 1 - $\beta$ 보간한 것을 사용
- $\beta$가 커질수록 성능도 좋아진다고 관찰함.

### result
<img width="427" alt="image" src="https://github.com/user-attachments/assets/e984a4f1-ce1c-40a1-8d94-e3d8acd2dba1">

- ABC-D : attention map을 policy network로 쓰는걸 



### Limitation
- tokenize 문제
reward model tokenizer == action model tokenize 여야지 현재가능 
- over optimized RM 
ABC 방법이 RM에 더 오버피팅된 것일 수도 있는데 fully 탐색하지 않았다. 
- only positive
모든 reward가 positive다. DeepLIFT 같은걸로 Negative도 해보자 
