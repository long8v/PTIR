---
title: "[63] Masked Autoencoders Are Scalable Vision Learners "
date: 2022-09-07
tags: ['2021Q4', 'SSL', '25min']
paper: "https://arxiv.org/pdf/2111.06377.pdf"
issue: 69
issueUrl: "https://github.com/long8v/PTIR/issues/69"
---
<img width="957" alt="image" src="https://user-images.githubusercontent.com/46675408/188760840-4a2876df-1339-44f1-b844-5c1333e0220a.png">

[paper](https://arxiv.org/pdf/2111.06377.pdf)

## TL;DR
- **task :** self-supervised learning -> image classification / object detection / segmentation
- **problem :** BERT처럼 masked 예측하는 방식으로 pretraining 하고 싶다
- **idea :** 오토인코더처럼 해보자. 그리고 image는 text 보다 각 토큰의 정보량이 적으니(spatial redundancy가 있다고 표현) mask ratio를 대신 엄청 높이자(논문에서 75%)
- **architecture :** encoder-decoder인데 encoder에는 mask되지 않은 토큰만 들어가고 encoder output에 원래 위치에 mask 임베딩을 끼워넣어서 decoder가 이를 보고 reconstruct하는 형태. encoder는 ViT-L, decoder는 자유롭게 선택해도 되나 논문에서는 encoder의 10% 정도의 computation이 드는 작은 decoder 사용.
- **objective :** mask된 토큰들에 대한 mean squared error(MSE)
- **baseline :** supervised learning, MoCov3, BeiT
- **data :** ImageNet-1K로 self-supervised pretraining. 이후 linear probing / finetuning. COCO, ADE20K, iNaturalists, Places로 finetuning.
- **result :** 다른 task로 transfer했을 때 SOTA 
- **contribution :** simple architecture with strong result!
- **limitation or 이해 안되는 부분 :**

## Details
### Architecture
<img width="511" alt="image" src="https://user-images.githubusercontent.com/46675408/188760803-71943291-5d15-43d1-aceb-5b1203d1be37.png">

### Result
<img width="999" alt="image" src="https://user-images.githubusercontent.com/46675408/188761395-90e9d96b-8aee-4570-b6f4-124db1dc7eea.png">

target을 noramalize 한게 더 잘됐음(전체 패치의 평균과 분산으로 normalize)

### Comparison with other SSL methods
<img width="477" alt="image" src="https://user-images.githubusercontent.com/46675408/188761464-291fa39d-1ef8-4e8a-aa94-842732db02e3.png">

mask ratio 높여도 잘된다. 
<img width="494" alt="image" src="https://user-images.githubusercontent.com/46675408/188761572-4bdec991-e655-441f-a37c-0bb59468316e.png">
얼룩말 한마리 된거 신기 ㅋㅋ

<img width="490" alt="image" src="https://user-images.githubusercontent.com/46675408/188761643-1c20261e-f6d2-4435-aa31-67f5d180f026.png">

근데 75%가 잘되긴 함