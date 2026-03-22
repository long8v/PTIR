---
title: "[72] Sparse DETR: Efficient End-to-End Object Detection with Learnable Sparsity"
date: 2022-10-20
tags: ['2021Q4', 'ICLR', 'object detection', 'sparse', 'kakao']
paper: "https://arxiv.org/abs/2111.14330"
issue: 80
issueUrl: "https://github.com/long8v/PTIR/issues/80"
---
<img width="579" alt="image" src="https://user-images.githubusercontent.com/46675408/196855402-34aa58d9-290b-45ba-9b3c-0fda4a4e1044.png">

[paper](https://arxiv.org/abs/2111.14330), [code](https://github.com/kakaobrain/sparse-detr)

## TL;DR
- **task :** object detection, efficient DETR 
- **problem :** deformable DETR은 deformable attention을 통해 쿼리가 주어졌을 때 key를 줄여주지만 multi-scale feature를 쓰기 때문에 encoder input의 토큰 개수가 20배가 되어 inference 속도는 오히려 느리다. 
- **idea :** 이미지에는 배경이 많고 salient한 object들만 attention이 들어가면 된다. encoder에 들어가는 token을 sparse하게 만들어보자!
- **architecture :** deformable DETR인데 encoder에 들어가는 input의 objectness를 측정하는 score network를 만듦. 이때 score network는 1) backbone feature map에 detection head를 추가하여 auxiliary loss처럼 학습 또는 2) Decoder Attention Map(DAM): cross attention map에서 크게 잡힌 p%의 token을 1, 나머지를 0으로 둔 pseudo-label로 학습 할 수 있음. 
- **objective :** DETR loss + encoder에도 detection head 넣어서 auxiliary loss 추가
- **baseline :** Faster R-CNN, DETR, DETR-DC5, Deformable DETR
- **data :** COCO 2017
- **result :** encoder 토큰의 10%만 쓰더라도 deformable과 비슷한 성능
- **contribution :** more efficient DETR than deformable DETR
- **limitation or 이해 안되는 부분 :**

## Details
- encoder token sparsity
<img width="544" alt="image" src="https://user-images.githubusercontent.com/46675408/196856584-adcd10fc-c259-4b54-b951-b0c7bd83cf83.png">

<img width="755" alt="image" src="https://user-images.githubusercontent.com/46675408/196856640-b1d746ed-1bb5-45cf-b452-091b5b1c8a29.png">

- Decoder cross-Attention Map(DAM)
<img width="796" alt="image" src="https://user-images.githubusercontent.com/46675408/196856702-6513d15c-733a-480a-8304-72b24747b0b0.png">

<img width="360" alt="image" src="https://user-images.githubusercontent.com/46675408/196856734-5f33366e-a194-45ea-aeea-0b60a2a1c6c5.png">

- Architecture overall
<img width="815" alt="image" src="https://user-images.githubusercontent.com/46675408/196856754-21ab31f3-a3d3-4309-b8e1-75ce2ded1227.png">

- Detection result
<img width="818" alt="image" src="https://user-images.githubusercontent.com/46675408/196856783-49d7f9e5-ab35-4097-9f14-5e663a3e1db3.png">

- selection criteria
<img width="821" alt="image" src="https://user-images.githubusercontent.com/46675408/196856812-586b9512-7516-4332-8277-de6fc89f4b6d.png">

- ablation of num encoder layer
<img width="535" alt="image" src="https://user-images.githubusercontent.com/46675408/196856840-6e57602e-a81e-4e86-a2ac-5563fe61c21c.png">

encoder layer 12는 auxilary loss 없이는 학습이 안됨