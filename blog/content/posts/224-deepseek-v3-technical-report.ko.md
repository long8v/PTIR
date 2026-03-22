---
title: "[203] DeepSeek-V3 Technical Report"
date: 2025-02-13
tags: ['WIP', '25min', 'LLM', 'RL', '2024Q4']
paper: "https://arxiv.org/abs/2412.19437"
issue: 224
issueUrl: "https://github.com/long8v/PTIR/issues/224"
---
![Image](https://github.com/user-attachments/assets/e532c76a-e9e1-4106-a0fa-76cb277ff0f6)

[paper](https://arxiv.org/abs/2412.19437)

## TL;DR
- **I read this because.. :** post training이 궁금해서 
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
  - 1.5M의 다양한 도메인에 대한 instruction tuning data를 모음
  - Reasoning data
    - internal Deepseek-R1을 가지고 생성.
    - 그러나 overthink, poor formatting, excessive length 해서 r1의 높은 정확도와 보통의 잘 포맷팅 된 reasoning data의 concise 함을 잘 균형잡히게 하는게 목표
    - 이를 위해 code, math, general reasoning 과 같은 특정한 도메인에 sft + rl 학습된 Expert model 을 만들고 이를 data generator로 사용하고자 함
      - 학습은 두개의 다른 SFT sample을 생성하는데 목표. 하나는 <problem, original response> <`system prompt`, problem, R1 response>
      - 이때 system prompt는 reflection과 verification을 할 수 있도록 섬세하게 디자인함
    - RL phase에서는 model이 high temperature sampling을 하여 system prompt없이도r1-generated, original data 둘다 생성할 수 있게 함. 
    - RL을 하고 나서 rejection sampling을 하여 high quality sft만 남김. 
  - Non-reasoning data
    - Deepseek v2.5로 만들고 human annotator가 정확도를 검증함
  - SFT -- two epochs
- Reinforcement Learning
  - Reward Model
    - Rule-based RM
     - math: format에 맞춘(in a box) 뒤 rule based / code: compiler to test code (leetcode)  
    - Model-based RM    
      - for free-form ground-truth answer
      - DeepSeek-v3 sft checkpoint로 부터 학습. reward 주기 전에 CoT 생성 -> reward hacking에 도움되었다고 함 
    - GRPO
      - critic model이 없이 group으로 묶여서 계산 하는 GRPO로 학습 
      - ![Image](https://github.com/user-attachments/assets/2c288d3b-e128-4239-9319-dc8fd48b87cf)
      - ![Image](https://github.com/user-attachments/assets/740b23e3-7858-489f-a5bd-994f7da7b479)
      - $o_i$는 old policy로 부터 나온 sample들 
     
### Ablations
- distiliation from deepseek-r1

![Image](https://github.com/user-attachments/assets/72dc4f63-6962-4d4a-bf62-d2a3f45e88ac)

   