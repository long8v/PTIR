---
title: "[211] Skywork R1V: Pioneering Multimodal Reasoning with Chain-of-Thought"
date: 2025-07-02
tags: ['MLLM', 'reasoning', '2025Q2']
paper: "https://arxiv.org/abs/2504.05599"
issue: 232
issueUrl: "https://github.com/long8v/PTIR/issues/232"
summary: "LVLM reporting AIME performance - Efficiently extending the reasoning LLM to vision, improving performance with RL"
---
<img width="749" alt="Image" src="https://github.com/user-attachments/assets/0963a01b-a184-47ba-821c-bf0b1be94550" />

[paper](https://arxiv.org/abs/2504.05599)

## TL;DR
* **I read this because.. :** LVLM reporting AIME performance
* **task :** multimodal reasoning (math, vision, QA)
* **problem :** VLM is weak for complex reasoning, and vision-text alignment is difficult.
* **idea :** MLP-based adapter + hybrid SFT+GRPO + adaptive-length CoT distillation
* **input/output :** {image, prompt} -> {step-by-step reasoning, boxed answer}
* **architecture :** DeepSeek-R1-distill-Qwen2.5-32B (frozen), InternViT-6B-448px-V2_5 (frozen), MLP Adapter
* **objective :** SFT, GRPO 
* **baseline :** GPT-4o, Claude 3.5, Kimi k1.5, InternVL2.5, QwenVL 
* **data :** 2M VL data → 200K (GPT-4 filtered) → 40K CoT (AL-CoTD) -> prompt
* **evaluation :** MATH500, AIME24, GPQA, MathVista, MMMU
* **result :** MATH500 94.0 / AIME24 72.0 / MMMU 69.0, etc. competitive performance
* **contribution :** Efficiently extend reasoning LLM to vision, improve performance with RL
* **etc. :** It's unusual and interesting to learn only MLP, but it's annoying(?) to report AIME performance. Here, llm frozen is well specified, but in V2, it is more annoying because it is vague.

## Details
thumbnail

![Image](https://github.com/user-attachments/assets/717f9215-0c8c-4bcb-80eb-7ee75d73bc93)

- The most unusual aspect of this paper is that it only trains MLPs. The way it trains the MLPs is very specific
- 1) When initializing MLP adapter for the first time, just use language model instead of reasoning lanugage model (Qwen2.5-32B-Instruct)
- Finetune with 2M full dataset
- 2) Replace language model with DeepSeek-R1-distill-Qwen2.5-32B at this stage, which has different tokenizer and parameter (why is it different??) but reportedly restores original performance well
- 200K of high-quality, GPT-4-rated usage
- 3) Train on 40K of high-quality CoT data (using Adaptive-Length Chain-of-Thought Distillation)
- For each 1 epoch, lr goes from 2e-4 -> 4e-5 -> 4e-5
-  Hybrid Optimization Framework
  - <img width="973" alt="Image" src="https://github.com/user-attachments/assets/ba953ba0-e548-466f-adef-31fcbfb7882a" />
- stage 1: train with all datasets without filtering
- stage 2: filter by what the reward model scored and find the intersection of what the model in the previous stage couldn't solve and use it as data (
- 2,3,4,5.
    - context length 16K 
  - stage 3: GRPO, reward=5, generation bs 8, temperature 1, lr 1e-6, max completion length 8k
    

### Adaptive-Length Chain-of-Thought Distilation

<img width="980" alt="Image" src="https://github.com/user-attachments/assets/b1075286-6303-4d03-a8b4-57ac9312fe13" />

- QDAM:
- vision score: image clarity, image necessity (do I need the image to answer the question)
- text score: Use GPT-4o to assess question quality, difficulty level, reasoning demand, etc.
- VTIA
- Have students evaluate the need for scientific reasoning, such as why and how
- Combine the two to estimate how long this query needs to be answered, P, and if P is low, use a higher repetition penalty to refresh it.
- Finally, let GPT4o evaluate if the answer is correct, and if not, let GPT4or regenerate it.


### performance

<img width="957" alt="Image" src="https://github.com/user-attachments/assets/db411526-cc24-4f63-a699-70c5d04d7515" />

### ablation

![Image](https://github.com/user-attachments/assets/47287793-99a7-4017-aef4-f3f956a01de3)