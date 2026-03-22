---
title: "[155] Revisiting Text-to-Image Evaluation with Gecko: On Metrics, Prompts, and Human Ratings"
date: 2024-05-03
tags: ['google', 'evaluation', 'generation', '2024Q2']
paper: "https://arxiv.org/pdf/2404.16820"
issue: 171
issueUrl: "https://github.com/long8v/PTIR/issues/171"
---

<img width="660" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4f0a737d-6668-4dda-9281-b0c1666af9f1">

[paper](https://arxiv.org/pdf/2404.16820), [code](https://github.com/google-deepmind/gecko_benchmark_t2i)

## TL;DR
- **I read this because.. :** T2I evaluation이고 word-level 어쩌구가 있길래 읽음. 
- **task :** T2I evaluation
- **problem :** 기존 DSG, QG2 방법론은 LLM의 hallucination 발생. skill 동작 방식을 바꿈. 
- **idea :** skill을 부르는 방식을 조금 다르게 함. 
- **input/output :** {image, text} -> score 
- **architecture :** PALM (QA) + PALI (VQA)  
- **baseline :** METEOR, SPICE, CLIP, TIFA, DSG
- **data :** proposed Gecko2k
- **evaluation :** proposed Gecko
- **result :** 다른 metric보다 human correlation이 높음. 
- **contribution :** 데이터 제안. word-level annotation. 
- **etc. :** 나름 열심히 읽었는데 word-level annotation을 받고 나서 어떻게 한지 모르겠네. 그냥 likert(절대 점수) annotation보다 좋았다는건가? 

## Details

### problems in DSG 

<img width="685" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1dce9e46-d2f7-4e91-8f65-050eebe25171">

<img width="652" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/489d0c1d-21f1-4a56-ba5e-8048684e9b1a">

### proposed 
<img width="869" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ff7fb2a9-ae8f-414c-9722-279460a2e59c">

### result
<img width="662" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/241b0f5d-2729-436d-8ae9-5b06b22fe20b">

여기서 CLIP에 WL을 어떻게 쟀는지가 너무 궁금해서 논문을 읽었는데.. metric을 Spearman으로 된걸 보니까 
word-level annoation을 한 뒤에 이걸로 점수 평균같은걸 매겨서 {image, caption}의 score를 매긴 다음에 그냥 이게 human의 선호와 얼마나 같은지를 본듯 했다. 

### word-level annotation 
<img width="677" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3bc0dff0-3a7e-4320-bbc1-860fc7b5e76a">

<img width="677" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4be56ae2-dda6-47f2-8124-5c0dbbd7df9d">

### 다양한 CLIP 모델에 대한 성능 평가
<img width="671" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e5e99846-70a0-4514-b935-eee569c39803">

SigLIP이 좋긴 하네
같은 모델의 경우 데이터 본 경우가 더 좋았음
모든 경우는 아니지만 larger model일 수록 좋긴 했음. 

pyramid CLIP의 경우 아래와 같이 생김 
<img width="549" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0be17af5-15ca-4952-ab9e-027c83a2b600">


