---
title: "[211] Skywork R1V: Pioneering Multimodal Reasoning with Chain-of-Thought"
date: 2025-07-02
tags: ['MLLM', 'reasoning', '2025Q2']
paper: "https://arxiv.org/abs/2504.05599"
issue: 232
issueUrl: "https://github.com/long8v/PTIR/issues/232"
---
<img width="749" alt="Image" src="https://github.com/user-attachments/assets/0963a01b-a184-47ba-821c-bf0b1be94550" />

[paper](https://arxiv.org/abs/2504.05599)

## TL;DR
* **I read this because.. :** AIME 성능을 레포트한 LVLM
* **task :** multimodal reasoning (math, vision, QA)
* **problem :** VLM은 complex reasoning에 약하고, vision-text alignment도 어려움
* **idea :** MLP-based adapter + hybrid SFT+GRPO + adaptive-length CoT distillation
* **input/output :** {image, prompt} -> {step-by-step reasoning, boxed answer}
* **architecture :** DeepSeek-R1-distill-Qwen2.5-32B (frozen), InternViT-6B-448px-V2_5 (frozen), MLP Adapter
* **objective :** SFT, GRPO 
* **baseline :** GPT-4o, Claude 3.5, Kimi k1.5, InternVL2.5, QwenVL 
* **data :** 2M VL data → 200K (GPT-4 filtered) → 40K CoT (AL-CoTD) -> prompt
* **evaluation :** MATH500, AIME24, GPQA, MathVista, MMMU
* **result :** MATH500 94.0 / AIME24 72.0 / MMMU 69.0 등 competitive 성능
* **contribution :** reasoning LLM을 vision으로 효율적으로 확장, RL로 성능 향상
* **etc. :** MLP만 학습한게 특이하고 신기하지만 AIME 성능을 report한게 괘씸(?)함. 여기선 llm frozen을 잘 명시해놨는데 V2에선 애매해게 서술해놔서 더 괘씸함

## Details
thumbnail

![Image](https://github.com/user-attachments/assets/717f9215-0c8c-4bcb-80eb-7ee75d73bc93)

- 이 논문의 가장 특이점은 MLP만 학습한다는 것임. 이때 MLP를 학습 시키는 방식에 공을 들임
  - 1) MLP adapter를 처음 initialize할 때는 reasoning lanugage model 대신 그냥 language model을 사용함 (Qwen2.5-32B-Instruct)
    - 2M full dataset으로 finetune
  - 2) 이 단계에서 language model을 DeepSeek-R1-distill-Qwen2.5-32B 로 교체. tokenizer와 parameter가 다르지만(왜 다르지??) 원래 성능을 잘 복원한다고 함
    - GPT-4로 평가된 high-quality 의 200K 사용
  - 3) 40K의 high-quality CoT 데이터로 학습 (Adaptive-Length Chain-of-Thought Distilation 사용)
  - 각 1 epoch씩 lr은 2e-4 -> 4e-5 -> 4e-5   
-  Hybrid Optimization Framework
  - <img width="973" alt="Image" src="https://github.com/user-attachments/assets/ba953ba0-e548-466f-adef-31fcbfb7882a" />
  - stage 1: filtering 없이 모든 데이터셋으로 학습
  - stage 2: reward model이 점수를 매긴것으로 filtering하고 이전 stage의 모델이 풀지 못한 걸 교집합을 구해서 데이터로 사용 (
    - 2,3,4,5로 높였다고 함.
    - context length 16K 
  - stage 3: GRPO, reward=5, generation bs 8, temperature 1, lr 1e-6, max completion length 8k
    

### Adaptive-Length Chain-of-Thought Distilation

<img width="980" alt="Image" src="https://github.com/user-attachments/assets/b1075286-6303-4d03-a8b4-57ac9312fe13" />

- QDAM:
  - vision score: image clarity, image necessity (질답을 위해 이미지가 필요한가)
  - text score: GPT-4o 를 사용해서 question quality, difficulty level, reasoning demand 등을 평가하게 함 
- VTIA
  - why, how 등 scientific reasoning이 필요한지를 평가하게 함 
- 두개를 결합해서 이 쿼리가 얼마나 긴 대답이 필요한지를 P로 추산하고 P가 낮으면 더 높은 repetition penalty를 사용하여 새엇ㅇ하게 함. 
- 최종적으로는 GPT4o가 정답이 맞는지 평가하게 하고, 틀리다면 GPT4or가 다시 생성하게 함. 


### performance

<img width="957" alt="Image" src="https://github.com/user-attachments/assets/db411526-cc24-4f63-a699-70c5d04d7515" />

### ablation

![Image](https://github.com/user-attachments/assets/47287793-99a7-4017-aef4-f3f956a01de3)