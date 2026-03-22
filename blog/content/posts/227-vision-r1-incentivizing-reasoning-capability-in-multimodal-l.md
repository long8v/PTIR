---
title: "[206] Vision-R1: Incentivizing Reasoning Capability in Multimodal Large Language Models"
date: 2025-03-12
tags: ['25min', 'RL', 'MLLM', '2025Q1']
paper: "https://arxiv.org/abs/2503.06749"
issue: 227
issueUrl: "https://github.com/long8v/PTIR/issues/227"
summary: "MLLM + O1 - Seems reasonable to create and use COT as prompt rather than just generate detail caption. I'd like to see the data published as well."
---
![Image](https://github.com/user-attachments/assets/896f4fbc-aa8b-4a17-b6d5-fd974859d0f0)

[paper](https://arxiv.org/abs/2503.06749)

## TL;DR
- **I read this because.. :** mllm + o1
- **task :** VLM reasoning 
- **problem :** I want to train like r1, but I don't have vision data.
- **idea :** Create cot first with MLLM, create description with it, give it to r1 and let him create long cot.
- **input/output :** {I, Q} -> {long CoT, A}
- **architecture :** Qwen2.5-VL-7B-Instruct, Llmama-3.2-V-Instruct
- **objective :** CE loss -> GRPO loss 
- **baseline :** Qwen2.5-VL-7B-Instruct, Llmama-3.2-V-Instruct, Math MLLM, LLaVA-CoT-11B, Mulberry-7B
- **data :** cold start {LLaVA-CoT, Mulberry} image / answer -- 200K -> GRPO {WeMath, PolyMATH, MathiVision, SceMQA, Geomety3K} -- 10K
- **evaluation :** MM-Math, MathVista, MathVerse
- **Result :** Significant improvement over the instruct model
- **contribution :** Seems reasonable to create and use cot as prompt rather than just generate detail caption. I'd like to see the data published as well.
- **etc. :** Write the bench set as a dataset

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