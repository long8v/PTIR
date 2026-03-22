---
title: "[91] Deep Residual Learning for Image Recognition"
date: 2022-12-25
tags: ['fundamental', 'microsoft', '2015']
paper: "https://arxiv.org/abs/1512.03385"
issue: 100
issueUrl: "https://github.com/long8v/PTIR/issues/100"
---
<img width="1203" alt="image" src="https://user-images.githubusercontent.com/46675408/209473234-9800aeb4-2355-44a3-b7b3-12ed70cb235f.png">


[paper](https://arxiv.org/abs/1512.03385)

## TL;DR
- **I read this because.. :** ResNet50과 101의 차이를 모름 ^^
- **task :** image classification, object detection
- **problem :** 레이어가 낮은 네트워크가 있고 거기에 identity mapping만 추가한 깊은 네트워크가 있을 때 사실상 같은 네트워크인데도 불구하고 깊은 네트워크의 training error가 더 높은 현상. 즉 깊을 수록 학습이 불안정하게 최적해를 찾음.
- **idea :** residual connection. f(x) + x를 하자. 이렇게 되면 깊은 레이어가 필요없으면 f(x)=0이 되어서 identity mapping을 하는 것과 같은 역할을 할 것.
- **architecture :** VGG의 원칙을 따라 1) 매 레이어의 필터 개수를 같게 설정 2) feature map크기가 반으로 줄면 filter 개수를 두배로 했지만 필터 개수가 VGG보다 작은 대신 더 깊게 쌓아서 파라미터수나 FLOPS는 VGG보다 낮음.
- **objective :** CE loss for classification, object detection loss
- **baseline :** VGG-16, GoogLeNet, plain(ResNet에 residual connection 뺀거)
- **data :** CIFAR-10, COCO 2015m ILSVRC 2015
- **evaluation :** accuracy, mAP, # params, FLOPS
- **result :** 이미지 분류에서 sota. object detection에서 성능 28% 개선
- **contribution :** residual connection 

## Details
### Motivation
<img width="471" alt="image" src="https://user-images.githubusercontent.com/46675408/209473452-62f3f101-3de2-4a83-bc35-62e0c20a838b.png">

degration이라는 현상. 깊으면 training error가 더 높음. 즉 overfitting이 문제가 아니라 학습 자체가 잘 안된 상황

### Residual learning
<img width="348" alt="image" src="https://user-images.githubusercontent.com/46675408/209473492-edf65025-a834-43e0-90f7-5e9e5e4f925e.png">

residual하는 block은 최소 2개 이상이어야(1개면 그냥 linear하는 효과), 차원도 같아야 함.

### Network architecture
<img width="304" alt="image" src="https://user-images.githubusercontent.com/46675408/209473537-fc6ae797-c38d-4990-94e0-36322f738729.png">

### Network variants
<img width="771" alt="image" src="https://user-images.githubusercontent.com/46675408/209473569-747444a1-644a-4638-9dfc-af37ca50a42b.png">

궁금증 해결 ^^ 101개 레이어 쌓은 것임

### training error on ImageNet
<img width="587" alt="image" src="https://user-images.githubusercontent.com/46675408/209473551-f30f42fb-1798-4d74-a2d2-d6c32e90c9a7.png">

### 기타 
초기 논문들 읽으면 재밌을 듯
- [Neural Networks: Tricks of the Trade](https://link.springer.com/book/10.1007/978-3-642-35289-8) 
-  Understanding the difficulty of training deep feedforward neural networks https://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf