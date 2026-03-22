---
title: "[126] ViLT: Vision-and-Language Transformer Without Convolution or Region Supervision"
date: 2023-08-09
tags: ['multimodal', '2021Q1', '25min', 'kakao']
paper: "https://arxiv.org/pdf/2102.03334.pdf"
issue: 138
issueUrl: "https://github.com/long8v/PTIR/issues/138"
---

<img width="892" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4da317f3-56b6-4c18-857d-6a37a67e8883">

[paper](https://arxiv.org/pdf/2102.03334.pdf), [code](https://github.com/dandelin/vilt) 

## TL;DR
- **I read this because.. :** fine-grained CLIP 읽으려다가 인용 되어있는거 보고 읽음. 
- **task :** VLM model -> VQAv2, NLVR2, retrieval
- **problem :** image -> CNN -> region 으로 Feature 뽑고 학습하면 너무 오래 걸린다. 
- **idea :** 그냥 ViT처럼 patch 후에 projection 한걸 바로 multi-modal Transformer에 넣어서 사용하자
- **input/output :** {image, text} -> matching score, masked token prediction
- **architecture :** Transformer encoder 
- **objective :** Image-Text matching, 
- **baseline :** pixelBERT, ViLBERT, OSCAR, VisualBERT
- **data :** MSCOCO, VG, GCC, SBU
- **evaluation :** 각각에 맞는 evaluation
- **result :** 10배 빠르게 runtime을 줄이고 성능이 비슷하거나 더 나음
- **contribution :** 각 modality에 대한 복잡한 디자인 최소화
- **etc. :**

## Details
### Motivation
<img width="423" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2434236b-82b9-41ed-9e0e-a7d9733489da">

<img width="825" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b42d1d83-f725-4def-8ea6-aeec1bcd16b6">


### Word Patch Alignment
<img width="170" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/239ee8f0-9426-4622-b88e-a92b39cc6e62">

여기서 무슨 일이 일어날까? 
이전 [UNITER: UNiversal Image-TExt Representation Learning](https://arxiv.org/pdf/1909.11740.pdf)에서 거의 비슷. region 대신 patch로 했다는게 다른 점.
<img width="308" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/df6e618c-5360-46ee-bea9-617fbf881cd2">

직접적인 word-region에 대한 supervision을 주는건 아니고 [Optimal Transport](https://en.wikipedia.org/wiki/Transportation_theory_(mathematics))라는 알고리즘으로 image embedding과 word embedding 사이의 transport를 최소화하는 cost를 구해서 이걸 loss로 추가해서 alignment가 더 잘되도록 

<img width="707" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f2c8e029-6bee-4ffd-bb67-5c5c510b5216">

- c: distance. cosine 유사도 사용. 
- $T\in \mathbb{R}^{T\times K}$ : transport plan. learned to optimize alignment between $w$ and $v$. 학습되는 건가보넹..

여기서 이 최소 거리를 구하는 방법이 어려워서 IPOT이라는 wasserstein distance를 approximate하는 복잡한 방법으로 근사. 
이 부분 구현은 [여기](https://github.com/dandelin/ViLT/blob/762fd3975c180db6fc88f577cf39549983fa373a/vilt/modules/objectives.py#L38-L87)

<img width="851" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/aebe332a-f82e-472f-b367-87cac0dc0188">

이런 결과 ->WPA 때문인가?
