---
title: "[66] Pointly-Supervised Instance Segmentation"
date: 2022-09-20
tags: ['2022Q2', '25min', 'ECCV', 'annotation', 'segmentation']
paper: "https://arxiv.org/pdf/2104.06404.pdf"
issue: 72
issueUrl: "https://github.com/long8v/PTIR/issues/72"
---
![image](https://user-images.githubusercontent.com/46675408/191143191-0224bb30-7f49-4382-90d6-db7146af2929.png)

[paper](https://arxiv.org/pdf/2104.06404.pdf)

## TL;DR
- **task :** instance segmentation 
- **problem :** 세그멘테이션 어노테이션 비용 너무 세다! weakly-supervised는 supervised의 85%정도 밖에 성능이 안나온다
- **idea :** point level의 어노테이션을 하자! bbox를 먼저 어노테이션을 하고 그 중에 랜덤 10개의 점을 찍어서 어노테이터가 이게 background인지 object인지 binary 레이블링을 함.
- **architecture :** mask RCNN
- **objective :** 10개의 점에 대해서 나온 prediction에 대해 bi-linear interpolate를 한 뒤  cross entropy loss
- **baseline :** fully supervised mask RCNN
- **data :** ImageNet, COCO
- **result :** ImageNet은 supervised의 97% 정도 성능, COCO는 99% 성능
- **contribution :** 원래 세그멘테이션을 하는데 개당 79초 정도 걸리는데 이 방법론으로는 7초면 어노테이션 가능.
- **limitation or 이해 안되는 부분 :** PointRend model 부분 안 읽음 

## Details
![image](https://user-images.githubusercontent.com/46675408/191144175-80c0c22a-f799-4c9a-9174-bcc0dacadcd0.png)

![image](https://user-images.githubusercontent.com/46675408/191144189-5783160c-375c-46e5-8804-203d14cc2eef.png)

- augmentation
보통 사용하는 이미지 어그멘테이션 사용 + 학습 epoch 때마다 10 개중 5개 랜덤샘플링해서 그것만 사용해서 학습.

- dice loss와 IoU의 차이
https://stackoverflow.com/questions/60268728/why-dice-coefficient-and-not-iou-for-segmentation-tasks
![image](https://user-images.githubusercontent.com/46675408/191143910-54752029-a47a-46f6-8bf0-771423ab54ea.png)

segmentation에는 dice, object detection에는 iou쓰는 듯. 딱히 그 이유는 없는듯? 