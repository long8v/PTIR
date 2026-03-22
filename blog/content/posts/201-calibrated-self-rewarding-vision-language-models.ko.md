---
title: "[182] Calibrated Self-Rewarding Vision Language Models"
date: 2024-10-10
tags: ['NeurIPS', '25min', 'RL', 'MLLM', '2024Q2']
paper: "https://arxiv.org/abs/2405.14622"
issue: 201
issueUrl: "https://github.com/long8v/PTIR/issues/201"
---

<img width="724" alt="image" src="https://github.com/user-attachments/assets/f1a33bb5-929b-4012-8f80-c6de8997bc46">

[paper](https://arxiv.org/abs/2405.14622)

## TL;DR
- **I read this because.. :** VLM self-rewarding
- **task :** LVLM
- **problem :** LVLM이 object hallucination이 심한데 이는 text token에 너무 attention이 실려있기 때문
- **idea :** self rewarding + CLIPScore로 image relevance 두개 잘 합쳐서 이미지에 dependant 하도록 reward 주도록 하자 
- **architecture :** LLaVA 1.5 7B / 13B
- **objective :** DPO loss 
- **baseline :** LLaVA, RLHF-V, VLfeedback, ...
- **data :** iteration 돌면서 생성. seed는 llava-instruction 150K 데이터 중 랜덤으로 뽑은 subset 13K
- **evaluation :** VLM bench(MME, SEED, LLaVA_w, MMBench, ...), VQA(SQA, VisWiz, GQA), Hall-bench(POPE, CHAIR)
- **result :** VLM bench, VQA, hall-bench 모두 개선 
- **contribution :** 
- **etc. :**

## Details
### Preliminary 
LARGE LANGUAGE MODELS CAN SELF-IMPROVE https://arxiv.org/abs/2210.11610

### Proposed

<img width="556" alt="image" src="https://github.com/user-attachments/assets/33f0caed-767e-4d0b-a1a5-1ceb1be467a3">

<img width="618" alt="image" src="https://github.com/user-attachments/assets/2a57777e-46be-4f36-9fbc-eef68ba90313">


VLM으로 샘플들 생성하고 (beam search decoding) 각 문장별로 reward를 매기고 이 reward의 합으로 전체 시퀀스의 점수를 매김.
good / bad response를 뽑고 이걸로 DPO 학습 
학습된 VLM으로 다시 샘플등 생성하고 ... 이렇게 세번 반복

#### Reward
Text score + image score의 합 
<img width="220" alt="image" src="https://github.com/user-attachments/assets/6c54465e-bd95-4d13-a158-b4e67839b5fe">

$\lambda$는 하이퍼파라미터. 0.9로 셋팅 

- text score
<img width="264" alt="image" src="https://github.com/user-attachments/assets/9a146c70-225d-443e-a802-ae1ed1a2d4a7">

$x$ : prompt 
$r_i$ : ith response token
$s$ : sentence
$R_t$ : LVLM의 text decoder 부분.

재밌는건 문장만 들어가고 이미지는 안들어가고, 이전 문장도 안들어감. 논문에서는 instruction following score라고 표현 

- image score
<img width="256" alt="image" src="https://github.com/user-attachments/assets/94cee736-20d8-4aae-9d62-a2ac5c22e676">

CLIPScore.


### Result 
<img width="563" alt="image" src="https://github.com/user-attachments/assets/7ac6c597-e9ff-4ac7-bfc1-16eb9deb8139">

- comparsion with other vlms
<img width="555" alt="image" src="https://github.com/user-attachments/assets/462cf0e3-a561-46c6-847b-e1fcb5a262f1">

- iterative 하면서 결과 
<img width="586" alt="image" src="https://github.com/user-attachments/assets/b4b4c39c-65d4-4816-a2c8-b83bf350609b">

<img width="287" alt="image" src="https://github.com/user-attachments/assets/868224ae-2cd4-46d0-b85c-1ebe839dcba2">

<img width="608" alt="image" src="https://github.com/user-attachments/assets/cff91c75-e91f-4769-81cb-d37f00e51f61">


### ablations

<img width="180" alt="image" src="https://github.com/user-attachments/assets/75652474-718c-4620-a436-626001e37d0c">
