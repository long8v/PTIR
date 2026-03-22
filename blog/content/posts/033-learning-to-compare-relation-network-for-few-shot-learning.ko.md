---
title: "[28] Learning to Compare: Relation Network for Few-Shot Learning"
date: 2022-05-31
tags: ['few-shot', 'zero-shot', '2018', 'CVPR']
paper: "https://arxiv.org/abs/1711.06025"
issue: 33
issueUrl: "https://github.com/long8v/PTIR/issues/33"
---
<img width="978" alt="image" src="https://user-images.githubusercontent.com/46675408/171096866-65d5c5be-d072-409d-b10b-093b197463f6.png">

[paper](https://arxiv.org/abs/1711.06025)

## TL;DR
**problem :** 이미지 분류 태스크에서, 새로운 class에 대해 데이터가 몇개 없어도 fiene-tuning 없이 성능이 잘나왔으면 한다.(few-shot classification)
**solution :** 1) training 시, C개의 클래스를 support set으로 두고 나머지 클래스를 query set으로 두어 트레이닝 하는 episode training 적용 2) 이미지에서 feature를 뽑는 encoder와 이를 뽑힌 query와 support combine하고 두 벡터가 관련 있는지를 예측하는(0~1) relation 모듈을 학습 3) loss는 두 query - support set이 같은 class로 부터 나오면 1, 아니면 0과 relation간의 MSE로 학습됨. 
**result :** few-shot / zero-shot에 대해 unified, simple, effective한 아키텍쳐이면서 few-shot 성능도 개선.

## Details

### episode training
<img width="483" alt="image" src="https://user-images.githubusercontent.com/46675408/171098141-376f8642-9334-466c-be13-168441829812.png">

### model architecture
<img width="816" alt="image" src="https://user-images.githubusercontent.com/46675408/171097841-9eea444b-75b9-46e1-b0ef-1f616b248d92.png">

<img width="358" alt="image" src="https://user-images.githubusercontent.com/46675408/171098808-95196aed-8e5d-4090-8c75-f2fd540e2e5d.png">

<img width="280" alt="image" src="https://user-images.githubusercontent.com/46675408/171098824-9655bde9-c531-4b44-b040-043780e39555.png">

### zero-shot learning
해당 class C에 대한 벡터가 1개 주어진다는 점에서 one-shot과 비슷하지만, one-shot과 달리 support set이 이미지가 아니라 semantic class embedding이 주어진다.(e.g. CUB 데이터의 경우 textual 정보) 즉 zero-shot의 경우에도 똑같이 support set에 대해 별도의 modality를 다루도록만 변경하면 ZSL에도 적용이 가능하다. 

### why effective? 
이전 연구들에서는 feature만 학습하고 metric은 euclidean이나 cosine으로 고정되어 있어서 효과적이지 못했던 것 같다. 

### result


