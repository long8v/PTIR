---
title: "[181] Step-DPO: Step-wise Preference Optimization for Long-chain Reasoning of LLMs"
date: 2024-10-07
tags: ['LLM', 'RL', '2023Q3']
paper: "https://arxiv.org/abs/2406.18629"
issue: 200
issueUrl: "https://github.com/long8v/PTIR/issues/200"
---
![image](https://github.com/user-attachments/assets/92c31320-5086-4e26-84fb-99ea0e73cf89)

[paper](https://arxiv.org/abs/2406.18629), [code/data](https://github.com/dvlab-research/Step-DPO)

## TL;DR
- **I read this because.. :** 언급되어. step을 어떻게 나눈다는건지 궁금해서 읽음. 
- **task :** LLM in reasoning
- **problem :** DPO가 널리 쓰이고 있으나 long-context에서 성능 향상은 제한됨 
- **idea :** 긴 reasoning이 있는 경우 틀린 step에 대해서 win / lose step을 최대화하는 DPO loss 
- **architecture :** Qwen2, Qwen1.5 Meta-Llama-3-70B, deepseek-math-7b-base
- **objective :** step-DPO (proposed)
- **baseline :** SFT, DPO
- **data :** 처음으로 틀린 step이 저장되어 있는 374K pair 데이터(proposed), AQuA
- **evaluation :** MATH, GSM8K, AIME, Odyssey-MATH
- **result :** DPO보다 나은 성능. GPT-4-1106, Claude-3-Opus, Gemini-1.5-Pro를 이겼다고 함. 
- **contribution :** data 공개. 이런 류가 많은것 같은데 이게 처음인지는 모르겠음
- **etc. :** 

## Details
### Performance
![image](https://github.com/user-attachments/assets/bfe19b44-26f1-4a60-950b-662af2d2534b)

### motivation
이 논문에서 말하는 SFT의 단점은 desirable output 뿐 아니라 undesirable output에 대한 likelihood도 높인다는 점임 -> prone to hallucination
이를 해결하기 위해 undesriable supervision을 주는게 RLHF인데 DPO의 경우 long sequence output에 대해 효과가 좋지 않다고 함. (finegrained process supervision이 없어서라고 표현)

![image](https://github.com/user-attachments/assets/faf6a212-4956-42eb-8d29-3a3df42cad71)

### Step-DPO
![image](https://github.com/user-attachments/assets/49593a57-00f7-4e12-9e8d-82af8a19ce4e)

전체 시퀀스가 아니라 틀린 step에 대해서 win -- lose margin을 최대화하도록 
![image](https://github.com/user-attachments/assets/683ac8cb-3901-46e0-a5fa-cbbe3e9aeeac)

- $s_i$ : i번째 reasoning step
- $x$ : prompt
- $k$ : 최초로 틀린 step

### In-distribtuion data construction
아래와 같이 만드는게 목표
![image](https://github.com/user-attachments/assets/77d6c95f-1add-4787-8e9f-6adeae7edd2c)

파이프라인
![image](https://github.com/user-attachments/assets/543b407f-9e67-4749-aa6e-a35167ee889f)

- error collection 
problems x 와 gt answer $\hat{y}$를 모음.
reference model $\pi_{ref}$를 가지고 step-wise CoT preifx로 실행해서 step으로 나눔 
final answer y가 gt answer가 다른 것들을 모음.

- step localization
reasoning step $y=s_1, s_2, ... , s_n$에서 처음으로 틀린 $k$를 찾음. (manually or gpt-4를 통해)
틀린 step k의 에러를 $s_{lose}$로 선정

- rectification
맞는 ressoning step $s_{1~{k-1}}$을 주어주고 여러번 reference model에 infer해서 여러개 구함 
![image](https://github.com/user-attachments/assets/4a20ae72-9236-43ca-8591-2197bb1a4766)

이중에 final answer가 gt와 맞는 걸 $s_{win}$으로 선정함. 
이때 정답이 맞더라도 과정이 틀릴 수 있는데 이는 manually or gpt-4로 정제함 (그림에서는 생략되어 있음)

### Result
- 전체 374K를 모았고, 이중 299K가 SFT 데이터로 쓰였고 나머지 75K는 Step-DPO로 쓰임
  - SFT는 3 or 2 에폭
  - Step-DPO는 8 or 4 에폭 돌림 
- SFT dataset에 추가적으로 AQuA 데이터 셋 사용함 

![image](https://github.com/user-attachments/assets/2bc68a78-0ea1-4877-b034-19453b43c5cd)

![image](https://github.com/user-attachments/assets/60c5c28c-54df-4b4e-91df-af783cc9e7a2)

### Ablation
- DPO vs Step-DPO
![image](https://github.com/user-attachments/assets/ae42e31b-821c-44c5-9426-79eb0f34d012)

- in-distribution vs out-distribution
![image](https://github.com/user-attachments/assets/2a028e47-4231-4551-a21d-094155dc7c97)

사용하는 데이터가 우리가 학습한 모델의 inference 결과인게 중요하다고 함 