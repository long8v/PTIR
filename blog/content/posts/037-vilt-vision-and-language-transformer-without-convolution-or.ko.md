---
title: "[32] ViLT: Vision-and-Language Transformer Without Convolution or Region Supervision"
date: 2022-06-28
tags: ['multimodal', '2021Q2', 'naver']
paper: "https://arxiv.org/pdf/2102.03334.pdf"
issue: 37
issueUrl: "https://github.com/long8v/PTIR/issues/37"
---
![image](https://user-images.githubusercontent.com/46675408/176077410-1ff5fe50-f2bb-49dd-a84b-35013951ecd9.png)

[paper](https://arxiv.org/pdf/2102.03334.pdf), [code](https://github.com/dandelin/vilt)

## TL;DR
- **task :** Vision-and-Language Pretraining(VLP) 
- **problem :** 기존 VLP에서 CNN backbone, object detector를 필수적으로 사용하고 visual encoder를 헤비하게 만들어서 성능을 뽑긴 좋지만 실제 application에 적용하기엔 적합하지 않다.  
- **idea :** CNN 없이 통합된 VLP 모델을 만들자. 
- **architecture :** visual 임베딩은 ViT처럼, word embedding은 BERT 방식으로. 각각의 인코더에서 나온 임베딩을 각자 modal-type 임베딩과 합한뒤 하나의 트랜스포머 인코더에 넣고 나온 output으로 아래 pretraining task로 학습.
- **objective :** Image Text Matching(이미지-텍스트 페어에서 이미지를 50% 확률로 다른 이미지로 바꾸고 원래의 pair가 맞는지 binary로 학습), MLM, whole word masking(토큰 단위가 아니라 원래 word 단어를 마스킹. `gi`, `##raf`, `##fe`에서 가운데만 마스킹하면 비쥬얼 정보 없이 텍스트 정보만으로 예측이 가능함.)
- **baseline :** ViLBERT, UNITER, PixelBERT ... 
- **result :** time(ms)를 benchmark 대비 4~60배 개선하면서 성능도 ㄱㅊ
- **contribution :** 1) deep visual encoder없이 만들어 runtime / 효율성 개선 2) region feature나 deep convolution없이 단순한 아키텍쳐로 비슷한 성능 3) word masking, image augmentation이 VLP 성능을 개선함을 보임
- **data :** (pretraining) MSCOCO, Visual Genome, [SBU captions](https://www.cs.virginia.edu/~vicente/sbucaptions/), Google Conceptual Captions 
![image](https://user-images.githubusercontent.com/46675408/176082305-b7b3d3e3-e7ea-4b7a-a4d6-47d9cd3fbb42.png)
(downstream)
VQA v2, NLVR2(Natural Language for Visual Reasoning, 두 이미지와 두 이미지간 관계(triplet)이 주어지고 질문이 주어졌을 때 binary classification), 
Retrieval MSCOCO, Flickr30k for image-to-text, text-to-image retrieval

## Details
![image](https://user-images.githubusercontent.com/46675408/176084187-1146128d-f6b9-4d1d-b904-62fd5f3dd3fc.png)
