---
title: "[169] Direct Preference Optimization: Your Language Model is Secretly a Reward Model"
date: 2024-08-26
tags: ['2023Q2', 'RL']
paper: "https://arxiv.org/abs/2305.18290"
issue: 188
issueUrl: "https://github.com/long8v/PTIR/issues/188"
summary: "Background Difference - Similar or better performance than baseline"
---

<img width="663" alt="image" src="https://github.com/user-attachments/assets/7c20da97-960b-440f-a2fb-222c5b737151">

[paper](https://arxiv.org/abs/2305.18290)

## TL;DR
- **I read this because.. :** Background Tea
- **task :** RL
- **problem :** TRPO also needs to learn a separate reward model, which is too hard as the model grows.
- **IDEA :** Can we learn LOSS to REWARD directly without a reward model?
- **input/output :** {state, reward} -> action
- **architecture :** GPT2-Large 
- **objective :** proposed. 
- **baseline :** zero-shot to GP-J, SFT, Preferre-ft, Unlikelihood, PPO, PPO-GT, Bes of N baseline (returns the most rewarding of the SFT responses)
- **data :** IMDb , Reddit TL;DR 
- **evaluation :** GPT-4 Evaluator 
- **result :** Similar or better performance than baseline
- **contribution :**
- **etc. :** Professor Finn, I see you here ..!

## Details
### Preliminaries 
- SFT 
Create $\pi^{SFT}$ using a small amount of good quality data


- Reward modeling (Bradley-Terry model)
<img width="372" alt="image" src="https://github.com/user-attachments/assets/d88ad225-4243-4068-8d26-fab50136755c">

If we replace this with a binary problem
<img width="405" alt="image" src="https://github.com/user-attachments/assets/e4117f85-2224-43cd-93e6-12c53bce301d">

- RL finetuning phrase
<img width="307" alt="image" src="https://github.com/user-attachments/assets/8aaacc7c-92f3-4107-bd24-5b63995593c4">


### DPO
If we rewrite the above function
<img width="289" alt="image" src="https://github.com/user-attachments/assets/ad6ba144-f2f9-4293-a670-59b0a65ed5df">

<img width="615" alt="image" src="https://github.com/user-attachments/assets/96720180-dada-43a7-9566-f7d04ba02e70">

What does a partition function do for a probability distribution?

For the optimal policy, the bradely-terry model has the following preferences

<img width="400" alt="image" src="https://github.com/user-attachments/assets/917fbd79-edc4-4816-b9b4-56eab9295668">

From a policy perspective, we have human preference data, so we can express this as an MLE objective by using the
<img width="534" alt="image" src="https://github.com/user-attachments/assets/6ade48b4-065e-4366-b5c1-7fde9a702fa6">

### what does the DPO updates?
<img width="604" alt="image" src="https://github.com/user-attachments/assets/15c6c893-17d1-447d-ba4c-d3291de19e5d">
