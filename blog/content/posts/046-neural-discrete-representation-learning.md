---
title: "Neural Discrete Representation Learning"
date: 2022-07-30
tags: ['DeepMind', '2017', 'generative']
paper: "https://arxiv.org/pdf/1711.00937.pdf"
issue: 46
issueUrl: "https://github.com/long8v/PTIR/issues/46"
---
<img width="757" alt="image" src="https://user-images.githubusercontent.com/46675408/181870151-040aef70-45f7-47fa-9787-e2ba91008cf1.png">

[paper](https://arxiv.org/pdf/1711.00937.pdf)

## TL;DR
- **task :** image generation
- **problem :** posterior collapse in generation model
- **idea :** discrete latent variable (idea from vector quantization)
- **architecture :** #45 with codebook(find nearest embedding vector) -> need copying gradient!
- **objective :** reconstruction error  + embedding loss w.r.t. reconstruction error + commitment loss(to train embedding + encoder in similar pace)
- **baseline :** VAE, VIMCO
- **data :** CIFAR10
- **result :** qualitatively good!
- **contribution :** VAE with discrete latent vector

## Details
[notion](https://long8v.notion.site/VQ-VAE-bd4f18b061ab4c95b99da60e422c3859)