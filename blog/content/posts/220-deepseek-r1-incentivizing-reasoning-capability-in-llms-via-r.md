---
title: "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning"
date: 2025-01-24
tags: ['RL', 'reasoning', '2025Q1']
paper: "https://github.com/deepseek-ai/DeepSeek-R1/blob/main/DeepSeek_R1.pdf"
issue: 220
issueUrl: "https://github.com/long8v/PTIR/issues/220"
summary: "The world is going crazy with deepseek r1 - probably the first open model to beat o1?"
---
<img width="685" alt="Image" src="https://github.com/user-attachments/assets/f4892d73-8ddb-4bb5-b024-658763afe32f" />

[paper](https://github.com/deepseek-ai/DeepSeek-R1/blob/main/DeepSeek_R1.pdf)

## TL;DR
- **I read this because.. :** because the world is going crazy with deepseek r1
- **task :** reasoning in LLM
- **problem :** MCTS, PRM, ORM methodologies can't keep up with o1 performance
- **idea :** Let's do a big RL.
- **architecture :** DeepSeek-R1-Zero
- PPO with **objective :** GRPO as an advantage...? I'm confused if GRPO is the objective itself or the trick.
- **baseline :** OpenAI o1, OpenAI o1-mini, Deepseek-v3
- **data :** (rl) verifiable prompts? (cold start sft) thousand of answer from DeepSeek-v3 CoT prompt (sft) QA used in deepseek-v3, prompt + rejection sampling (distil)
- **evaluation :** AIME, Codeforces, GPQA diamond, MATH-500, MMLU, SWE-bench 
- **Result :** Improved o1
- **contribution :** Probably the first open model to beat O1?

## Details
- benchmark thumbnail

<img width="657" alt="Image" src="https://github.com/user-attachments/assets/ab77fb90-e8fa-4e07-935f-570bf04ce3e9" />

### DeepSeek-R1-Zero
- Version with no SFT data at all

- GRPO
<img width="831" alt="Image" src="https://github.com/user-attachments/assets/bd03cbf2-c34e-4044-8f3e-bf3b9c738355" />

- RM
- accuracy rewards: final answer in sepcific format. leetcode problem. compiler 
- format rewards: putting thinking process between `<think>`, `</think>` tags

- Training template

<img width="856" alt="Image" src="https://github.com/user-attachments/assets/cfb359a2-075f-45db-92dc-66573d96543d" />

- performance 
Incremental performance improvements with RL alone.

<img width="867" alt="Image" src="https://github.com/user-attachments/assets/5403d197-2ca5-4a3b-9148-13138706df75" />

And as learning progresses, the sequence length increases as reflection (revisit or reevaluate) increases.

<img width="820" alt="Image" src="https://github.com/user-attachments/assets/d7f245b4-3516-42ab-a586-8d5b01a69482" />

An interesting one is the "aha moment," where a model suddenly has an aha moment during training and changes its initial approach.

<img width="796" alt="Image" src="https://github.com/user-attachments/assets/76798acf-7e14-4de3-8ad6-adc1d1ed49fb" />

Funny point that I did RL and it did reflection on its own

- drawback
language mixing, poor readability.

### DeepSeek-R1: rl with cold start 
few shot long CoT prompt, Deepseek-r1-zero + human annotator postprocessing, directly prompting to generate detailed answer with reflection and verification.
Aim for readability and performance improvements

- reasoning oriented rl
- Focus on coding, math, science, and logical thinking
- Add language consistency reward
- rejection sampling and supervised finetuning
- Create SFT data with the trained model after the reasoning RL. This is not limited to reasoning, but it is said to be adapted to writing, role-playing, and general-purpose tasks.
  - reasoning sft data : 
- Evaluate with generative reward with deepseek-v3 judgemnet
- lanauage mix, chaotic cot cleared by filter
  - non-reasoning data:
- I created 200K training data by using deepseek-v3 sft data, creating cot with deepseek-v3-base, and filtering cot for the ones that don't need cot.
  - secondary rl
- For reasoning, rule based reward / general data is referred to as using RM (helpful, harmless, etc.)

### Distilation 
Qwen, Llama was used by distil with 800K CoT data from DeepSeek-R1. RL was not used.

### Performance

<img width="835" alt="Image" src="https://github.com/user-attachments/assets/67e1c69b-9899-4438-abce-ecb41855aec7" />

distil models

<img width="820" alt="Image" src="https://github.com/user-attachments/assets/0dcca1d1-4f88-426a-88fe-3ae887048e06" />

### discussion
- rl vs distil
<img width="843" alt="Image" src="https://github.com/user-attachments/assets/199a92aa-2c34-4613-9e7d-c618f0dccded" />

distil performs better

- unsuccessful attempts 
- PRM: Automatically getting process labels is noisy, hard to scale up if done by humans, and open to reward hacking.
- MCTS: Too large a search space and risk of falling into local optima