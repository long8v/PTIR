---
title: "[60] Efficient Sparsely Activated Transformers"
date: 2022-09-02
tags: ['MoE', '2022Q3', '25min', 'AutoML']
paper: "https://arxiv.org/pdf/2208.14580.pdf"
issue: 66
issueUrl: "https://github.com/long8v/PTIR/issues/66"
---

![image](https://user-images.githubusercontent.com/46675408/188034202-71ddef7d-3317-4e0e-8ee0-84480a3ec0b8.png)

[paper](https://arxiv.org/pdf/2208.14580.pdf)

## TL;DR
- **task :** lanugage modeling
- **problem :** transformer가 너무 크고 무겁다. inference latency 목표에 맞게 알아서 네트워크가 구성되면 좋겠다.
- **idea :** NAS 써서 latency가 주어졌을 때, Transfomer-XL의 FFN, MHA, MoE FFN 레이어를 설계. 
- **architecture :** Transformer-XL, NAS가 block을 선택할 때 GumbelSoftmax 사용 + reinforcement 기반의 search.
- **objective :** cross-entropy loss + latent loss(=각 super block이 선택될 확률과 그 super block의 latency), latency loss는 목표 latency보다 높아질 경우에만 부가됨.
- **baseline :** Transformer-XL, PAR Transformer, Sandwich Transformer
- **data :** wt103, enwiki8
- **result :** 비슷한 성능에 2배 빠른 latency. 같은 크기의 MoE 적용안한(iso-parametric setting) 모델과 비교했을 때 PPL 대비 높은 normalized latency. 
- **contribution :** NAS for inference latency 
- **limitation or 이해 안되는 부분 :** MHA는 다들 MoE로 건드릴 생각을 안하네..왜징 -> runtime overhead introduced by dynamic behavior라고 나와있는데 뭔말인지 모르겠음.

## Details
- 트랜스포머의 각 레이어 별 latency
![image](https://user-images.githubusercontent.com/46675408/188034371-070796c9-2cba-46fe-8284-44eb1c5d97dd.png)

- MSA / FFN 각 하이퍼파라미터 변경할 때의 latency 비교
![image](https://user-images.githubusercontent.com/46675408/188034413-343792ea-f36a-4d6b-8235-6e9c8f798032.png)

- NAS가 서치한 모델 아키텍쳐 구성들
![image](https://user-images.githubusercontent.com/46675408/188034380-9391629d-6551-4b21-af08-4e811abffa8e.png)

MHA레이어의 개수와 차원을 줄이고, MoE나 FFN을 추가하는 양상.

- MoE
![image](https://user-images.githubusercontent.com/46675408/188036741-7b5d2c76-a45c-4be8-a7cc-5341fa68cf15.png)

- search space for NAS
![image](https://user-images.githubusercontent.com/46675408/188036769-8b71ca8e-2166-4431-ba98-e1c2be035ca0.png)
