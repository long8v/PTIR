---
title: "[81] Equalization Loss for Long-Tailed Object Recognition"
date: 2022-11-22
tags: ['2020Q1', 'object detection', 'SenseTime', 'imbalance']
paper: "https://arxiv.org/pdf/2003.05176.pdf"
issue: 90
issueUrl: "https://github.com/long8v/PTIR/issues/90"
---
<img width="697" alt="image" src="https://user-images.githubusercontent.com/46675408/203190570-22561a0c-3712-460e-8c9f-d4356b9482ca.png">

[paper](https://arxiv.org/pdf/2003.05176.pdf), [code](https://github.com/tztztztztz/eql.detectron2) 

## TL;DR
- **task :** long-tail object recognition
- **problem :** 이전의 연구들은 foreground - background에만 집중했고 foreground 내의 class imbalance에 대해 다루지 않았다! sigmoid, softmax 든 rare한 class들은 frequent한 class의 negative sample로 인해 gradient에 영향을 받는다.
- **idea :** sigmoid / softmax의 $log(p_j)$ term 앞에 frequency 기반의 weight를 주자.
- **architecture :** ResNet-50 Mask R-CNN
- **objective :** equalization loss(proposed in this paper)
- **baseline :** sigmoid, softmax, class-aware sampling, class balanced loss, focal loss 
- **data :** LVIS v0.5, CIFAR-100-LT, ImageNet-LT
- **result :** baseline 대비 AP, AP50의 전체적인 성능 향상. rare, frequent에 대한 성능은 베이스라인 대비 떨어지고 common의 성능이 매우 좋음.
- **contribution :** 아마 foreground 내 class imbalance를 다룬 첫 논문인듯?

## Details
### Motivation
![image](https://user-images.githubusercontent.com/46675408/203194015-52368b45-41a5-4171-b7a4-3a9e87f9c3fb.png)

오른쪽으로 갈수록 rare한 클래스인데 negative sample의 gradient가 positive 보다 높아지는 영향이 있음

### Equalization Loss Formulation
![image](https://user-images.githubusercontent.com/46675408/203194122-c763aaaa-23ec-4dcb-bd47-e3a6ac1f24ca.png)

![image](https://user-images.githubusercontent.com/46675408/203194165-9a09a42c-15be-40c3-8f46-80e3c5a9b8e3.png)

- $E(r)$ : foreground면 1 아니면 0
- $f_j$ : class j의 frequency
- $T_\lambda$ : $x < \lambda$면 0 아니면 1인 tresholding 

이때 $\lambda$는 아래의 Tail Ratio(TR)을 보고 고름 => 절대적으로 크면 좋고 낮으면 좋고는 아니고 그냥 값에 따라 frequent <=> rare 성능이 달라짐.
![image](https://user-images.githubusercontent.com/46675408/203194213-25f04ee2-93f8-4493-98f8-3d7192939f3c.png)

### Softmax Equalization Loss Formulation
![image](https://user-images.githubusercontent.com/46675408/203195125-46b56296-64a5-4ee7-b39e-248851c9d7ff.png)
![image](https://user-images.githubusercontent.com/46675408/203195170-3fe75245-eaf5-4158-bd70-a8a16e23e146.png)
- weight를 분모에만 곱해주넹

![image](https://user-images.githubusercontent.com/46675408/203195201-3fb45f04-5aea-4265-89f2-2a38a279e95c.png)

- $\beta$ : $\gamma$의 확률로 1이 되고 $1-\gamma$의 확률로 0이 되는 랜덤변수

### Result
![image](https://user-images.githubusercontent.com/46675408/203195414-b56c2cea-2ca3-4936-b558-1e19679fe395.png)

추가하면 성능은 전체적으로 다 좋아짐!

![image](https://user-images.githubusercontent.com/46675408/203195563-dc753038-602c-4838-b42a-c814425d738e.png)

다른 Long-tail Loss와 비교했을 때는 전체적으로 좋아지지만 rare, frequent에 대해서는 sampling 방법보다는 안좋음
Focal 보다는 확실히 좋음!

### Ablation
![image](https://user-images.githubusercontent.com/46675408/203195493-a2b4ccf4-4747-4737-b83c-00b32c98c0c2.png)
tail ratio가 높아지면 frequent한 Class에 대해 잘하고 rare는 점점 떨어지는 모습 -> $\lambda$가 완전 하이퍼파라미터임

![image](https://user-images.githubusercontent.com/46675408/203196236-f37fb0d5-8d48-4850-9482-6cd3ac3a8b35.png)

background이면 1로 바꿔주는 E(r)에 대한 ablation. rare가 안좋아지넹