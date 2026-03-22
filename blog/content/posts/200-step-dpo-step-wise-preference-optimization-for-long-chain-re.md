---
title: "[181] Step-DPO: Step-wise Preference Optimization for Long-chain Reasoning of LLMs"
date: 2024-10-07
tags: ['LLM', 'RL', '2023Q3']
paper: "https://arxiv.org/abs/2406.18629"
issue: 200
issueUrl: "https://github.com/long8v/PTIR/issues/200"
summary: "I was wondering how to divide the step and read it. - data disclosure. There seems to be a lot of this kind of thing, but I don't know if this is the first one"
---
![image](https://github.com/user-attachments/assets/92c31320-5086-4e26-84fb-99ea0e73cf89)

[paper](https://arxiv.org/abs/2406.18629), [code/data](https://github.com/dvlab-research/Step-DPO)

## TL;DR
- **I read this because.. :** mentioned. I was wondering how to divide the steps.
- **task :** LLM in reasoning
- **problem :** DPO is widely used, but performance gains in long-context are limited
- **idea :** DPO loss to maximize win/loss steps for incorrect steps if there is long reasoning
- **architecture :** Qwen2, Qwen1.5 Meta-Llama-3-70B, deepseek-math-7b-base
- **objective :** step-DPO (proposed)
- **baseline :** SFT, DPO
- **data :** 374K pair data (proposed) with the first incorrect step stored, AQuA
- **evaluation :** MATH, GSM8K, AIME, Odyssey-MATH
- **result :** Better performance than DPO. Said to have beaten GPT-4-1106, Claude-3-Opus, and Gemini-1.5-Pro.
- **contribution :** data disclosure. There seem to be a lot of these, but I don't know if this is the first one
- **etc. :** 

## Details
### Performance
![image](https://github.com/user-attachments/assets/bfe19b44-26f1-4a60-950b-662af2d2534b)

### motivation
The disadvantage of SFT in this paper is that it increases the likelihood of undesirable outputs as well as desirable outputs -> prone to hallucination
To solve this problem, RLHF provides undesriable supervision, but DPO is said to be ineffective for long sequence output. (due to lack of fine-grained process supervision)

![image](https://github.com/user-attachments/assets/faf6a212-4956-42eb-8d29-3a3df42cad71)

### Step-DPO
![image](https://github.com/user-attachments/assets/49593a57-00f7-4e12-9e8d-82af8a19ce4e)

Maximize the win -- lose margin for the wrong step, not the entire sequence.
![image](https://github.com/user-attachments/assets/683ac8cb-3901-46e0-a5fa-cbbe3e9aeeac)

- $s_i$ : i-th reasoning step
- $x$ : prompt
- $k$ : first incorrect step

### In-distribtuion data construction
The goal is to create something like this
![image](https://github.com/user-attachments/assets/77d6c95f-1add-4787-8e9f-6adeae7edd2c)

Pipelines
![image](https://github.com/user-attachments/assets/543b407f-9e67-4749-aa6e-a35167ee889f)

- error collection 
A collection of problems x and gt answer $\hat{y}$.
Take reference model $\pi_{ref}$ and run it with step-wise CoT preifx and divide by step
A collection of things where final answer y is different from gt answer.

- step localization
Find the first incorrect $k$ in the reasoning step $y=s_1, s_2, ... , s_n$. (manually or via gpt-4)
Select $s_{lose}$ as the error of the wrong step k

- rectification
Given a suitable ressoning step $s_{1~{k-1}}$, infer multiple times to the reference model to get multiple
![image](https://github.com/user-attachments/assets/4a20ae72-9236-43ca-8591-2197bb1a4766)

Of these, the one whose final answer matches gt is selected as $s_{win}$.
Even if the answer is correct, the process can be incorrect, which is refined manually or with gpt-4 (not shown)

### Result
- Collected 374K in total, of which 299K was SFT data and 75K was Step-DPO
- SFT is a 3 or 2 epoxy
- Step-DPO is 8 or 4 epoxy turns
- Using the AQuA dataset in addition to the SFT dataset

![image](https://github.com/user-attachments/assets/2bc68a78-0ea1-4877-b034-19453b43c5cd)

![image](https://github.com/user-attachments/assets/60c5c28c-54df-4b4e-91df-af783cc9e7a2)

### Ablation
- DPO vs Step-DPO
![image](https://github.com/user-attachments/assets/ae42e31b-821c-44c5-9426-79eb0f34d012)

- in-distribution vs out-distribution
![image](https://github.com/user-attachments/assets/2a028e47-4231-4551-a21d-094155dc7c97)

It's important that the data we use is the result of inference from the model we trained.