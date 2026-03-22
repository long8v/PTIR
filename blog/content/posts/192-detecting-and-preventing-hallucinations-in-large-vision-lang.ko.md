---
title: "[173] Detecting and Preventing Hallucinations in Large Vision Language Models"
date: 2024-08-30
tags: ['AAAI', 'RL', '2023Q3', 'MLLM', 'ScaleAI']
paper: "https://arxiv.org/pdf/2308.06394"
issue: 192
issueUrl: "https://github.com/long8v/PTIR/issues/192"
---
<img width="643" alt="image" src="https://github.com/user-attachments/assets/48e5a2d4-4639-4ebe-bbf8-6eabdc0c5372">

[paper](https://arxiv.org/pdf/2308.06394)

## TL;DR
- **I read this because.. :** VLM + RLHF
- **task :** LVLM 
- **problem :** hallucination
- **idea :** human annotation을 segment level로 받아서 hallucination을 측정 + rejection sampling / DPO처럼 학습하자
- **input/output :** {image, question} -> class(accurate, inaccurate, analysis)
- **architecture :** InstructBLIP 
- **objective :** CE loss or proposed FDPO loss
- **baseline :** InstructBLIP, LLaVA, mPLUG-OWL
- **data :** (proposed) 16K image-prompt-response 
- **evaluation :** RM Score(true segment 대한 NLL), human eval(percent of content that was truthful? 문장단위인지..
- **result :** Reward model을 학습하고 rejection sampling 했을 때 성능 개선. 제안한 FDPO도 성능 개선. 
- **contribution :** 벤치마크 공개, VLM에 RLHF한 꽤 초기작인듯
- **etc. :** MHALDetect 벤치마크가 잘 되어서 그런지 인용수는 많은데 뭔가 잘 안 읽히넹.. 

## Details

아래와 같이 annotation
<img width="715" alt="image" src="https://github.com/user-attachments/assets/0489694d-ff20-42b6-9d6f-3d81c308a5f4">

4000 images - instructBLIP response (10 human annotated)
class는 accurate, inaccurate, analysis, unsure 4개 

이중 3200개를 val split  --> 이게 아마 MHALDetect

### Method
- Multi-Modal Reward Model
Instruct BLIP 사용. 각 sentence level의 eos token에 classifier (accurate, inaccurate, analysis) 달아서 학습하는 방식
segment-level reward model의 경우 각 segment(데이터 까보니까 다른 label이 나오기 까지 그냥 다 이어짐)의 끝에 classifier 달음. 이건 왜 한지 모르겠음..! 

- Rejection sampling 
제대로 된 설명이 없는데.. inference에서 sampling 있게 뽑은 뒤에 각 sentence level로 RM 모델에서 negative log likelihood 값을 가지고 hallucination이 있는지 없는지 판단해서 사용하는 듯
best-of-n, worst-of-n 으로 뽑음. 이때 n은 16, 64
<img width="710" alt="image" src="https://github.com/user-attachments/assets/84b4ba8b-2fe2-468a-b3fb-49eb4a934f76">

- fine-grained direct preference optimization 
DPO와 달리 이 경우 pair가 없어서 그냥 segment level로 loss를 부과

<img width="305" alt="image" src="https://github.com/user-attachments/assets/04293d45-8758-4f07-9b2c-2d0563cedb6a">

- $x$ : 현재 segment 이전까지의 토큰들
- $y$ : generated segment
- $c$ : class of current segment
  - 1 : preferred classs (correct)
  - 0 : dispreferred class (incorrect, optional하게 analysis도) 

### Result
- reward model의 성능 
<img width="439" alt="image" src="https://github.com/user-attachments/assets/9d7b260e-81c9-4d8b-9fa6-516f4415cbc8">

- rejection sampling / finegrained DPO result
<img width="703" alt="image" src="https://github.com/user-attachments/assets/304321ba-f445-4ed2-be86-0f0b3ba56377">

RM Score는 잘 와닿지 않음.. Human Eval에서 성능 개선.
다른 hallucination bench나 VLM 벤치는 찍어보지 않음.
