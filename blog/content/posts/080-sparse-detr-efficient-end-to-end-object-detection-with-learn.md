---
title: "Sparse DETR: Efficient End-to-End Object Detection with Learnable Sparsity"
date: 2022-10-20
tags: ['2021Q4', 'ICLR', 'object detection', 'sparse', 'kakao']
paper: "https://arxiv.org/abs/2111.14330"
issue: 80
issueUrl: "https://github.com/long8v/PTIR/issues/80"
summary: "more efficient DETR than deformable DETR"
---
<img width="579" alt="image" src="https://user-images.githubusercontent.com/46675408/196855402-34aa58d9-290b-45ba-9b3c-0fda4a4e1044.png">

[paper](https://arxiv.org/abs/2111.14330), [code](https://github.com/kakaobrain/sparse-detr)

## TL;DR
- **task :** object detection, efficient DETR 
- Problem :** deformable DETR reduces the key when given a query with deformable attention, but because it uses multi-scale features, the number of tokens in the encoder input is 20 times larger, which makes inference rather slow.
- Idea :** Images have a lot of background and only salient objects need attention. Let's make the token that goes into the encoder sparse!
- **architecture :** Create a score network that is a deformable DETR that measures the objectness of inputs entering the encoder. The score network can be trained like auxiliary loss by 1) adding detection heads to the backbone feature map, or 2) Decoder Attention Map (DAM), which is a pseudo-label with 1 for p% of tokens in the cross attention map and 0 for the rest.
- **objective :** DETR loss + add auxiliary loss by putting detection head also in encoder
- **baseline :** Faster R-CNN, DETR, DETR-DC5, Deformable DETR
- **data :** COCO 2017
- **result :** Performance similar to deformable with only 10% of encoder tokens used
- **contribution :** more efficient DETR than deformable DETR
- **Limitations or things I don't understand :**

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

encoder layer 12 does not learn without auxiliary losses