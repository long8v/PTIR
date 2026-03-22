---
title: "[210] Weight Ensembling Improves Reasoning in Language Models"
date: 2025-05-30
tags: ['RL', 'reasoning', '2025Q2']
paper: "https://arxiv.org/abs/2504.10478"
issue: 231
issueUrl: "https://github.com/long8v/PTIR/issues/231"
summary: "Is it bad to do too much SFT? 2 - Various Analytics"
---
<img width="860" alt="Image" src="https://github.com/user-attachments/assets/e3ff76a5-77c8-447d-a72b-758bfdff3d5a" />

[paper](https://arxiv.org/abs/2504.10478)

## TL;DR
- **I read this because.. :** Is it bad to do too much SFT?2
- **task :** reasoning model 
- **problem :** As SFT progresses, pass@1 improves but pass@k tends to worsen
- **idea :** weight ensemble pretrained and SFT
- **input/output :** prompt -> {reasoning, answer}
- **architecture :** {Gemma-2-2B, Qwen-2.5-0.5B}
- **objective :** ce loss, GRPO loss 
- **baseline :** SFT, temperature majority voting
- **data :** SFT {GSM8K, [OpenThoughts-114k](https://huggingface.co/datasets/open-thoughts/OpenThoughts-114k/viewer/default/train?row=0)(cold-start SFT)} -> GRPO {30K subset of rephrased question from MetaMath}
- **evaluation :** AIME24, MATH500, GSM8K / majority voting, BoN 
- Result :** Diversity decreases as SFT progresses. The upper bound of RL performance drops as we do more SFT. Wise-FT is best and this performance is better than BoN with temperature diversification.
- **contribution :** Various analytics
- **etc. :** 2B, 0.5B is said to be the limit

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

Percentage of unique answers in AIME2024 as SFT progresses
<img width="767" alt="Image" src="https://github.com/user-attachments/assets/4e8d085e-2aea-4acc-a077-405b47a9ae03" />

<img width="728" alt="Image" src="https://github.com/user-attachments/assets/9e9afa61-db8e-4e68-a716-0a28e8f4a21f" />

- PPO further training performance for different SFT step ckpts

<img width="797" alt="Image" src="https://github.com/user-attachments/assets/ca5ed121-a58a-4880-aa2c-bc8a22023a2b" />

1) Policy diversity breaks down without KL regularization
2) This does not mean that adding KL regularization can converge to a policy that is better than the existing diversity ==> Proof in appendix

<img width="791" alt="Image" src="https://github.com/user-attachments/assets/b0a73c17-99ea-4089-8dcf-d67052277505" />

pass@k has upper bounds on bias and variance according to jensen's inequality.

<img width="752" alt="Image" src="https://github.com/user-attachments/assets/654434ea-5127-4ed0-a045-87071e473de2" /> 

<img width="801" alt="Image" src="https://github.com/user-attachments/assets/ac741e20-e10d-47e1-992d-864d2205049e" />

SFT increases the pass@1 variance. (Wrong is always wrong and right is always right) (==direction of decreasing response diversity.)

<img width="815" alt="Image" src="https://github.com/user-attachments/assets/b04de3c7-04ac-4b4e-a134-027eebc21c17" />