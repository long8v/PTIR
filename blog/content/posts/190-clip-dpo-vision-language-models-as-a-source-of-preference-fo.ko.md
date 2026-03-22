---
title: "[171] CLIP-DPO: Vision-Language Models as a Source of Preference for Fixing Hallucinations in LVLMs"
date: 2024-08-30
tags: ['ECCV', 'RL', 'MLLM', '2024Q3']
paper: "https://www.arxiv.org/abs/2408.10433"
issue: 190
issueUrl: "https://github.com/long8v/PTIR/issues/190"
---
<img width="800" alt="image" src="https://github.com/user-attachments/assets/ebe72de4-8626-4297-9ef5-3d5853cef631">

[paper](https://www.arxiv.org/abs/2408.10433)

## TL;DR
- **I read this because.. :** google scholar가 추천해줌
- **task :** VLM + RLHF
- **problem :** VLM의 hallucination 해결하고 싶은데 싸게 DPO 학습용 데이터 못만들까?
- **idea :** CLIP score 가지고 만들까?
- **input/output :** {image, question} -> score
- **architecture :** MobileVLM-v2), LLaVA 1.5
- **objective :** DPO loss 
- **baseline :** BLIP-2, InstructBLIP, Shira, OpenFlamingo, Qwn-VL ... ShareGPT4V, DPO 기법으로는 HA-DPO
- **data :** 이미지 소스는 SFT, MobileVLM-v2로 만들고 CLIP score와 휴리스틱으로 필터링 함. CLIP Score 기준 2이상 나는 것을 win / loose 페어를 만듦 
- **evaluation :** [AMBER](https://github.com/junyangwang0410/AMBER), CLIP에서 평가하는 분류(caption 생성하라고 한 뒤 siglip으로 zero-shot classification), VLM benchs(GQA, SQA, VQA, MME, MMB)
- **result :** AMBER 개선. QwenVL, GPT4V 말고 AMBER sota. 다른 벤치마크는 성능을 악화시키진 않으며 SQA나 MMB는 개선시키기도? 
- **contribution :** 싸게 DPO data 만들기. 
- **etc. :**

## Details
- why CLIP?
아래와 같이 hallucination을 만든 뒤에 CLIP vs LLaVA 1.5 logit 비교 
<img width="500" alt="image" src="https://github.com/user-attachments/assets/d3ca114a-89bf-45a2-b6c0-e41dfdf88594">

<img width="300" alt="image" src="https://github.com/user-attachments/assets/6840772b-d3ad-418c-bfb0-0b7da038af28">

bar = hallucinated caption에 대해 logit을 더 크게 할당한 것 (진파랑 llava 1.5 / 하늘색 CLIP) 

CLIP이 VLM보다는 hallucinated object, attribute, relation을 잘 뽑아낸다! 

- `CLIP-DPO`
DPO 알고리즘은 바꾼 것이 없고 데이터 풀만 바꿈
<img width="590" alt="image" src="https://github.com/user-attachments/assets/7b8e10d4-2f4d-428a-a8a9-7ceaa5340dde">

- data
<img width="648" alt="image" src="https://github.com/user-attachments/assets/068998e0-8cb3-466a-a549-80ab70f3cdb9">

1) generation : 가벼운 VLM (논문에선 MobileVLM-v2 family)를 사용하여 두가지 형태로 만듦 
- generic caption
Mobile VLM v2 모델들에게 caption 만들어달라고 함. 5개의 프롬프트 사용

- per-image QA
<img width="634" alt="image" src="https://github.com/user-attachments/assets/d9dff43b-195f-413d-a5a7-12c256b2c653">

Mistral 7B에게 이미지에서 질문과 맞는 답변, 틀린 답변을 만들라고 함 

2) data annotation
- CLIP ranking : CLIPScore를 다 담
- Global filtering : 
  - text 가 들어있는 이미지가 CLIPScore가 높아서 제거  
  - CLIPScore threshold 이하 제거 
  - long caption 제거  
  - question도 CLIPScore재서 낮은것 제거 (e.g. “what is the main object in the image?”)
<img width="630" alt="image" src="https://github.com/user-attachments/assets/f73732cc-0f56-42bd-83f6-b402b1a2fab1">

- Pair filtering : 
  - QA의 경우 Q에서 이미지에 대한 설명을 regex로 뺀 다음에 대답과 concat후 CLIPScore가 낮은걸 정제 (?) 
  - CLIPScore의 차이가 2 이상인 것만 
  - 캡션 길이가 너무 다르지 않은 것만

최종적으로 750K pair 확보 -- 이 중 50K가 QA 나머지는 700K는 caption 

<img width="634" alt="image" src="https://github.com/user-attachments/assets/76a77d41-7de4-4a02-b4e1-5a5c42399d91">

#### Result 

<img width="644" alt="image" src="https://github.com/user-attachments/assets/8196d514-f547-4cb1-bd75-a246a482a8f7">

<img width="620" alt="image" src="https://github.com/user-attachments/assets/9865fec5-8865-4936-a5dc-7eb5c50b6cdb">

<img width="623" alt="image" src="https://github.com/user-attachments/assets/61eb1f33-a0f4-4860-ac2d-b11b9d12ecfc">
