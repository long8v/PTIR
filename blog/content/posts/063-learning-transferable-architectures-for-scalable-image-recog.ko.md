---
title: "[57] Learning Transferable Architectures for Scalable Image Recognition"
date: 2022-08-30
tags: ['fundamental', '2017', '25min', 'AutoML']
paper: "https://arxiv.org/pdf/1707.07012.pdf"
issue: 63
issueUrl: "https://github.com/long8v/PTIR/issues/63"
---
![image](https://user-images.githubusercontent.com/46675408/187320072-5e79e4d0-4d4a-4151-b620-09b1b5059211.png)

[paper](https://arxiv.org/pdf/1707.07012.pdf)

## TL;DR
- **task :** image classification, object detection
- **problem :** 뉴럴네트워크를 잘 학습하기 위해 아키텍쳐 엔지니어링이 너무 많이 들어간다!
- **idea :** 네트워크 내에서 작은 데이터에 대해 building block을 찾고 큰 데이터에 대해서 이걸 transfer 하도록 하자
- **architecture :** RNN Controller가 이전 2개의 레이어의 output을 받고 어떤 레이어의 output을 받을건지 선택하고, 그 레이어에 어떤 conv를 쌓을지 선택함. 선택을 할 때 이전 기본 NAS 연구에서는 reinforcement learning을 사용했지만, 이 연구에서는 random으로 해도 성능의 하락이 작아서 random serach함.
- **objective :** image classification loss, object detection loss
- **baseline :** hand-crafted SOTA models(DenseNet, Shake-Shake,  MobileNet, ShuffleNet), NAS v3
- **data :** CIFAR-10, ImageNet, COCO
- **result :** 더 작은 계산비용으로 image classification / object detection SOTA. 
- **contribution :** NAS 보다 효율적인 아키텍쳐(random search, CIFAR-10으로 선택한 아키텍쳐로 ImageNet으로 학습)이지만 더 나은 성능 
- **limitation or 이해 안되는 부분 :**

## Details
### NAS
![image](https://user-images.githubusercontent.com/46675408/187321215-b30e13c3-0c9f-497d-8ce9-6e5e2a29a32e.png)

### Controller가 하는 5가지의 prediction
![image](https://user-images.githubusercontent.com/46675408/187323974-271745ed-2ac3-4614-8082-e7abbf04838f.png)

### Controller가 고를 수 있는 레이어들 
![image](https://user-images.githubusercontent.com/46675408/187323378-60e5ab9b-0e72-45fb-9266-35176b9d534e.png)

### Architecture 
![image](https://user-images.githubusercontent.com/46675408/187324010-e749cbcf-b95e-4126-b10a-f5cace7154ba.png)
