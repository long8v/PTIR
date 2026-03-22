---
title: "[58] MetaFormer Is Actually What You Need for Vision"
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
- **problem :** transformer의 token간 information 정보를 mixing하는 attention 모듈을 MLP로 바꿨더니 잘되더라는 선행연구. 
- **idea :** 위의 self-attention 또는 mlp같은 token mixer를 abstract한 모듈로 두어보자. 
- **architecture :** token -> token embedding -> "token mixer" -> FFN. 여기서 token mixer를 pooling으로 하는 걸 제안(PoolFormer)
- **objective :** 각각의 task에 맞는 loss
- **baseline :** RSB-ResNet, ViT, DeiT, PVT, MLP-Micer, ResMLP, Swin-Mixer,...
- **data :** ImageNet-1K, COCO, ADE20K
- **result :** SOTA 모델들과 비슷한 성능. ImageNet10K top-1 accuracy는 DeiT나 ResMLP보다 더 낮은 파라미터로 더 높은 성능
- **contribution :** MLP mixer를 일반적으로 풀었다?

## Details
<img width="678" alt="image" src="https://user-images.githubusercontent.com/46675408/187568081-aeef2f2c-89d0-460f-89f0-fd40475ff818.png">
