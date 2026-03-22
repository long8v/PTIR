---
title: "[61] Generative Modeling by Estimating Gradients of the Data Distribution"
date: 2022-09-03
tags: ['generative', '2020Q4']
paper: "https://arxiv.org/pdf/1907.05600.pdf"
issue: 67
issueUrl: "https://github.com/long8v/PTIR/issues/67"
---
![image](https://user-images.githubusercontent.com/46675408/188270401-c5ec5b9a-7c41-49b9-9ed3-b0bc26b7a3fe.png)

[paper](https://arxiv.org/pdf/1907.05600.pdf)

## TL;DR
- **task :** generative model
- **problem :** generative model은 데이터 분포를 추정해서 sampling을 통해 데이터를 생성하는 것. 이때 pdf는 적분이 1이 되어야한다는 것 때문에 구하기가 어려움. 그래서 pdf의 추정 없이 바로 log p(x)를 x로 미분한 score를 추정하는 것이 score matching 방법! 이때 score matching 방법은 low-dimensional manifold에서 score가 정의되지 않는 것이 문제임.
- **idea :** gaussian noise를 크기에 따라 여러번 추가하고 각 noise level을 하나의 conditional score network로 학습하자. sampling은 langevin dynamic sampling(x의 미분값을 iterative하게 하면 원래 x를 얻을 수 있다)을 통해 할 수 있다.  
- **architecture :** U-Net
- **objective :** 우리가 추정한 score network $s_\theta$에 x에 가우시안 noise를 추가한 $\tilde x$를 넣었을 때의 output과 우리가 추가한 noise distribution의 score 차이
- **baseline :** PixelCNN, WGAN, BigGAN
- **data :** CIFAR10, MNIST, CelebA
- **result :** InCeption, FID에서 준수한 성적.(BigGAN, MoLM 보다 조금 낮음)
- **contribution :** score based model w/o any sampling or adversarial training 
- **limitation or 이해 안되는 부분 :** sliced score matching

## Details
- [notion](https://long8v.notion.site/NCSN-9c399c02d5d84a5693d1dece6bf469c2)