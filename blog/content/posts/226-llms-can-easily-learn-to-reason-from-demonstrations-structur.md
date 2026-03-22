---
title: "[205] LLMs Can Easily Learn to Reason from Demonstrations Structure, not content, is what matters!"
date: 2025-02-28
tags: ['Berkley', 'reasoning', '2025Q1']
paper: "https://arxiv.org/abs/2502.07374"
issue: 226
issueUrl: "https://github.com/long8v/PTIR/issues/226"
summary: "Is it the content or the structure of the CoT that matters? Featured aka SkyThought - ablations"
---
<img width="897" alt="Image" src="https://github.com/user-attachments/assets/809785f6-1a4c-4e78-b90f-cb4a27cdbc9b" />

[paper](https://arxiv.org/abs/2502.07374), [code](https://github.com/NovaSky-AI/SkyThought)

## TL;DR
- **I read this because.. :** Is it the content or the structure of CoT that matters? Recommended by aka SkyThought
- **task :** reasoning in LLM 
- **problem :** ablation on how to learn a long CoT
- Idea:** Experiment with ablation for CoTs
- **input/output :** Q -> {reasoning(long CoT), A}
- **architecture :** Qwen2.5-32B-Instruct 
- **objective :** ce loss 
- **baseline :** Qwen2.5-32B-Instruct, QwQ
- **data :** proposed 17K samples (prompts from {AMC/AIME, Math, Olympiad subset from NuminaMATH, APPS, TACO} + distil from {DeepSeek-R1, QwQ-32B preview}  + R1-17K reasoning 
- **evaluation :** MATH-500, OlympiadBench, AIME-2024, AMC23, LiveCodeBench
- **result :** long Structure is more important than correctness inside CoT.
- **contribution :** ablations

## Details
### thumbnail

<img width="730" alt="Image" src="https://github.com/user-attachments/assets/90827512-90cc-4823-88be-bd63c4618b34" />

contributions
- Reveals that tuning lora with 17K fewer samples can result in reasoning capabilities
- The structure of the Long CoT doesn't matter The accuracy of each reasoning step doesn't matter
- Performed various ablations for model size, arch, dataset size, and data generation model

### Simple distilation is effective
- distilation data curation ->12k math / 5k coding
  - prompt : math -- {AMC/AIME, MATH, Olympiad, Numina-Math}  + code -- {APPS, TACO}
  - distill model : {DeepSeek-R1, QwQ-32B-Preview}
- GPT-4o-mini to differentiate difficulty prompt / ground truth solution validate
  - +) open R1-17K reasoning dataset (https://huggingface.co/datasets/bespokelabs/Bespoke-Stratos-17k) 
- training details
  - (code) llama-factory
  - (base model) Qwen2.5-32B-Instruct
  - lr 1e-5 / lora lr 1e-4

### Result
- small amount of data is enought
<img width="370" alt="Image" src="https://github.com/user-attachments/assets/7b615b4b-ea1c-4d11-91bd-7c0072fb75b1" />

16 is more than enough performance.

- lora finetuning without performance degradation

<img width="377" alt="Image" src="https://github.com/user-attachments/assets/f34c27ef-1f09-46f9-8f74-9fe9afba0900" />

###  long cot: structure is key
- Ablation of CoTs to local content / global structure
- local content
- Final answer, numbers within the math derivation, reasoning keywords
- global structure
  - reflection, self-validation, backtracking  
- setting: Ablation using QwQ-32B-Preview with 4618 correct responses as the criterion

<img width="337" alt="Image" src="https://github.com/user-attachments/assets/2e1907b0-a487-4c07-b78e-5497901f74a8" />

### local content
- wrong answer sample
- Only 3.2 percentage points of performance degradation
- digits corrupted samples 
- Intentionally randomly corrupted the numbers in the middle.
- Corrupting 70% of the numbers only degrades performance by 4.3%.
- Corrupting everything is bad for performance
- reasoning keyword  removal


### global structure
- Using Llama-3.3.-70-B-instruct to split a reasoning step into several
- Then insert, delete, and shuffle by a percentage
<img width="627" alt="Image" src="https://github.com/user-attachments/assets/5e31a0a5-fddb-4286-a4eb-bc25ed56769b" />

The degradation is really bad. (Read more)

## more ablations
- does long cot learning cause non-reasoning task performance degradation?
<img width="319" alt="Image" src="https://github.com/user-attachments/assets/32dbbb8d-dec5-45b0-8d03-d6f3a595892b" />

It didn't, and performance actually went up.

- ablation for student model
<img width="320" alt="Image" src="https://github.com/user-attachments/assets/4f02cd62-6cdd-4ff2-bdee-8a39f37ff560" />

It went up except for Qwen2.5-32B-Instruct. I'm not sure why this one doesn't.

- Comparison with BoN

<img width="339" alt="Image" src="https://github.com/user-attachments/assets/31e7982d-9d93-498e-bc94-52799766ca1b" />

- comparsion to short cot finetuning 

<img width="352" alt="Image" src="https://github.com/user-attachments/assets/149c27b2-b576-4d86-8f2d-109133af1290" />

short cot performance was poor