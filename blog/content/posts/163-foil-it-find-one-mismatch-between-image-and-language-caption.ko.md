---
title: "[151] FOIL it! Find One mismatch between Image and Language caption"
date: 2024-03-03
tags: ['dataset', '2017', 'XAI', 'evaluation']
paper: "https://arxiv.org/pdf/1705.01359.pdf"
issue: 163
issueUrl: "https://github.com/long8v/PTIR/issues/163"
---

<img width="839" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0bc0c5c1-8b30-48a2-8eb3-bda6649943ee">

[paper](https://arxiv.org/pdf/1705.01359.pdf)

## TL;DR
- **I read this because.. :** 데이터 어떻게 만들었나 / 평가 방식은 어떤가 보고 싶어서 
- **task :** proposed. (1) FOIL Detection (2) FOIL word detection (3) FOIL word correction 
- **problem :** captioning, VQA 모델과 같은 VLM 모델들이 정말 두 모달리티를잘 이해하고 있는게 맞나?
- **idea :** caption의 word를 비슷한 다른 단어로 치환
- **input/output :** {image, caption} -> (1) FOIL인지 아닌지 (2) FOIL word가 어딘지 (3) FOIL word correction 
- **objective :** ce loss 
- **baseline :** 당시 sota VQA, Caption 모델 / caption만 본 LSTM, CNN LSTM
- **data :** COCO의 caption을 활용해서 65K(train) / 32K(test)의 이미지, 197K(train) / 99K(test)의 caption. 
- **evaluation :** (1) accuracy (2) FOIL caption 중에 word를 잘 찾았나. noun으로만 평가 / 전체 명사로 평가 (3) FOIL word가 주어졌을 때 원래의 단어로 다 바뀌나
- **contribution :** 이후 hallucination measure 등으로 사용됨 
- **etc. :** 
  - 17년도에서 할 수 있는 가장 합리적인 방법으로 만듦
  - 별로 유명한 evaluation set은 아닌 듯 -> 최근 LVLM benchmark로 하는게 더 나을지도 모르겠다
    - single noun 하나만 바꾼다는게 좀 단점이려나

## Details
### Task
<img width="417" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/83d6a138-ce4a-402b-895b-2bdb99b59da6">

### num samples
<img width="758" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2a375e8b-9dd3-4949-a3b8-80e925ccf1a1">


### 데이터 제작 방식
<img width="804" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b8fc1f83-261e-45e5-9282-1b5b0107626b">

1) MS-COCO에서 같은 supercategory를 가진 object로 pair를 만듬
- 이 때, 단어가 2개 이상인 애들을 뺌. e.g. traffic light
2) train / test category를 나눔
- 학습에 사용된 targe::foil pair는 test에 사용되지 않을 것임
3) foil caption을 만듦
- 이때, caption에 들어간 단어를 교체함
- 그리고 이미지 내에 존재하지 않는 object에 대해 교체함
- e.g. "강아지와 고양이가 밥을 먹는다"에서 고양이가 있으므로 강아지를 고양이로 교체하지는 않음
4) Neuraltalk이란 captioning 모델을 사용해서 가장 어려운 caption으로 선택함

### Evaluation
- T1은 그냥 분류
- T2는 {image, FOIL caption}이 주어졌을 때 foil word를 찾는지
- T3는 {image, FOIL caption, FOIL word}가 주어졌을 때 foil word를 잘 고치는지

<img width="409" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/267fea78-4857-4ba1-b41e-57a9f00862b3">

T1의 경우 원래 caption에 각 단어들을 지우고 captioner 모델로 생성을 하라고 한 뒤에 그 단어로 치환한 캡션과 원래 캡션 중에 모델이 더 높게 예측한 값을 비교해서 치환한 캡션이 더 높으면 FOIL으로 판단

<img width="414" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/039819c4-e4a0-48cf-8f0b-a48be7308666">

T2의 경우 Towards Transparent AI Systems: Interpreting Visual Question Answering Models (https://arxiv.org/pdf/1608.08974.pdf)
<img width="877" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/3c14e33e-d32f-47fb-998d-b9d153bf5b02"> 에서 사용된 occulsion 방법을 사용.
뭐냐 하면 question의 단어들을 하나씩 mask하고 forward를 한 뒤에 original predicted answer에 대해 score가 얼마나 바뀌었는지로 측정

<img width="329" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/21f7f90f-6d26-430c-bdb0-24f0653bd5bf">

T3의 경우 target word에 대한 linear regression을 수행 (얘만 새로 학습하는듯?)

### Analysis
<img width="869" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/54c5543d-f8ea-46a4-b536-a71ee880a5cb">


잘못만들어진 데이터셋
<img width="396" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/01d2b1f5-ea7f-4bee-ae0c-071e0e6438a0">
