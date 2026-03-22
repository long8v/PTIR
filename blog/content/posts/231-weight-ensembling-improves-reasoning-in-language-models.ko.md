---
title: "[210] Weight Ensembling Improves Reasoning in Language Models"
date: 2025-05-30
tags: ['RL', 'reasoning', '2025Q2']
paper: "https://arxiv.org/abs/2504.10478"
issue: 231
issueUrl: "https://github.com/long8v/PTIR/issues/231"
---
<img width="860" alt="Image" src="https://github.com/user-attachments/assets/e3ff76a5-77c8-447d-a72b-758bfdff3d5a" />

[paper](https://arxiv.org/abs/2504.10478)

## TL;DR
- **I read this because.. :**  SFT를 너무 많이 하는게 안좋나?2 
- **task :** reasoning model 
- **problem :** SFT를 진행함에 따라 pass@1은 개선되는데 pass@k가 악화되는 경향성
- **idea :** pretrained와 SFT를 weight ensembling 하자
- **input/output :** prompt -> {reasoning, answer}
- **architecture :** {Gemma-2-2B, Qwen-2.5-0.5B}
- **objective :** ce loss, GRPO loss 
- **baseline :** SFT, temperature majority voting
- **data :** SFT {GSM8K, [OpenThoughts-114k](https://huggingface.co/datasets/open-thoughts/OpenThoughts-114k/viewer/default/train?row=0)(cold-start SFT)} -> GRPO {30K subset of rephrased question from MetaMath}
- **evaluation :** AIME24, MATH500, GSM8K / majority voting, BoN 
- **result :** SFT를 진행함에 따라 diversity가 떨어짐을 보임. SFT를 더 많이 할수록 RL 성능의 상한도 떨어짐. Wise-FT를 할 경우 가장 최선이고 이 성능은 temperature를 다양화하며 BoN을 하는것보다 나음 
- **contribution :** 다양한 분석 
- **etc. :** 2B, 0.5B에서만 진행된게 한계라고 함 

## Details
- related work 
  - PRESERVING DIVERSITY IN SUPERVISED FINE-TUNING OF LARGE LANGUAGE MODELS 
  - Inference-Aware Fine-Tuning for Best-of-N Sampling in Large Language Models 
- pass@1 vs pass@k tradeoff

<img width="790" alt="Image" src="https://github.com/user-attachments/assets/209217ce-1082-4f8c-bc64-40a8b490c5c3" />

- better test time scaling / RL scaling 
<img width="789" alt="Image" src="https://github.com/user-attachments/assets/230f0b22-2a53-49e9-9536-08e5e2681325" />

- diversity collapse 

<img width="815" alt="Image" src="https://github.com/user-attachments/assets/6ba25d2b-3fb8-4425-a0ec-04e07b59b032" />

SFT가 진행됨에 따라 AIME2024의 unique answer 비율 
<img width="767" alt="Image" src="https://github.com/user-attachments/assets/4e8d085e-2aea-4acc-a077-405b47a9ae03" />

<img width="728" alt="Image" src="https://github.com/user-attachments/assets/9e9afa61-db8e-4e68-a716-0a28e8f4a21f" />

- 서로 다른 SFT step ckpt에 대한 PPO further training 성능 

<img width="797" alt="Image" src="https://github.com/user-attachments/assets/ca5ed121-a58a-4880-aa2c-bc8a22023a2b" />

1) KL regularization 없이는 policy diversity 가 붕괴됨
2) 그렇다고 KL regularization을 넣는다고  해서 기존의 diversity보다 넘어서는 policy로 수렴할 수 있는 것은 아님 ==> appendix에서 증명 

<img width="791" alt="Image" src="https://github.com/user-attachments/assets/b0a73c17-99ea-4089-8dcf-d67052277505" />

pass@k는 jensen's inequality에 따라 bias와 variance에 upper bound가 생김.

<img width="752" alt="Image" src="https://github.com/user-attachments/assets/654434ea-5127-4ed0-a045-87071e473de2" /> 

<img width="801" alt="Image" src="https://github.com/user-attachments/assets/ac741e20-e10d-47e1-992d-864d2205049e" />

SFT를 함에 따라 pass@1 variance가 높아짐. (틀린건 무조건 틀리고 맞는건 무조건 맞음) (==response diversity가 떨어지는 방향.)

<img width="815" alt="Image" src="https://github.com/user-attachments/assets/b04de3c7-04ac-4b4e-a134-027eebc21c17" />