---
title: "[5] An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale"
date: 2022-01-13
tags: ['ViT', 'backbone', '2021Q1', 're-read']
paper: "https://arxiv.org/pdf/2010.11929.pdf"
issue: 5
issueUrl: "https://github.com/long8v/PTIR/issues/5"
---
![image](https://user-images.githubusercontent.com/46675408/149278862-fd941e4a-54b0-40da-89cb-13c1c60bd4b8.png)
[paper](https://arxiv.org/pdf/2010.11929.pdf)
[paper summary](https://long8v.notion.site/ViT-9e25358e194e45b484a0b10ea6b570e9)
[implementation](https://github.com/google-research/vision_transformer)

**problem :** fully self-attention인 구조로, 기존 Transformer의 구조에서 변경을 최소화하면서 이미지 분류 문제를 풀어보자
**solution :** 이미지를 P x P개의 패치를 자르고, flatten한 뒤 linear projection으로 D차원으로 만들어 줌. 이 결과로 나온 패치 임베딩을 트랜스포머 인코더 인풋에 넣음. `[CLS]` 토큰을 추가하여 output에 MLP를 얹어 프리트레이닝, 이후 분류 MLP만 변경하여 파인튜닝.  
**result :** 적은 데이터에서는 ResNet계열보다 성능이 안좋았지만 큰 데이터에 대해 학습했을 때는 ResNet보다 빠르게 학습하고 SOTA