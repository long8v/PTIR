---
title: "[92] Long-Tail Learning via Logit Adjustment"
date: 2022-12-26
tags: ['2020Q3', 'google', '25min', 'imbalance']
paper: "https://arxiv.org/pdf/2007.07314.pdf"
issue: 101
issueUrl: "https://github.com/long8v/PTIR/issues/101"
---
<img width="602" alt="image" src="https://user-images.githubusercontent.com/46675408/209494125-e7b3f1b1-0146-4a44-aa70-0856313be676.png">

[paper](https://arxiv.org/pdf/2007.07314.pdf), [code](https://github.com/google-research/google-research/tree/master/logit_adjustment)

## TL;DR
- **I read this because.. :** #57 에서 사용한 trick
- **task :** long-tail image classification 
- **problem :** real-world에서는 class가 imbalance한 경우가 많다
- **idea :** label frequency 기반으로 logit adjustment를 함
- **architecture :** ResNet-32, ResNet-50
- **objective :** softmax의 exponential에 들어가는 값에다가 class별 frequency를 $\tau$를 곱해서 더함.
- **baseline :** ERM, weight normalisation, Adaptive, Equalized
- **data :** CIFAR-10-LT, CIFAR-100-LT, ImageNet-LT, iNaturalist2018
- **evaluation :** balanced error(class별 평균)
- **result :** outperform baselines
- **limitation / things I cannot understand :** 수식 및 논리를 이해하지는 않고 읽음

## Details
### Post-hoc logit adjustment
<img width="482" alt="image" src="https://user-images.githubusercontent.com/46675408/209494647-6a590f71-12e3-46c7-aa41-afe7fc3f8ee6.png">

### Logit adjusted softmax cross-entropy
<img width="665" alt="image" src="https://user-images.githubusercontent.com/46675408/209494714-1831906a-8206-43d4-8e81-e5244ea620e7.png">

### Result
<img width="727" alt="image" src="https://user-images.githubusercontent.com/46675408/209494738-a7d649d6-642f-4b9b-8791-5516ed8e84d3.png">

