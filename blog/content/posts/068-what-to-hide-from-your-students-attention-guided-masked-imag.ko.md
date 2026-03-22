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
- **problem :** SSL에서 사용하고 있는 Masked Image Modling(MIM)에서 mask되는 토큰을 선택하는 전략에 대해 생각해보자
- **idea :** ViT에 넣었을 때 attention score가 높게 걸리는 걸 마스킹하자!
- **architecture :** teacher ViT가 모든 input tokens를 받고 attention score가 높은걸 masking. student는 MIM 태스크를 품. teacher의 weight는 student의 weight의 exponential moving average(EMA)로 업데이트 됨. 아키텍쳐는 ViT-S/16
- **objective :** MIM loss(=reconstruction loss), distillation loss(student과 teacher의 [CLS] 토큰에 대한 output 차이)
- **baseline :** iBOT, DINO, MST 
- **data :** ImageNet-1k for pretraining, CIFAR-10, CIFAR-100, Oxford Flower, COCO, ADE20K
- **result :** random masking보다 높은 성능
- **contribution :** MIM에서 masking strategy 탐색
- **limitation or 이해 안되는 부분 :**

## Details
![image](https://user-images.githubusercontent.com/46675408/188523034-794d7d08-4673-455d-9117-d259c2d8d221.png)
![image](https://user-images.githubusercontent.com/46675408/188523046-39bfd77e-b835-435c-9588-06c19a0df56d.png)
