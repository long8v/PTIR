---
title: "[178] RLAIF-V: Aligning MLLMs through Open-Source AI Feedback for Super GPT-4V Trustworthiness"
date: 2024-09-23
tags: ['RL', 'MLLM', '2024Q2']
paper: "https://arxiv.org/pdf/2405.17220"
issue: 197
issueUrl: "https://github.com/long8v/PTIR/issues/197"
---
![image](https://github.com/user-attachments/assets/06dc30a8-03d1-4cb2-a384-49c734fb1098)


[paper](https://arxiv.org/pdf/2405.17220), [code](https://github.com/RLHF-V/RLAIF-V)

## TL;DR
- **I read this because.. :** RLHF-V 후속작
- **task :** vision-RLHF 
- **problem :** human annotated preference data는 scalable하지 않다
- **idea :** peer LVLM들에게 평가를 받자. 이때, reward를 논리 단위로 나눈 뒤 binary question으로 바꾸고 이에 대해 정답이 맞는지 틀린지로 점수를 매기자.
- **input/output :** {image, question} -> answer
- **architecture :** LLaVA 1.5, OmniLMM
- **objective :** DPO loss
- **baseline :** VCD, Less-is-more, LURE, QEWEn-VL, LLaVA-NeXT, Minigemini, HA-DPO, POVID, LLaVA-RLHF, Silikie, RLHF-V
- **data :** image - instruction from {MSCOCO, ShareGPT-4V, MovieNet, GoogleLandmark v2, VQA v2, OKVQA, TextVQA} => DPO data 로 제작 
- **evaluation :** trustworthiness(Object Halbench, MMHal-Bench, MHumanEval, AMBER), helpfulness(LLaVA Bench, MMStar) 
- **result :** trustworthiness 부분에서 GPT-4V를 넘어서는 성능. 
- **contribution :** 빠르게 RLAIF를 VLM에 붙임!
- **etc. :** iterative alignment 등.. 굉장히 고된 작업일듯 

## Details
### performance 
![image](https://github.com/user-attachments/assets/0cb4887c-7a8e-463f-b01c-2cbd9ffc99b1)

### RLAIF-V
![image](https://github.com/user-attachments/assets/25cf0fbf-269e-4236-bbdc-beedb8de141e)

1) response generation 
seed를 다르게 해서 대상이되는 모델에 대해서 답변을 n개 생성하라고 함 

2) response evaluation
- divide
답변이 길고 여러가지 statement를 포함하고 있기 때문에 이를 atomic한 statement로 나눈다.

- conquer
각 claim의 trustworthiness를 측정하기 위해서 binary question으로 바꾼다. (무조건 답은 yes)
그리고 Labeler model에게 질문하여 대답을 매긴다. 

- combine
claim에 대한 대답이 더 많은 답변을 $n_{rej}$로 표시할 때 최종적인 score S를 $-n_{rej}$로 구한다
그 뒤 score의 차이가 있는 두 답변 Pair를 구하고 instruction 당 최대 2개의 pair를 Sampling해서 사용한다.
이때 filtering process등이 의미가 없었다. 

3) iterative alignment
단순히 DPO를 적용하는 경우 학습 과정동안 model output distribution이 달라지는 "distribution shift problem"이 있다. (이에 대한 인용은 Scaling Laws for Reward Model Overoptimization)
이를 해결하기 위해 학습 -> DPO 데이터 수집 -> 학습을 반복하는 Iterative alignment를 제안
![image](https://github.com/user-attachments/assets/cbd2733a-cacf-4917-9b72-de290992c5b7)

가장 최신의 Instruction model $M_i$를 가지고 generation을 하고 위의 divide-and-conquer 전략으로 pair를 만들고 이를 학습하고 이를 반복

### Experiment 
- hparams
  - base models
    - LLaVA 1.5를 instruction model -- 대응하는 labeler모델은 LLaVA-NeXT (Nous-Hermes-2-Yi-34B)
    - OmniLMM -- 대응하는 Labeler 모델은 같은 Labeler model  (no-RLHF)
  - 4 epochs, lr 5e-7, beta 0.1, bs 8
  - 4 iterations (4K instrctions)
  - 8 A100으로 7B /12B를 학습하는데
    - data collection 48h / 50h 
    - training 6h / 8h 가 걸림

### Result
![image](https://github.com/user-attachments/assets/f3f4c3e0-9fec-473a-aa07-09fc9e20d06c)

### analysis
#### deconfounded strategy
divide-and-conquer 전략으로 점수를 매기는 것에 대한 ablation
![image](https://github.com/user-attachments/assets/9e32cf0e-4b95-41af-8594-223995d99aaf)

- RLHF-V는 finegrained human feedback으로 학습된 것 
- adapted는 preferred response가 human annotation으로 바꾼 것

ours가 가장 좋게 나왔는데 
rlhf-v 데이터는 Muffin inference 결과를 finegrained하게 정정한 것이고, adapted는 human이 다시 쓴거여서 그런지 성능차이가 꽤 났다.
DPO를 할 때 자기 자신의 Inference 결과를 쓰는게 그렇게까지 중요한건가? 싶었다.

- Self rewarding vs divide-and-conquer
self-rewarding은 그냥 labeler에게 prompt 길게 주고 response를 점수로 매겨달라고 하는 방식. 
![image](https://github.com/user-attachments/assets/0c4b7715-2727-44bd-a4eb-124157201a0f)

제안한 방식이 확실히 효과적이었다.

- iterative alignment 
![image](https://github.com/user-attachments/assets/2bdc3a10-0663-4b00-899b-c45e67a97b4b)

iterative alignment 방식이 아닌 경우 성능이 금방 saturate하는 양상을 보였다.


- data source // multiple lvlm
다른 데이터와 함께 썼을 때 성능이 일관적으로 올랐다
![image](https://github.com/user-attachments/assets/957c5953-c845-42fa-92c8-0c0ec9758255)
 
다양한 Lvlm에서 잘 동작했고 그중에 OmniLMM이 가장 성능이 좋았따. 
