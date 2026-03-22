---
title: "[176] Smaug: Fixing Failure Modes of Preference Optimisation with DPO-Positive"
date: 2024-09-05
tags: ['LLM', 'RL', '2024Q1']
paper: "https://arxiv.org/pdf/2402.13228"
issue: 195
issueUrl: "https://github.com/long8v/PTIR/issues/195"
---
<img width="663" alt="image" src="https://github.com/user-attachments/assets/ada18676-8bca-4f04-9698-13dbb6b3eb89">

[paper](https://arxiv.org/pdf/2402.13228), [code](https://github.com/abacusai/smaug)

## TL;DR
- **I read this because.. :** dense RLHF 관련인가 싶어서 
- **task :** RLHF
- **problem :** DPO는 상대적인 log prob에 대한 loss를 부가하기 때문에 edit distance가 적은 pair의 경우 틀리지 않은 부분에 대해서도 log prob이 낮아지는 것 관찰 
- **idea :** preferred answer에 대한 log prob이 너무 낮아지지 않도록 penalty 부가 
- **input/output :** query -> answer
- **architecture :** Llama-2-7B-Chat, Bagel-34B-v0.2, MoMo-72b-lora-1.8.7-DPO
- **objective :** proposed DPOP loss(DPO loss + $\max\left(0, \log \frac{\pi_{\text{ref}}(y_w|x)}{\pi_{\theta}(y_w|x)}\right)$ )
- **baseline :** DPO, IPO, SLiC
- **data :** GSM8K, MetaMath, ARC, Hellaswag를 일부러 틀린 pair를 만드는 식으로 해서 다시 만듦.
- **evaluation :** GSM8K / ARC / Hellaswag test split 
- **result :** edit distance가 낮은/높은 데이터셋 모두에서 베이스라인보다 높은 성능.
- **contribution :** 어떤 상황에서 문제가 생긴건지 직관적으로 이해하기 쉽고 해결 방법도 직관적임
- **etc. :** dense RLHF랑은 상관 없었지만 상관 있는걸로..?! ㅋㅋ

## Details
### motivation
<img width="511" alt="image" src="https://github.com/user-attachments/assets/e5803e03-078c-4d3e-be9a-def613e58b2c">

DPO의 loss는 위와 같음
이때 저자들이 강조하는 문제는 loss가 상대적인 log prob에만 의존한다는 것임. (논문에서 $\pi_{ratio}$로 표현)
이 상대적인 비율이 preferred 가 disprefered보다 높기만 하면 되니까 $y_w$에서도 $\pi_{ratio}(y_w)$는 계속 낮아질 수 있음.
이것이 어느 상황에 대해서 문제가 되냐면 edit distance가 적은 pair에 대해서 DPO를 할 때임.

<img width="682" alt="image" src="https://github.com/user-attachments/assets/e51277fd-8a8f-411c-968c-8f57fbf77646">

DPO loss에 대해 Gradient를 구하면 아래와 같음
<img width="375" alt="image" src="https://github.com/user-attachments/assets/f05c59ed-5d9d-4927-87bb-59e14f9ccb11">

이 때 논의의 편의성을 위해 첫번째 토큰에서만 $y_w$, $y_l$이 다르다고 하자. 그러면 그 이후 토큰 $k$에 대한 gradient는 아래와 같다.
<img width="379" alt="image" src="https://github.com/user-attachments/assets/59dede43-4750-4685-b86f-fc57768fb730">

- $s_j^{x}$ 는 x가 주어졌을 때 j 번째 토큰을 예측하는 확률

우리는 보통 DPO를 SFT가 완료된 weight에서 시작하기 때문에 틀린 토큰 이후에 나오는 토큰에 대해서는 log prob이 낮을 수 밖에 없음.
그러면 뒤의 토큰들은 사실상 맞는 토큰임에도 불구하고 둘의 log prob의 차이가 생기기 때문에 Loss가 부가됨. 
즉 틀린 토큰에 대한 확률 분포는 맞게 수정되지만 그 이후의 맞는 토큰에 대해서는 불필요하게 log prob이 낮아지게 되는 것이 문제

### Propose DPOP

<img width="633" alt="image" src="https://github.com/user-attachments/assets/ed9f19e5-7d0d-4fb2-b8d1-b586b97c7d1a">

penalty term 추가. prefered answer에 대해 $\pi_{ref}$보다 낮아지지 않도록. 

### Result

<img width="681" alt="image" src="https://github.com/user-attachments/assets/305a4736-bd61-4803-952d-11f91222a023">

<img width="680" alt="image" src="https://github.com/user-attachments/assets/afcd6923-1c97-4327-b6c0-bafe17948333">
