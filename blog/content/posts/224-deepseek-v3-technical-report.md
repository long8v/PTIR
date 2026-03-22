---
title: "DeepSeek-V3 Technical Report"
date: 2025-02-13
tags: ['WIP', '25min', 'LLM', 'RL', '2024Q4']
paper: "https://arxiv.org/abs/2412.19437"
issue: 224
issueUrl: "https://github.com/long8v/PTIR/issues/224"
summary: "I was wondering about the post training"
---
![Image](https://github.com/user-attachments/assets/e532c76a-e9e1-4106-a0fa-76cb277ff0f6)

[paper](https://arxiv.org/abs/2412.19437)

## TL;DR
- **I read this because.. :** I was wondering about the post training
- **task :** LLM 
- **problem :** 
- **idea :** 
- **input/output :**
- **architecture :**
- **objective :**
- **baseline :**
- **data :** 
- **evaluation :**
- **result :**
- **contribution :**
- **etc. :**

## Details
### Post-training
- SFT
- Collected 1.5M of instruction tuning data for different domains
  - Reasoning data
- Created with internal Deepseek-R1.
- However, the goal is to balance the high accuracy of r1 with the conciseness of normal, well-formatted reasoning data without overthinking, poor formatting, or excessive length.
- To do this, we want to create sft + rl trained expert models for specific domains such as code, math, general reasoning, and use them as data generators.
- The training aims to generate two different SFT samples. One is <problem, original response> <`system prompt`, problem, R1 response>
- The system prompts are carefully designed to allow for reflection and verification.
- In the RL phase, the model does high temperature sampling, allowing both r1-generated and original data to be generated without a system prompt.
- RL and then rejection sampling to keep only high quality sft.
  - Non-reasoning data
- Created with Deepseek v2.5 and validated for accuracy by human annotators
  - SFT -- two epochs
- Reinforcement Learning
  - Reward Model
    - Rule-based RM
- math: formatted (in a box) followed by rule based / code: compiler to test code (leetcode)
    - Model-based RM    
      - for free-form ground-truth answer
- Learned from DeepSeek-v3 sft checkpoints. Generated CoTs before reward cycle -> helped with reward hacking
    - GRPO
- Learning with GRPO, which computes in groups without a critic model
      - ![Image](https://github.com/user-attachments/assets/2c288d3b-e128-4239-9319-dc8fd48b87cf)
      - ![Image](https://github.com/user-attachments/assets/740b23e3-7858-489f-a5bd-994f7da7b479)
- $o_i$ is samples from old policy
     
### Ablations
- distiliation from deepseek-r1

![Image](https://github.com/user-attachments/assets/72dc4f63-6962-4d4a-bf62-d2a3f45e88ac)

   