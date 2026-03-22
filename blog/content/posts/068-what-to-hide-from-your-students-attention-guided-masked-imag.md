---
title: "[62] What to Hide from Your Students: Attention-Guided Masked Image Modeling"
date: 2022-09-06
tags: ['SSL', '2022Q1', '25min', 'ECCV']
paper: "https://arxiv.org/pdf/2203.12719.pdf"
issue: 68
issueUrl: "https://github.com/long8v/PTIR/issues/68"
---
![image](https://user-images.githubusercontent.com/46675408/188522702-47ba4767-89ba-461d-bc34-6da881ecfff4.png)

[paper](https://arxiv.org/pdf/2203.12719.pdf)

## TL;DR
- **task :** self-supervised learning -> image classification, object detection, image segmentation
- **problem :** Think about the strategy for selecting the tokens that are masked in the Masked Image Modling (MIM) you are using in SSL.
- **idea :** Let's mask the high attention score when put into ViT!
- **architecture :** teacher ViT receives all input tokens and has a high attention score, masking the fact that it has a high attention score. student takes on the MIM task. teacher's weight is updated with the exponential moving average (EMA) of student's weight. The architecture is based on ViT-S/16
- **objective :** MIM loss(=reconstruction loss), distillation loss(difference in output for [CLS] tokens of student and teacher)
- **baseline :** iBOT, DINO, MST 
- **data :** ImageNet-1k for pretraining, CIFAR-10, CIFAR-100, Oxford Flower, COCO, ADE20K
- **result :** higher performance than random masking
- **contribution :** Exploring masking strategies in MIM
- **Limitations or things I don't understand :**

## Details
![image](https://user-images.githubusercontent.com/46675408/188523034-794d7d08-4673-455d-9117-d259c2d8d221.png)
![image](https://user-images.githubusercontent.com/46675408/188523046-39bfd77e-b835-435c-9588-06c19a0df56d.png)
