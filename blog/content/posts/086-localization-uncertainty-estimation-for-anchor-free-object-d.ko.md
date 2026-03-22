---
title: "[78] Localization Uncertainty Estimation for Anchor-Free Object Detection"
date: 2022-11-10
tags: ['2020Q2', '25min', 'uncertainty']
paper: "https://arxiv.org/pdf/2006.15607.pdf"
issue: 86
issueUrl: "https://github.com/long8v/PTIR/issues/86"
---
<img width="1148" alt="image" src="https://user-images.githubusercontent.com/46675408/200983113-09230531-3a80-444c-9142-76109a20af6a.png">

[paper](https://arxiv.org/pdf/2006.15607.pdf)

## TL;DR
- **task :** uncertainty in FCOS model
- **problem :** left, right, top, bottom 4 방향에 대한 uncertainty를 얻고 싶다.
- **idea :** 4개의 가우시안을 가정하자
- **architecture :** FCOS + uncertainty branch + classification head에 uncertainty branch의 output을 fusion
- **objective :** uncertainty loss : 4개의 가우시안에 대한 KL divergence에 IoU term을 지수항으로 넣어줌. cls loss : uncertainty를 반영한 focal loss
- **baseline :** centerness-branch, IoU branch, QFL, VFL 
- **data :**  COCO2017
- **result :** FCOS 성능 1.8 point 올림

## Details
### Related work 
- generalized focal loss 
https://arxiv.org/pdf/2006.04388.pdf

<img width="1013" alt="image" src="https://user-images.githubusercontent.com/46675408/200983028-a99fba92-5600-415a-aca6-c6867466542a.png">

- FCOS: Fully Convolutional One-Stage Object Detection
https://arxiv.org/pdf/1904.01355.pdf
이건 나중에 한번 읽어보면 좋을듯 
<img width="709" alt="image" src="https://user-images.githubusercontent.com/46675408/200983295-ff762c7f-3f6a-419a-816d-12e7dcb70cb3.png">

### Architecture
<img width="518" alt="image" src="https://user-images.githubusercontent.com/46675408/200990473-dc0d2aa1-6209-4289-a410-babb310b12b4.png">

### Loss

#### Uncertainty Loss 
<img width="376" alt="image" src="https://user-images.githubusercontent.com/46675408/200990247-56c2edb9-7e79-4795-a6a0-2fa4c8874b80.png">


### Uncertainty Focal Loss
<img width="504" alt="image" src="https://user-images.githubusercontent.com/46675408/200990372-6ca0b696-59cd-43ae-94af-e53e2210a42e.png">


### Result 
<img width="529" alt="image" src="https://user-images.githubusercontent.com/46675408/200989846-260e0dda-f53a-44f4-aee0-637391995da2.png">


<img width="501" alt="image" src="https://user-images.githubusercontent.com/46675408/200989832-f3b35884-46cf-4d05-9955-4089b4f09834.png">

<img width="502" alt="image" src="https://user-images.githubusercontent.com/46675408/200990840-0d844838-b1c5-4389-9d49-dcbc91244940.png">
