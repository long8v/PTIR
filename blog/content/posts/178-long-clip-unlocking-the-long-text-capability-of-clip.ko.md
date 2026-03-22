---
title: "[159] Long-CLIP: Unlocking the Long-Text Capability of CLIP"
date: 2024-05-10
tags: ['25min', 'CLIP', '2024Q1']
paper: "https://arxiv.org/pdf/2403.15378"
issue: 178
issueUrl: "https://github.com/long8v/PTIR/issues/178"
---

<img width="785" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/6ad2d5fa-c0c0-4c5a-818b-153bf7e8fc9f">

[paper](https://arxiv.org/pdf/2403.15378), [code](https://github.com/beichenzbc/Long-CLIP)

## TL;DR
- **I read this because.. :** github follow 하는 분이 Star 눌러서 알게됨 
- **task :** CLIP with long context
- **problem :** CLIP이 77 토큰 개수로 제한되게 학습되어 있고 이 중에 유효하게 사용되는 토큰은 20개이다.
- **idea :** 긴 CLIP을 학습 하자. PE를 interpolate 하되 유효 토큰 20개는 남기고 나머지만 Interpolate 하자
- **input/output :** {image, text} -> score
- **architecture :** CLIP ViT-B/16, ViT-L/14
- **objective :** infoNCE 
- **baseline :** CLIP
- **data :** ShareGPT4V 1M  
- **evaluation :** ImageNet, COCO, FLICKR retrieval, ShareGPT4V retrieval (long context retreival)
- **result :** 정량적으로 좋은 성능. 훨씬 context를 잘 파악하는 듯한 느낌. 
- **contribution :**
- **etc. :**

## Details
### Problem
<img width="928" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4bec18fa-4065-45dc-9d8f-c21895d48430">

### PE interpolate strategy
<img width="842" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ef2171c7-be7e-4bab-810f-808c8c69805b">

### finetuning strategy 
<img width="865" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2781260b-4be5-4265-8857-fe50fa1d79f5">
- finegrained alignment는 하던대로 하는듯
- coarse grained alignment는 이미지에 PCE 알고리즘(PCA한 뒤 Top 32개 element를 남김)을 적용한뒤에 threshold 빼는건 낮춘 뒤 골라진 Eigenvector와 Eigenvalue로 weighted sum 한거와 short caption이 align 되는 형식 

<img width="709" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5370334c-de99-412e-b476-797fce30fb3a">


<img width="709" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d5ca455a-fa12-4df5-9b94-658b732e9f85">


### Result
<img width="751" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e3e0cb2a-b85e-4327-aa75-ee60ab43eb48">

<img width="746" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/e6a9ddf6-1e46-4c49-8722-19d12066b9ca">

<img width="747" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/738cce63-69fb-4194-a306-5adea2ff23fa">

<img width="734" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9af7b461-dd12-4c8e-a75f-01fdeb56763d">
