---
title: "[92] Long-Tail Learning via Logit Adjustment"
date: 2022-12-26
tags: ['2020Q3', 'google', '25min', 'imbalance']
paper: "https://arxiv.org/pdf/2007.07314.pdf"
issue: 101
issueUrl: "https://github.com/long8v/PTIR/issues/101"
summary: "trick used in #57 - outperform baselines"
---
<img width="602" alt="image" src="https://user-images.githubusercontent.com/46675408/209494125-e7b3f1b1-0146-4a44-aa70-0856313be676.png">

[paper](https://arxiv.org/pdf/2007.07314.pdf), [code](https://github.com/google-research/google-research/tree/master/logit_adjustment)

## TL;DR
- **I read this because.. :** trick I used in #57
- **task :** long-tail image classification 
- **problem :** In the real-world, classes are often unbalanced
- **idea :** logit adjustment based on label frequency
- **architecture :** ResNet-32, ResNet-50
- **objective :** Add the values that go into the exponential of softmax plus the frequency per class multiplied by $\tau$.
- **baseline :** ERM, weight normalisation, Adaptive, Equalized
- **data :** CIFAR-10-LT, CIFAR-100-LT, ImageNet-LT, iNaturalist2018
- **evaluation :** balanced error(average by class)
- **result :** outperform baselines
- **limitation / things I cannot understand :** Reading, but not understanding formulas and logic

## Details
### Post-hoc logit adjustment
<img width="482" alt="image" src="https://user-images.githubusercontent.com/46675408/209494647-6a590f71-12e3-46c7-aa41-afe7fc3f8ee6.png">

### Logit adjusted softmax cross-entropy
<img width="665" alt="image" src="https://user-images.githubusercontent.com/46675408/209494714-1831906a-8206-43d4-8e81-e5244ea620e7.png">

### Result
<img width="727" alt="image" src="https://user-images.githubusercontent.com/46675408/209494738-a7d649d6-642f-4b9b-8791-5516ed8e84d3.png">

