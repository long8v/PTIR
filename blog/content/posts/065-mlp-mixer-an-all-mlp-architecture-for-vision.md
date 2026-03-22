---
title: "MLP-Mixer: An all-MLP Architecture for Vision"
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
- **idea :** Let's follow ViT's input method, but do it with MLP only, without attention or convolution!
- architecture :** Cut the image into non-overlapping patches and send it to C dimensions as a single projection. This results in S C-dimensional matrix $\mathbb{R}^{S\times C}$, which is called a "token-mixing MLP" in column dimension and a "channel-mixing MLP" in row dimension.
- **objective :** CrossEntropy Loss
- **baseline :** BiT-R, Mixer-L, HaloNet
- **data :** ILSVRC2012 ImageNet, CIFAR-10/100, Oxford-IIIT-pets, JFT-30
- **result :** Similar performance, high throughput, FLOPS
- **contribution :** O(n) complexity, simple architecture, MLP revisited! 
- **Limitations or things I don't understand :**

## Details
<img width="717" alt="image" src="https://user-images.githubusercontent.com/46675408/187814147-55d23c3d-565a-40f4-8819-1a52270c21dd.png">

<img width="1536" alt="image" src="https://user-images.githubusercontent.com/46675408/189045274-2d0810c3-54b6-452f-a229-df9668965263.png">

<img width="701" alt="image" src="https://user-images.githubusercontent.com/46675408/187814166-c8a07d6a-a614-4a37-9990-4ca98c00f9d2.png">

<img width="1538" alt="image" src="https://user-images.githubusercontent.com/46675408/189045386-1f5f138a-5220-4610-ada8-d07e82a03049.png">

