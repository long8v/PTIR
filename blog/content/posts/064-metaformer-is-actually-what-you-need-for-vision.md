---
title: "MetaFormer Is Actually What You Need for Vision"
date: 2022-08-31
tags: ['2021Q4', 'backbone', '25min']
paper: "https://arxiv.org/pdf/2111.11418.pdf"
issue: 64
issueUrl: "https://github.com/long8v/PTIR/issues/64"
---
<img width="667" alt="image" src="https://user-images.githubusercontent.com/46675408/187567450-2fe24d04-8359-4de1-9448-99c916b456cc.png">

[paper](https://arxiv.org/pdf/2111.11418.pdf)

## TL;DR
- **task :** image classification / object detection / instance segmentation / vision backbone
- **problem :** Prior research shows that replacing the attention module that mixes information between tokens in the transformer with MLP works well.
- **idea :** Consider having a token mixer like self-attention or mlp above as an abstract module.
- **architecture :** token -> token embedding -> "token mixer" -> FFN. Suggest token mixer to be pooling here (PoolFormer)
- **objective :** loss for each task
- **baseline :** RSB-ResNet, ViT, DeiT, PVT, MLP-Micer, ResMLP, Swin-Mixer,...
- **data :** ImageNet-1K, COCO, ADE20K
- **result :** Performance comparable to SOTA models. ImageNet10K top-1 accuracy is higher with lower parameters than DeiT or ResMLP.
- **contribution :** Solved MLP mixer in general?

## Details
<img width="678" alt="image" src="https://user-images.githubusercontent.com/46675408/187568081-aeef2f2c-89d0-460f-89f0-fd40475ff818.png">
