---
title: "[206] Vision-R1: Incentivizing Reasoning Capability in Multimodal Large Language Models"
date: 2025-03-12
tags: ['25min', 'RL', 'MLLM', '2025Q1']
paper: "https://arxiv.org/abs/2503.06749"
issue: 227
issueUrl: "https://github.com/long8v/PTIR/issues/227"
---
![Image](https://github.com/user-attachments/assets/896f4fbc-aa8b-4a17-b6d5-fd974859d0f0)

[paper](https://arxiv.org/abs/2503.06749)

## TL;DR
- **I read this because.. :** mllm + o1
- **task :** VLM reasoning 
- **problem :** r1 처럼 학습하고 싶은데 vision data 가 없네
- **idea :** MLLM으로 cot 먼저 생성하고 이걸로 description 생성한 뒤 r1에게 주고 long cot 생성하게 함.
- **input/output :** {I, Q} -> {long CoT, A}
- **architecture :** Qwen2.5-VL-7B-Instruct, Llmama-3.2-V-Instruct
- **objective :** CE loss -> GRPO loss 
- **baseline :** Qwen2.5-VL-7B-Instruct, Llmama-3.2-V-Instruct, Math MLLM, LLaVA-CoT-11B, Mulberry-7B
- **data :** cold start {LLaVA-CoT, Mulberry} image / answer -- 200K -> GRPO {WeMath, PolyMATH, MathiVision, SceMQA, Geomety3K} -- 10K
- **evaluation :** MM-Math, MathVista, MathVerse
- **result :** instruct 모델보다 상당히 개선된 모습 
- **contribution :** 그냥 디테일 캡션 생성해라 보다 prompt로 cot 생성하고 사용하는게 합리적인듯. 데이터도 공개했으면 좋겠다. 
- **etc. :** bench 셋을 데이터셋으로 씀 

## Details
- thumbnail

<img width="683" alt="Image" src="https://github.com/user-attachments/assets/ae33b730-ba98-47d1-b54e-05c0fd48dd1b" />

MLLM -- Qwen-VL2.5-72B
LLM -- R1 


<img width="319" alt="Image" src="https://github.com/user-attachments/assets/1ed829c6-4ac6-4eb8-9acd-f7304c382f81" />

<img width="306" alt="Image" src="https://github.com/user-attachments/assets/b49e6a17-8dbb-471e-851f-db39244263b9" />

<img width="332" alt="Image" src="https://github.com/user-attachments/assets/976f53d6-9afc-4e65-ac08-2e98f5f86426" />

- data distil

<img width="678" alt="Image" src="https://github.com/user-attachments/assets/df5314d9-3a67-4f4e-ab35-7edb22871dc4" />

- data ablation

<img width="690" alt="Image" src="https://github.com/user-attachments/assets/435ef4d0-7cf7-4f9c-a08f-381f27e9aa2d" />

- progressive 

<img width="683" alt="Image" src="https://github.com/user-attachments/assets/0756c302-8f96-441b-8e57-b27640d02212" />

<img width="340" alt="Image" src="https://github.com/user-attachments/assets/1ee5c2ef-617a-4574-8516-9e2deec26640" />

- main result 

<img width="685" alt="Image" src="https://github.com/user-attachments/assets/a227d111-9d4f-499d-88a9-069d96b05e61" />

- qualitative example 

<img width="696" alt="Image" src="https://github.com/user-attachments/assets/3ddca4f5-fac8-4135-baa6-12d44731686a" />