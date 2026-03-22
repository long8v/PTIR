---
title: "[117] Multimodal Chain-of-Thought Reasoning in Language Models"
date: 2023-06-07
tags: ['multimodal', '2023Q1']
paper: "https://arxiv.org/abs/2302.00923"
issue: 126
issueUrl: "https://github.com/long8v/PTIR/issues/126"
---
<img width="1383" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d0810875-33b6-4243-95ee-1fe52d61f84e">

[paper](https://arxiv.org/abs/2302.00923)

## TL;DR
- **I read this because.. :** flamingo에서 demonstration 주는 것 보고 multi-modal에서 Infer단계에서 할 수 있는 trick은 뭐가 있나 하고 봄
- **task :** chain-of-thought
- **problem :** 100B 이상의 파라미터를 가진 애들만 CoT 능력이 있더라. 왜 1B는 실패했을까? LLM의 chain-of-thought를 Multi-modal에 그대로 이용하면 hallucination이 등장해서 성능이 오히려 악화되는 현상. 
- **idea :** QCM(question / context / multiple choice)를 보고 rationale을 생성하는 모델, rationale과 QCM을 받고 answer를 생성하는 모델 두개를 학습. 아키텍쳐는 같으나 따로 학습한다. 이때 두 모델 모두 vision feature를 추가로 받음.
- **input/output :** image, context, question, options -> gold rationale / image, context, question, option, rationale -> answer
- **architecture :** DETR encoder + T5(initialized by unified QA)
- **objective :** cross entropy loss
- **baseline :** No-CoT(one-stage model), CoT w/o visual feature, CoT with caption  
- **data :** ScienceQA
- **evaluation :** RougeL, accuracy
- **result :** language only CoT GPT3.5보다 우위.
- **contribution :** 처음으로 visual 정보를 보는 CoT를 제안한듯 하다
- **etc. :**

## Details
### Problem
<img width="552" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5dff0b2d-86cf-47a6-b6ed-12775838f228">

text-only 모델로 SicenceQA에 대해 one-stage setting(reasoning과 answer를 한번에 뽑게하는?)으로 학습하게 했더니 CoT를 안 한것보다 성능이 안좋아졌다.
이게 왜 이런지 보기 위해서 QCM -> R / QCMR -> A로 나누어 성능을 봤더니 이랬다. 

<img width="566" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a60dd92d-20b1-4385-9430-5694e56fd917">

<img width="581" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/cb47651d-48df-4335-8286-3c952570927d">

즉 rationale을 잘못 생성하고 있어서 일어난 거였다. 아래 예시를 보면 

<img width="1148" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/eb4339f3-8d5a-4077-9f7e-7258dfbaa4f5">

당연한거긴 한뎅.. 이미지를 안보고 rataionale를 만들라고 하니 이미지와 상반되는걸 본 것처럼 hallucination -> 성능이 떨어짐 

## Framework
<img width="1150" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7d711b7c-407b-4141-a2ab-d815cc17154a">

(i) rationale generation과 (ii) answer inference 두 단계로 나누고, 아키텍쳐는 같지만 따로 학습된다(이에 대한 이유는 논문에 있나?)
(i) 단계에서 input은 $X=\{X^1_{language}, X_{vision}\}$이고 ouput은 rationale인 $R$이다.
(ii) 단계는 생성한 $R$을 concat하여 input X'={concat(X_^1_{language}, R), X_{vision}} 를 넣고 answer $A$를 생성하게 한다.

## Architecture 
- Encoding
<img width="522" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d39dd4c1-d4c4-45bf-b1c2-cda9222bb38f">

VisionExtractor는 DETR. $H_{vision}\in\mathbb{R}^{m\times d}$이고 (m: # of patches, d: hidden dim) lanugage output이랑 차원을 맞춰줬다고 하넹 

- Interaction
<img width="346" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/20da5879-1781-478e-ae1c-03a9d512425b">

Q : $H_{language}$
K=V: $H_{vision}$

gated fusion을 해서 얼마나 vision 정보를 볼지도 학습하게했다. 

<img width="485" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/68d15375-3d18-45bc-98ce-13623cc5b5d0">

## Result
<img width="1153" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2aea36cc-4abd-4c5e-bd70-ac7b40ac33ed">

GPT-3.5 성능보다 우위

<img width="542" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c8d78875-1bb5-4128-a913-6e110cf55372">

two-stage baseline(image 안보고 two-stage로 학습)의 경우 처음에 성능은 좋았으나 에폭이 갈 수록 개선이 안됨. 
one-stage baseline은 왜 좋아지는거징? 흠..

- vision features architecture

<img width="513" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/29d3879b-5e49-45ac-8858-f8e9831feb71">

- language model architecture
<img width="557" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/559625dc-1ac4-4850-a602-b19c87333bfa">

- multimodal CoT 오류 case study
<img width="531" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0bc77578-e14a-4434-b3c1-a2575fad5f24">
