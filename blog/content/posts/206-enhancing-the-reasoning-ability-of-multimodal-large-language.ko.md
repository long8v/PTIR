---
title: "[187] Enhancing the Reasoning Ability of Multimodal Large Language Models via Mixed Preference Optimization"
date: 2024-11-21
tags: ['RL', 'MLLM', '2024Q4', 'SHU']
paper: "https://arxiv.org/abs/2411.10442"
issue: 206
issueUrl: "https://github.com/long8v/PTIR/issues/206"
---

<img width="1092" alt="image" src="https://github.com/user-attachments/assets/b3dd4dc1-edc2-4300-86bd-20966ec81585">

[paper](https://arxiv.org/abs/2411.10442), [dataset](https://huggingface.co/datasets/OpenGVLab/MMPR), [code](https://github.com/OpenGVLab/InternVL/tree/main/internvl_chat/shell/internvl2.0_mpo)

## TL;DR
- **I read this because.. :** reasoning in LVLM
- **task :** MLLM 
- **problem :** MLLM의 CoT 능력 떨어짐
- **idea :** CoT 데이터 만들자 + DPO 학습하자 
- **architecture :** InternVL2-8B
- **objective :** DPO loss + CE loss + [BCOloss](https://arxiv.org/html/2404.04656v1)
- **baseline :** InternVL2-8B, InternVL2-8B-SFT, DPO variants, Gemini, GPT4o, LLaVA-1.5-13B, Qwen2VL-7B, ...
- **data :** proposed MMPR (3.2M)
- **evaluation :** M3CoT, Mathvista, MathVision, MMVET, LLaVA-Bench, POPE, CRPE, MMHalbench
- **result :** CoT 능력과 math쪽 성능을 크게 개선 (mathvista 67.0). SFT보다 preference optimization을 하는게 CoT 성능에 크리티컬했다고 주장. 
- **contribution :** 데이터셋 공개. 제안한 loss 조합도 성능이 좋음
- **etc. :**

## Details
- thumbnail
<img width="570" alt="image" src="https://github.com/user-attachments/assets/ede24053-fcb1-4421-91bd-6f323c19fb4d">

### MMPR dataset 
답이 있는 경우엔 답이 맞으면 chosen / 아니면 loose
답이 없는 경우엔 일단 생성한 애를 다 chosen으로 선택하고, loose의 경우는 생성된 문장의 반을 가려놓고 나머지를 생성하라고 함. 이때 hallucination이 많이 생겼다고 함. (?) -- DropNTP로 이름 붙임
2.5M 답이 있는 데이터 // 750K 답이 없는 데이터 

- examples
<img width="1089" alt="image" src="https://github.com/user-attachments/assets/acc1d0d0-181b-4b5f-9f89-0237912e2b44">

- source
<img width="518" alt="image" src="https://github.com/user-attachments/assets/374bf238-c128-4e2c-ae10-19337e0a4289">

### MPO Loss
DPO loss (0.8) + BCO loss (0.2) + SFT loss (1) 의 조합 (dpo가 rationale을 생성하지 못한다는게 smaug에서도 보였다고?)

<img width="179" alt="image" src="https://github.com/user-attachments/assets/81c0f572-99d9-4f04-867f-806450880b35">

- BCO loss
<img width="136" alt="image" src="https://github.com/user-attachments/assets/4c520ad0-1129-4311-a11b-0394a459fda0">

<img width="200" alt="image" src="https://github.com/user-attachments/assets/6ad689c7-4356-4d44-8af7-ad825347b2bb">

좋은지 나쁜지에 대한 binary classifier를 같이 학습하고 저기 델타는 과거 reward들 moving average.

### Result

<img width="1097" alt="image" src="https://github.com/user-attachments/assets/d33a6910-9a4d-48af-916b-5af3892cd085">

CoT 벤치랑 math쪽 벤치 크게 개선 (76B variant랑 비슷한 성능)

- text benchmarks
<img width="1095" alt="image" src="https://github.com/user-attachments/assets/5a565c67-6a32-4b92-91aa-fdcf3db37eb9">

complex science 문제인 TheoremQA와 Instruction following 벤치인 IFEval이 크게 늘어서 성능 개선.
text CoT 벤치는 없는건가..? 

#### Ablations
- SFT loss vs MPO
<img width="527" alt="image" src="https://github.com/user-attachments/assets/78de261c-733c-4304-9b97-6bf0a6415764">

SFT로 CoT를 넣었을 때 direct / CoT 둘다 전반적으로 늘어남
MPO로 넣었을 때 direct / CoT 둘다 크게 개선되고 모든 벤치에서 CoT > direct 성적이 나옴

- DropNTP vs RLAIF
<img width="529" alt="image" src="https://github.com/user-attachments/assets/477a9366-0d6a-4897-8131-bfc476b82f0d">

제안한 방법이 더 간단하고 hallucination 쪽에서 더 좋다고 함 

- DPO variants
<img width="1093" alt="image" src="https://github.com/user-attachments/assets/c8940c36-df73-4044-81f9-767fd6849ca5">

일단 SFT들보다 다 성능이 좋았는데 단순히 DPO loss를 쓰면 CoT능력이 direct보다 좋아지지 않았다.
