---
title: "[200] Advancing Language Model Reasoning through Reinforcement Learning and Inference Scaling"
date: 2025-02-03
tags: ['25min', 'RL', '2025Q1', 'THU']
paper: "https://arxiv.org/abs/2501.11651"
issue: 221
issueUrl: "https://github.com/long8v/PTIR/issues/221"
summary: "The answer-only reward approach, which is all the rage these days - see also #220 for various ablations and methodologies"
---
<img width="572" alt="Image" src="https://github.com/user-attachments/assets/7251c675-ec9a-4662-965c-60b8885c48a6" />

[paper](https://arxiv.org/abs/2501.11651), [github](https://github.com/THUDM/T1)

## TL;DR
- **I read this because.. :** The answer-only reward approach that's all the rage these days
- **task :** RL reasoning
- **problem :** scale RL 
- **idea :** 1) make cot sft data good 2) let them explore a lot (temperature when exploring, entropy bonus) 3) reward only for correct answers + undesirable behavior
- **input/output :** Q -> A
- **architecture :** Qwen2.5-32B 
- **objective :** 1 or 0 reward  + RLOO + entropy bonus 
- **baseline :** QwQ-32B-preview 
- **data :** MATH-train, NuminaMATH
- **evaluation :** MATH500, AIME2024, Omni-math-500
- **result :** Higher performance than QwQ-32B-preview
- **contribution :** Various ablations and methodologies are also shown in #220 and similarly
- **etc. :** Now that I look at it again, it looks like you also emphasized on-policy a lot?

## Details
### overall pipeline 
<img width="932" alt="Image" src="https://github.com/user-attachments/assets/9d415a57-bcfe-48b3-b03a-83e5f733d069" />

There, the correct answer is compared to the ground truth, and if it's correct, it's either 1 or 0.

- Initializing Policy with CoT for Reasoning
A collection of different attempts to prompt X using different LLMs.

- scaling response sampling with high temperature
Give temperature more than 1 to get different responses
Reward scaling using RLOO
<img width="368" alt="Image" src="https://github.com/user-attachments/assets/20a25134-9c1d-4c95-9176-509623dea1cc" />

- auxiliary entropy bonus 

<img width="917" alt="Image" src="https://github.com/user-attachments/assets/56f7e8cf-ac3d-420e-877b-d1553d6a65a3" />

- on-policy kl divergence 

<img width="1075" alt="Image" src="https://github.com/user-attachments/assets/11fb733e-ffd3-4cee-8069-fa9233cd1c1d" />

Also scaling for KL divergence term

<img width="429" alt="Image" src="https://github.com/user-attachments/assets/bf0b33c6-3777-4a1d-a7d8-eb04ce3b0740" />

Applying EMA to a reference model

- Penalizing Unexpected Patterns in RL Training
<img width="566" alt="Image" src="https://github.com/user-attachments/assets/39852320-48b5-4b81-9acd-0d1e875cb06c" />

Add -1 to reward for repeated / overlong answer. This was detected by rule based (n-gram repetition, etc.)


### details 
- data construction
- Breaking down MATH, NuminaMATH for SFT/RL
- Apply additional filtering to SFT data -- remove data that is too easy or noisy.
- Generate 16 responses and keep the kids with a 0.3 or lower score.
 

### result
- overall results
<img width="1063" alt="Image" src="https://github.com/user-attachments/assets/7e1bc003-0244-4cfb-8187-c4d220eac566" />

- ablation on sampling more

<img width="1083" alt="Image" src="https://github.com/user-attachments/assets/edd06011-8afb-479e-8872-ebc599798f61" />

Increasing sampling K increases the length of answers and increases accuracy. (a), (b)
Also, for the same reward, the KL divergence is smaller and slower to increase (c) -- why is this good?

<img width="1070" alt="Image" src="https://github.com/user-attachments/assets/2fd77f0c-21e4-489e-b389-2336c4fb1847" />

Ultimate performance

- exploration

<img width="989" alt="Image" src="https://github.com/user-attachments/assets/dfdc92fa-ab94-4283-9821-05589f2fac96" />

<img width="965" alt="Image" src="https://github.com/user-attachments/assets/d3174a41-e63f-413f-8f7a-318f31df5546" />

1.2 is optimal. Too big is bad.

- penalty reward

<img width="1018" alt="Image" src="https://github.com/user-attachments/assets/6554f873-fb7b-427d-8cd3-ac03d23b556b" />

