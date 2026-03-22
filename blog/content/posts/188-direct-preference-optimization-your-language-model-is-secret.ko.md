---
title: "[169] Direct Preference Optimization: Your Language Model is Secretly a Reward Model"
date: 2024-08-26
tags: ['2023Q2', 'RL']
paper: "https://arxiv.org/abs/2305.18290"
issue: 188
issueUrl: "https://github.com/long8v/PTIR/issues/188"
---

<img width="663" alt="image" src="https://github.com/user-attachments/assets/7c20da97-960b-440f-a2fb-222c5b737151">

[paper](https://arxiv.org/abs/2305.18290)

## TL;DR
- **I read this because.. :** 배경지식 차
- **task :** RL
- **problem :** TRPO도 별도의 Reward model을 학습해야 하는데 모델이 커짐에 따라 너무 힘듦
- **idea :** reward model을 따로 없이 loss에 reward 에 대한 loss까지 direct하게 학습할 수 없을까?
- **input/output :** {state, reward} -> action
- **architecture :** GPT2-Large 
- **objective :** proposed. 
- **baseline :** zero-shot to GP-J, SFT, Preferre-ft, Unlikelihood, PPO, PPO-GT, Bes of N baseline(SFT reponse 중에 가장 reward가 높은 값 return)
- **data :** IMDb , Reddit TL;DR 
- **evaluation :** GPT-4 Evaluator 
- **result :** 베이스라인 대비 비슷하거나 나은 성능 
- **contribution :**
- **etc. :** 핀 교수님 여기서 뵙는군요 ..!

## Details
### Preliminaries 
- SFT 
소량의 양질의 데이터를 사용해서 $\pi^{SFT}$를 만듦


- Reward modeling (Bradley-Terry model)
<img width="372" alt="image" src="https://github.com/user-attachments/assets/d88ad225-4243-4068-8d26-fab50136755c">

이걸 binary 문제로 치환하면 
<img width="405" alt="image" src="https://github.com/user-attachments/assets/e4117f85-2224-43cd-93e6-12c53bce301d">

- RL finetuning phrase
<img width="307" alt="image" src="https://github.com/user-attachments/assets/8aaacc7c-92f3-4107-bd24-5b63995593c4">


### DPO
위의 함수를 다시 쓰면 
<img width="289" alt="image" src="https://github.com/user-attachments/assets/ad6ba144-f2f9-4293-a670-59b0a65ed5df">

<img width="615" alt="image" src="https://github.com/user-attachments/assets/96720180-dada-43a7-9566-f7d04ba02e70">

partition function은 확률분포로 만들어주는 역할?

optimal policy에 대해 bradely-terry model은 아래와 같은 preferenc가 성립 

<img width="400" alt="image" src="https://github.com/user-attachments/assets/917fbd79-edc4-4816-b9b4-56eab9295668">

policy의 관점에서 human preference data를 가지고 있으니 이를 mle objective로 표현하면
<img width="534" alt="image" src="https://github.com/user-attachments/assets/6ade48b4-065e-4366-b5c1-7fde9a702fa6">

### what does the DPO updates?
<img width="604" alt="image" src="https://github.com/user-attachments/assets/15c6c893-17d1-447d-ba4c-d3291de19e5d">
