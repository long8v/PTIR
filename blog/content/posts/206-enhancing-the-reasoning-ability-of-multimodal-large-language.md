---
title: "Enhancing the Reasoning Ability of Multimodal Large Language Models via Mixed Preference Optimization"
date: 2024-11-21
tags: ['RL', 'MLLM', '2024Q4', 'SHU']
paper: "https://arxiv.org/abs/2411.10442"
issue: 206
issueUrl: "https://github.com/long8v/PTIR/issues/206"
summary: "reasoning in LVLM - Dataset released. The proposed LOS combination also performs well"
---

<img width="1092" alt="image" src="https://github.com/user-attachments/assets/b3dd4dc1-edc2-4300-86bd-20966ec81585">

[paper](https://arxiv.org/abs/2411.10442), [dataset](https://huggingface.co/datasets/OpenGVLab/MMPR), [code](https://github.com/OpenGVLab/InternVL/tree/main/internvl_chat/shell/internvl2.0_mpo)

## TL;DR
- **I read this because.. :** reasoning in LVLM
- **task :** MLLM 
- Problem :** MLLM's CoT ability is poor
- Idea:** Let's create CoT data + Learn DPO
- **architecture :** InternVL2-8B
- **objective :** DPO loss + CE loss + [BCOloss](https://arxiv.org/html/2404.04656v1)
- **baseline :** InternVL2-8B, InternVL2-8B-SFT, DPO variants, Gemini, GPT4o, LLaVA-1.5-13B, Qwen2VL-7B, ...
- **data :** proposed MMPR (3.2M)
- **evaluation :** M3CoT, Mathvista, MathVision, MMVET, LLaVA-Bench, POPE, CRPE, MMHalbench
- Result :** Significantly improved CoT ability and math performance (mathvista 67.0). Claimed that preference optimization over SFT was critical for CoT performance.
- **contribution :** Dataset released. The proposed LOS combination also performs well
- **etc. :**

## Details
- thumbnail
<img width="570" alt="image" src="https://github.com/user-attachments/assets/ede24053-fcb1-4421-91bd-6f323c19fb4d">

### MMPR dataset 
If there is an answer, it is selected if the answer is correct, or loose
In the case of unanswered questions, we select all the generated children as chosen, and in the case of loose, we cover half of the generated sentences and ask them to generate the rest. This is said to cause a lot of hallucinations. (?) -- Name it DropNTP
2.5M answered data // 750K unanswered data

- examples
<img width="1089" alt="image" src="https://github.com/user-attachments/assets/acc1d0d0-181b-4b5f-9f89-0237912e2b44">

- source
<img width="518" alt="image" src="https://github.com/user-attachments/assets/374bf238-c128-4e2c-ae10-19337e0a4289">

### MPO Loss
Combination of DPO loss (0.8) + BCO loss (0.2) + SFT loss (1) (smaug also showed that dpo doesn't generate rationale?)

<img width="179" alt="image" src="https://github.com/user-attachments/assets/81c0f572-99d9-4f04-867f-806450880b35">

- BCO loss
<img width="136" alt="image" src="https://github.com/user-attachments/assets/4c520ad0-1129-4311-a11b-0394a459fda0">

<img width="200" alt="image" src="https://github.com/user-attachments/assets/6ad689c7-4356-4d44-8af7-ad825347b2bb">

We learn together a binary classifier for good or bad, and the delta over there is a moving average of past rewards.

### Result

<img width="1097" alt="image" src="https://github.com/user-attachments/assets/d33a6910-9a4d-48af-916b-5af3892cd085">

Significantly improved CoT bench and math bench (similar performance to 76B variant)

- text benchmarks
<img width="1095" alt="image" src="https://github.com/user-attachments/assets/5a565c67-6a32-4b92-91aa-fdcf3db37eb9">

Improved performance with significant increases in TheoremQA, a complex science question, and IFEval, an instruction following bench.
text Isn't there a CoT bench...?

#### Ablations
- SFT loss vs MPO
<img width="527" alt="image" src="https://github.com/user-attachments/assets/78de261c-733c-4304-9b97-6bf0a6415764">

Overall increase in both direct / CoT when putting CoT with SFT
When put into MPO, both direct / CoT improve significantly, with CoT > direct grades on all benches

- DropNTP vs RLAIF
<img width="529" alt="image" src="https://github.com/user-attachments/assets/477a9366-0d6a-4897-8131-bfc476b82f0d">

Suggested method is simpler and better for hallucination

- DPO variants
<img width="1093" alt="image" src="https://github.com/user-attachments/assets/c8940c36-df73-4044-81f9-767fd6849ca5">

First of all, they all performed better than SFTs, but simply using DPO loss did not improve CoT performance over direct.
