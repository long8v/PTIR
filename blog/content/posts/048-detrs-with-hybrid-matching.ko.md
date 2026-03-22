---
title: "[42] DETRs with Hybrid Matching"
date: 2022-08-01
tags: ['object detection', '2022Q3', '25min', 'DETR']
paper: "https://arxiv.org/pdf/2207.13080.pdf"
issue: 48
issueUrl: "https://github.com/long8v/PTIR/issues/48"
---
![image](https://user-images.githubusercontent.com/46675408/182053331-52075198-7268-4eb9-9f2b-b4bffae820f3.png)

[paper](https://arxiv.org/pdf/2207.13080.pdf), [code](https://github.com/HDETR)

## TL;DR
- **task :** object detection, pose estimation, object tracking, label assignment
- **problem :** DETR에서 hungarian one-to-one matching을 하는 부분 때문에(그 덕에 NMS 같은걸 안해도 되었지만), positive pair가 너무 없어 학습이 효율적이지 못함.
- **idea :** hybrid matching. one-to-one matching 하나 하고, one-to-many matching(그냥 gt 여러번 복사하면 됨)도 함. 이걸 auxilary loss처럼 모든 레이어에 대해서 함.
- **architecture :** deformable DETR 
- **objective :** 각 task에 맞는 목적 함수
- **baseline :** deformable DETR, PETR, 3DETR...
- **data :** ...
- **result :** 성능 gain. 학습 속도는 one-to-one matching을 할때 1epoch에 65분 정도 였다면 hybrid matching을 하면 85분
- **contribution :** 간단한 trick으로 성능 개선.

## Details
### hybrid matching을 하는 다양한 방법들
![image](https://user-images.githubusercontent.com/46675408/182053840-433d8bdf-3ca3-45f1-b06d-f8c1b2e5c267.png)

### Results
![image](https://user-images.githubusercontent.com/46675408/182053914-072ce5da-ffbf-4656-9321-b492fd56b9ab.png)

![image](https://user-images.githubusercontent.com/46675408/182053941-8988aab6-e68d-45fd-b5b0-20bbac4c7bf2.png)

### related works 
[Group DETR: Fast Training Convergence with Decoupled One-to-Many Label Assignment](https://arxiv.org/pdf/2207.13085.pdf)
![image](https://user-images.githubusercontent.com/46675408/182054024-ba0dac94-7829-49a6-be48-d3df08f4d5cf.png)

query embedding들 넣을 때, K개의 그룹을 나누고 그 그룹 내에서만 query들이 interaction 할 수 있음.
