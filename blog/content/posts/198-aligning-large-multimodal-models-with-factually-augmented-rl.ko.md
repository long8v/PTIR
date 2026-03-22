---
title: "[179] Aligning Large Multimodal Models with Factually Augmented RLHF"
date: 2024-09-25
tags: ['25min', 'RL', '2023Q3', 'MLLM', 'Berkley']
paper: "https://arxiv.org/abs/2309.14525"
issue: 198
issueUrl: "https://github.com/long8v/PTIR/issues/198"
---

<img width="648" alt="image" src="https://github.com/user-attachments/assets/4c2d8b52-6625-4961-b507-281693a33f54">

[paper](https://arxiv.org/abs/2309.14525), [code](https://github.com/llava-rlhf/LLaVA-RLHF)

## TL;DR
- **I read this because.. :** VLM RL 초기작. PPO 써서.
- **task :** VLM + RL
- **problem :** VLM의 hallucination
- **idea :** PPO 적용해보자! 한가지 다른 점은 reward model에 human annotation(caption 등)을 추가로 넣어주자
- **input/output :** {image, question} -> answer
- **architecture :** LLaVA 7B (vicuna) 
- **objective :** PPO loss 
- **baseline :** OpenFlamingo, MiniGPT-4, InstructBLIP, LLaVA-SFT
- **data :** LLaVA SFT 모델로 10K sample을 만든 뒤 Human annotated preference data만듦 
- **evaluation :** MMBench, LLaVA-w, POPE, MMHal (proposed)
- **result :** MMBench 개선 (finegrained perception) 
- **contribution :** VLM에 RLHF를 붙인 거의 처음 연구
- **etc. :**

## Details

### Proposed
<img width="678" alt="image" src="https://github.com/user-attachments/assets/70830c97-2116-4e72-a909-0aec02087542">

- humna preference data collection
temperature 0.7로 SFT 모델에 대해 10K의 LLaVA held-out 데이터를 만듦 (이미지 소스는?)
human prefernce annotation 받을 때 Instruction 
<img width="702" alt="image" src="https://github.com/user-attachments/assets/d21f4201-12d2-41b3-8339-5c228815360c">

RM model에게 주는 prompt. 추가적으로 caption 등을 줬다고 해서 factually augmented rlhf 
<img width="663" alt="image" src="https://github.com/user-attachments/assets/5fe4c1d4-7bdc-4ee7-bde5-5f6d83beb043">

### MMHal-Bench 
수량은 96개이고 8개의 카테고리(object attribute, adversairal object, comparsion, counting, spatial relation, environment, holistic, others)에 대해 12개 질답을 만듦.
이미지 소스는  OpenImages이고 text-only GPT4에게 이미지 컨텐츠에 대한 사람이 생성한 답변과 이미지 내에 있는 (아마 Object의) 카테고리도 같이 줌. gpt4의 평가 결과는 human과 94% 일치함. 

### Result
- LLaVA bench
<img width="693" alt="image" src="https://github.com/user-attachments/assets/c4d1d9e1-e5ee-4bbb-8ab6-0bd38a319862">

- mmhal bench
<img width="665" alt="image" src="https://github.com/user-attachments/assets/bd47e34c-e12f-4fc9-b7a2-8597a6967acd">

- mmbench 
 
<img width="680" alt="image" src="https://github.com/user-attachments/assets/d2cd9e6c-bca3-41ee-a48c-1683d2b7a7ca">

### Qualitative result 
<img width="661" alt="image" src="https://github.com/user-attachments/assets/3b7b1234-9cf6-45e2-86ca-0d1c5a4d078d">


### Ablation
- SFT data ablation
<img width="674" alt="image" src="https://github.com/user-attachments/assets/1b6cfab8-2fc8-40bd-b352-946982bde3f1">

VQA 데이터가 POPE 개선에 도움 