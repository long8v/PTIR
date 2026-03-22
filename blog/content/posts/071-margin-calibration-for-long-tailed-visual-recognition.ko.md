---
title: "[65] Margin Calibration for Long-Tailed Visual Recognition"
date: 2022-09-19
tags: ['2021Q4', '25min', 'imbalance', 'ECCV']
paper: "https://arxiv.org/pdf/2112.07225.pdf"
issue: 71
issueUrl: "https://github.com/long8v/PTIR/issues/71"
---
![image](https://user-images.githubusercontent.com/46675408/190935677-3709e24a-25d0-453c-a2b2-f1c70106f44a.png)

[paper](https://arxiv.org/pdf/2112.07225.pdf)

## TL;DR
- **task :** long-tail visual recognition
- **problem :** 학습 시에는 클래스당 데이터 개수가 불균형하고 test시에는 균형인 경우의 문제가 long-tail. 
- **idea :** classifier의 margin이 클래스당 개수가 많은 곳에서 더 커진다. margin을 조정해줄수 있도록 beta를 곱해주고 gamma를 더해준다. 이 과정을 그냥 전체 imbalance 데이터로 학습시킨 다음에 beta와 gamma에 대해서만 다시 학습한다. 
- **architecture :** ResNet32, ResNeXt50, ResNet152, ResNet50
- **objective :** cross entropy loss + loss re-weighting
- **baseline :** softmax, data re-sampling, loss function engineering, decision Boundary Adjustment ... 
- **data :** CIFAR-LT, ImageNet-LT, Places-LT, iNaturalist-LT
- **result :** SOTA!
- **contribution :** 아주 간단한 구현으로 SOTA!
- **limitation or 이해 안되는 부분 :** test시에도 train과 같은 클래스 분포를 가질 때도 성능이 좋아지는지 모르겠음!

## Details
### Related Work
- data re-sampling
head 클래스를 undersampling, tail 클래스를 oversampling
- loss function engineering
클래스별로 loss가 더 균형있게 부과되도록 loss re-weighting. 또는 logit을 조정
- decision boundary adjustment
원래 데이터 분포대로 학습하는 것이 좋은 표현을 만들지만 classifier 부분이 성능의 병목이다는 분석이 있음.
학습은 원래대로 하고 classifier를 조정하는 방법론들, Platt scaling 같은 방법을 쓰는 방법들이 있음.

### Paper details
- margin
![image](https://user-images.githubusercontent.com/46675408/190936476-6f06e81c-6a8f-463d-9270-dab41c0b58be.png)

- margin을 아래와 같이 표현 가능 
![image](https://user-images.githubusercontent.com/46675408/190936484-ce945e4c-18c2-4685-ad13-09fdcdb47c96.png)

- logit은 margin에 대한 식으로 표현 가능 -> n이 커지면 margin이 커지고 logit도 커짐
![image](https://user-images.githubusercontent.com/46675408/190936491-c72aa33c-e351-475c-84d4-6f7f2a26c133.png)

- 제안하는 방법론(MARC)의 pseudo-code
![image](https://user-images.githubusercontent.com/46675408/190936503-749c8090-be4c-4f2d-829a-8f5a37cc5e71.png)

- loss re-weighting도 적용했다고 함
![image](https://user-images.githubusercontent.com/46675408/190936518-3cace0c6-3d2f-417e-84b3-97fc2062b368.png)

- 전체 학습 과정에 대한 pseudo-code
![image](https://user-images.githubusercontent.com/46675408/190936526-a13a49bc-a7f9-4042-a097-908522a33951.png)

### Result 
![image](https://user-images.githubusercontent.com/46675408/190936466-b2e9db11-3a30-4ad1-91cf-66fff7291065.png)
