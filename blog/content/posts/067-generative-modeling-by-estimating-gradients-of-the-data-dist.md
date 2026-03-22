---
title: "Generative Modeling by Estimating Gradients of the Data Distribution"
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
- **problem :** generative model is to generate data through sampling by estimating the data distribution. pdf is difficult to obtain because the integral must be 1. Therefore, the score matching method is to estimate the score directly by differentiating log p(x) by x without estimating the pdf! The problem with the score matching method is that the score is not defined in a low-dimensional manifold.
- **idea :** add multiple Gaussian noises of different sizes and train each noise level as one conditional score network. sampling can be done via langevin dynamic sampling (iterating over the derivatives of x gives the original x).
- **architecture :** U-Net
- **objective :** Difference between the output of our estimated score network $s_\theta$ with $\tilde x$ with Gaussian noise added to x and the score of the noise distribution we added.
- **baseline :** PixelCNN, WGAN, BigGAN
- **data :** CIFAR10, MNIST, CelebA
- **result :** InCeption, FID passes (slightly lower than BigGAN, MoLM)
- **contribution :** score based model w/o any sampling or adversarial training 
- **LIMITATION OR UNDERSTANDING :** sliced score matching

## Details
- [notion](https://long8v.notion.site/NCSN-9c399c02d5d84a5693d1dece6bf469c2)