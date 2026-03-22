---
title: "[205] LLMs Can Easily Learn to Reason from Demonstrations Structure, not content, is what matters!"
date: 2025-02-28
tags: ['Berkley', 'reasoning', '2025Q1']
paper: "https://arxiv.org/abs/2502.07374"
issue: 226
issueUrl: "https://github.com/long8v/PTIR/issues/226"
---
<img width="897" alt="Image" src="https://github.com/user-attachments/assets/809785f6-1a4c-4e78-b90f-cb4a27cdbc9b" />

[paper](https://arxiv.org/abs/2502.07374), [code](https://github.com/NovaSky-AI/SkyThought)

## TL;DR
- **I read this because.. :** CoT의 내용이 중요한가 아니면 구조가 중요한가? 추천받아 aka SkyThought
- **task :** reasoning in LLM 
- **problem :** long CoT를 어떻게 학습할 것인가에 대한 ablation 
- **idea :** CoT에 대한 ablation 실험 해보자
- **input/output :** Q -> {reasoning(long CoT), A}
- **architecture :** Qwen2.5-32B-Instruct 
- **objective :** ce loss 
- **baseline :** Qwen2.5-32B-Instruct, QwQ
- **data :** proposed 17K samples (prompts from {AMC/AIME, Math, Olympiad subset from NuminaMATH, APPS, TACO} + distil from {DeepSeek-R1, QwQ-32B preview}  + R1-17K reasoning 
- **evaluation :** MATH-500, OlympiadBench, AIME-2024, AMC23, LiveCodeBench
- **result :** long CoT 내부의 correctness 여부보다 structure가 더 중요. 
- **contribution :** ablations

## Details
### thumbnail

<img width="730" alt="Image" src="https://github.com/user-attachments/assets/90827512-90cc-4823-88be-bd63c4618b34" />

contributions
- 17K 적은 sample로 lora tuning 해도 reasoning 능력이 발현이 된다는 것을 밝힘
- Long CoT의 구조가 중요하지 각각의 reasoning step의 정확도가 중요하지 않음
- model size, arch, dataset size, data generation model에 대한 다양한 ablation 을 진행했다

### Simple distilation is effective
- distilation data curation ->12k math / 5k coding
  - prompt : math -- {AMC/AIME, MATH, Olympiad, Numina-Math}  + code -- {APPS, TACO}
  - distill model : {DeepSeek-R1, QwQ-32B-Preview}
  - GPT-4o-mini로 difficulty prompt 구분 시킴 / ground truth solution validate
  - +) open R1-17K reasoning dataset (https://huggingface.co/datasets/bespokelabs/Bespoke-Stratos-17k) 
- training details
  - (code) llama-factory
  - (base model) Qwen2.5-32B-Instruct
  - lr 1e-5 / lora lr 1e-4

### Result
- small amount of data is enought
<img width="370" alt="Image" src="https://github.com/user-attachments/assets/7b615b4b-ea1c-4d11-91bd-7c0072fb75b1" />

16만으로도 충분한 성능.

- lora finetuning without performance degradation

<img width="377" alt="Image" src="https://github.com/user-attachments/assets/f34c27ef-1f09-46f9-8f74-9fe9afba0900" />

###  long cot: structure is key
- CoT를 local content / global structure 중 뭐가 더 중요한지를 ablation
- local content
  - 최종 정답, math derivation 내의 숫자, rasoning keywords
- global structure
  - reflection, self-validation, backtracking  
- setting: QwQ-32B-Preview를 사용 해서 4618개의 correct response 기준으로 ablation 

<img width="337" alt="Image" src="https://github.com/user-attachments/assets/2e1907b0-a487-4c07-b78e-5497901f74a8" />

### local content
- wrong answer sample
   - 3.2%p 정도 밖에 성능 저하가 없음
- digits corrupted samples 
  - 일부러 중간의 숫자를 random하게 corrupt    함. 
  - 70% 정도의 숫자를 corrupt해도 성능이 4.3% 밖에 안떨어짐.
  - 다 corrupt하는건 성능이 떨어짐
- reasoning keyword  removal
 - wait, let me think again, but 이런 단어들을 모두 제거해도 성능 3.3% 정도밖에 안떨어짐- 

### global structure
- Llama-3.3.-70-B-instruct 사용해서 reasoning step을 여러개로 나눔
- 이후 insert, delete, shuffle을 비율 만큼 진행함 
<img width="627" alt="Image" src="https://github.com/user-attachments/assets/5e31a0a5-fddb-4286-a4eb-bc25ed56769b" />

degradation이 엄청 심함. (자세히 안읽음)

## more ablations
-  long cot 학습이 non-reasoning task 성능 저하를 일으키는가? 
<img width="319" alt="Image" src="https://github.com/user-attachments/assets/32dbbb8d-dec5-45b0-8d03-d6f3a595892b" />

그렇지 않았고 오히려 성능이 오른다.

- student model에 대한 ablation
<img width="320" alt="Image" src="https://github.com/user-attachments/assets/4f02cd62-6cdd-4ff2-bdee-8a39f37ff560" />

Qwen2.5-32B-Instruct를 제외하고 올랐다. 얘는 왜 안되는지 잘 모르겠다.

- BoN과의 비교 

<img width="339" alt="Image" src="https://github.com/user-attachments/assets/31e7982d-9d93-498e-bc94-52799766ca1b" />

- comparsion to short cot finetuning 

<img width="352" alt="Image" src="https://github.com/user-attachments/assets/149c27b2-b576-4d86-8f2d-109133af1290" />

short cot 성능이 좋지 않았다