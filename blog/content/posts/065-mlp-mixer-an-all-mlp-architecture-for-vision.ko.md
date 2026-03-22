---
title: "[59] MLP-Mixer: An all-MLP Architecture for Vision"
date: 2022-09-01
tags: ['backbone', '2021Q2', 'google', '25min']
paper: "https://arxiv.org/pdf/2105.01601.pdf"
issue: 65
issueUrl: "https://github.com/long8v/PTIR/issues/65"
---
![image](https://user-images.githubusercontent.com/46675408/187809895-d06968f3-7f15-4d4c-a0b0-670f8c529dea.png)

[paper](https://arxiv.org/pdf/2105.01601.pdf)

## TL;DR
- **task :** image classification
- **problem :** vision backbone without CNN and transformer
- **idea :** ViT의 input 방식을 따라가되, attention이나 convolution 없이 MLP로만 해보자!
- **architecture :** 이미지를 겹치지 않는 패치 단위로 자르고, 하나의 projection으로 C차원으로 보냄. 그러면 S개의 C차원의 matrix $\mathbb{R}^{S\times C}$ 가 생기는데 이를 열 차원에서 하면 "token-mixing MLP", 행 차원에서 하면 "channel-mixing MLP"이 되게 됨. 
- **objective :** CrossEntropy Loss
- **baseline :** BiT-R, Mixer-L, HaloNet
- **data :** ILSVRC2012 ImageNet, CIFAR-10/100, Oxford-IIIT-pets, JFT-30
- **result :** 비슷한 성능, 높은 throughput, FLOPS
- **contribution :** O(n) complexity, simple architecture, MLP revisited! 
- **limitation or 이해 안되는 부분 :**

## Details
<img width="717" alt="image" src="https://user-images.githubusercontent.com/46675408/187814147-55d23c3d-565a-40f4-8819-1a52270c21dd.png">

<img width="1536" alt="image" src="https://user-images.githubusercontent.com/46675408/189045274-2d0810c3-54b6-452f-a229-df9668965263.png">

<img width="701" alt="image" src="https://user-images.githubusercontent.com/46675408/187814166-c8a07d6a-a614-4a37-9990-4ca98c00f9d2.png">

<img width="1538" alt="image" src="https://user-images.githubusercontent.com/46675408/189045386-1f5f138a-5220-4610-ada8-d07e82a03049.png">

