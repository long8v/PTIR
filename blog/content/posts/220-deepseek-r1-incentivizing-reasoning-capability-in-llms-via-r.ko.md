---
title: "[199] DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning"
date: 2025-01-24
tags: ['RL', 'reasoning', '2025Q1']
paper: "https://github.com/deepseek-ai/DeepSeek-R1/blob/main/DeepSeek_R1.pdf"
issue: 220
issueUrl: "https://github.com/long8v/PTIR/issues/220"
---
<img width="685" alt="Image" src="https://github.com/user-attachments/assets/f4892d73-8ddb-4bb5-b024-658763afe32f" />

[paper](https://github.com/deepseek-ai/DeepSeek-R1/blob/main/DeepSeek_R1.pdf)

## TL;DR
- **I read this because.. :** deepseek r1으로 세상이 난리라서 
- **task :** reasoning in LLM
- **problem :** MCTS, PRM, ORM 방법론들이 o1 성능을 따라잡지 못함
- **idea :** 대규모 RL을 하자.
- **architecture :** DeepSeek-R1-Zero
- **objective :** GRPO를 advantage로 사용한 PPO..? GRPO가 objective자체인지 trick인지 헷갈리네 
- **baseline :** OpenAI o1, OpenAI o1-mini, Deepseek-v3
- **data :** (rl) verifable prompts? (cold start sft) thousand of answer from DeepSeek-v3 CoT prompt  (sft) deepseek-v3에서 사용된 QA, prompt + rejection sampling (distil) 
- **evaluation :** AIME, Codeforces, GPQA diamond, MATH-500, MMLU, SWE-bench 
- **result :** o1을 개선 
- **contribution :** 아마 o1을 이긴 최초의 오픈 모델인듯?

## Details
- benchmark thumbnail

<img width="657" alt="Image" src="https://github.com/user-attachments/assets/ab77fb90-e8fa-4e07-935f-570bf04ce3e9" />

### DeepSeek-R1-Zero
- SFT 데이터 전혀 없이 넣은 버전 

- GRPO
<img width="831" alt="Image" src="https://github.com/user-attachments/assets/bd03cbf2-c34e-4044-8f3e-bf3b9c738355" />

- RM
- accuracy rewards: final answer in sepcific format. leetcode problem. compiler 
- format rewards: thinking process를 `<think>`, `</think>` 태그 사이에 넣기

- Training template

<img width="856" alt="Image" src="https://github.com/user-attachments/assets/cfb359a2-075f-45db-92dc-66573d96543d" />

- performance 
RL 만으로도 점진적인 성능 개선. 

<img width="867" alt="Image" src="https://github.com/user-attachments/assets/5403d197-2ca5-4a3b-9148-13138706df75" />

그리고 학습을 진행하면서 reflection (revisit or reevaluate)이 늘어나면서 sequence length가 늘어나는 현상

<img width="820" alt="Image" src="https://github.com/user-attachments/assets/d7f245b4-3516-42ab-a586-8d5b01a69482" />

흥미로운 건 'aha moment'인데, 학습을 진행하다가 갑자기 모델이 aha moment가 있다면서 초기 접근 방법을 바꾸는 현상이 관찰되었음 

<img width="796" alt="Image" src="https://github.com/user-attachments/assets/76798acf-7e14-4de3-8ad6-adc1d1ed49fb" />

rl을 했더니 알아서 reflection을 했다는게 재밌는 포인트

- drawback
language mixing, poor readability.

### DeepSeek-R1: rl with cold start 
few shot long CoT prompt, Deepseek-r1-zero + human annotator postprocessing, directly prompting to generate detailed answer with reflection and verification.
readability와 성능상 개선이 목적 

- reasoning oriented rl
  - coding, math, science, logical thinking에 집중
  - language consistency reward를 추가
- rejection sampling and supervised finetuning
  - reasoning RL 이후 학습된 모델을 가지고 SFT 데이터를 만듦. 이때는 reasoning에만 국한된건 아니고 writing, role-playing, general-purpose 테스크에 맞게 했다고 함 
  - reasoning sft data : 
    - deepseek-v3 judgemnet로 generative reward 로 평가 
    - lanauage mix, chaotic한 cot는 필터로 지웠다고  
  - non-reasoning data:
    - deepseek-v3 sft data를 사용하고, deepseek-v3-base로 cot를 만들고, cot가 필요없는건 필터링 cot 없게 만들어서 200K training data를 만들었다고 . 
  - secondary rl
    - reasoning을 위해서는 rule based reward / general data는 RM(helpful, harmless 등)을 사용했다고 함

### Distilation 
Qwen, Llama를 DeepSeek-R1의 CoT 데이터 800K를 가지고 distil 해서 사용했다고 함. RL은 사용하지 않았음.

### Performance

<img width="835" alt="Image" src="https://github.com/user-attachments/assets/67e1c69b-9899-4438-abce-ecb41855aec7" />

distil models

<img width="820" alt="Image" src="https://github.com/user-attachments/assets/0dcca1d1-4f88-426a-88fe-3ae887048e06" />

### discussion
- rl vs distil
<img width="843" alt="Image" src="https://github.com/user-attachments/assets/199a92aa-2c34-4613-9e7d-c618f0dccded" />

distil하는게 더 성능이 좋음 

- unsuccessful attempts 
  - PRM: 자동으로 process label을 얻는건 noisy하고 human이 하면 scale up이 어렵고. reward hacking될 여지도 큼 
  - MCTS: 너무 search space가 크고 local optimum에 빠질 위험이 큼