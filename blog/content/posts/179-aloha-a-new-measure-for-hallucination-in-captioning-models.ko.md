---
title: "[160] ALOHa: A New Measure for Hallucination in Captioning Models"
date: 2024-06-15
tags: ['evaluation', '2024Q2', 'NAACL']
paper: "https://arxiv.org/pdf/2404.02904"
issue: 179
issueUrl: "https://github.com/long8v/PTIR/issues/179"
---
![image](https://github.com/long8v/PTIR/assets/46675408/2eae7a2a-e566-4f78-bda7-fbd82a381126)

[paper](https://arxiv.org/pdf/2404.02904), [code](https://github.com/DavidMChan/aloha)

## TL;DR
- **I read this because.. :** 개인 연구 매우 관련 연구
- **task :** object hallucination evaluation
- **problem :** 기존 hallucination을 측정하기 위한 CHAIR는 string matching에 의존 하고 있고, COCO object에 한정되어 있다. 
- **idea :** LLM을 사용해서 파싱, DETR로 object 뽑고, S-BERT로 semantic similiarity로 bipartite matching
- **input/output :** {image, text} -> score (높을 수록 좋음)
- **baseline :** CHAIR, CLIPScore, RefCLIPScore
- **data :** FOIL, noCaps-FOIL(proposed), HAT(proposed)  
- **evaluation :** AP for task 1, LA for task 2(accuracy)
- **result :** Average Precision는 RefCLIPScore와 비슷한 성능, Localization Accuracy는 CHAIRs와 비슷하지만 noCaps-FOIL에서는 우월한 성능.
- **contribution :** object hallucination에 대한 captioning 모델에 대한 파이프라인 제안
- **etc. :** limitation을 숨기는게 아니라 잘 밝혀놔서 좋고, proposed method의 장점을 보여줄 수 있는 데이터를 만든 것도 좋다. 

## Details
### motivation
![image](https://github.com/long8v/PTIR/assets/46675408/0d327e2f-ec8f-4860-9a57-6e9ba8722374)

### overall pipeline
![image](https://github.com/long8v/PTIR/assets/46675408/163814a2-1d7e-4f2d-865f-5b6332a1327f)

(1) Extracting objects from candidates, references, and images
- GT 후보들
  - COCO로 학습된 DETR -> object candidates
  - referecne caption에서의 object parsing을 ChatGPT 사용해서 뽑음
    - 이때 attribute도 같이 뽑으라고 함
    - 단수화(s 빼기)
- predicted 
 - candidata catpion에서 마찬가지로 LLM으로 파싱
  
(2) Object Filtering 
- 캡션모델이 uncertain해서 `fork or knife`와 같은 서술을 하는 경우가 있음.
  - 이런 경우 candidate caption의 class set에서 뺌 (referecne에선 안 뺌)
- spaCy를 사용하여 referecne noun phrase에서 명사만 남김. 
 
(3) Object matching 
SBERT 사용 bipartite matching

최종 metric은 아래와 같이 "가장 최소의 matching similarity"
![image](https://github.com/long8v/PTIR/assets/46675408/fb1608e8-8f1c-42b6-81b7-f3a4ca7dba77)

### Result
##### HAT
![image](https://github.com/long8v/PTIR/assets/46675408/c96c33b4-1120-473f-b2d6-c28b219e6dcf)

HAT은 COCO 이미지에 대해서 직접 만듦. (TEST 400)
여기서 CHAIRs는 accuracy라고 함 (AP와 accuracy를 같은 테이블에 두어도 되는건가?)

#### FOIL
![image](https://github.com/long8v/PTIR/assets/46675408/28413040-74f1-405d-91c8-669003ef00d5)

no-caps에서 우수한 성적
여기 베이스라인이 50이어서 CLIPScore에서 재듯이 두개를 비교적으로 잰건지 잘 모르겠음. 그랬을 때 정확도가 아니라 AP라고 적어도 되는 건지 모르겠음

#### Qualitative
![image](https://github.com/long8v/PTIR/assets/46675408/8bdd3c05-2c60-401f-a3af-6a4cea819431)

##### Ablation
![image](https://github.com/long8v/PTIR/assets/46675408/1b451ca5-a034-4750-b77f-d96fecd2809c)
