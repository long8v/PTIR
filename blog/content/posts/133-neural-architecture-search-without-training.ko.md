---
title: "[122] Neural Architecture Search without Training "
date: 2023-06-28
tags: ['ICML', '2020Q2', 'NAS']
paper: "https://arxiv.org/abs/2006.04647"
issue: 133
issueUrl: "https://github.com/long8v/PTIR/issues/133"
---

<img width="723" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f038beb0-290a-431e-9f65-f804424150cf">

[paper](https://arxiv.org/abs/2006.04647), [code](https://github.com/BayesWatch/nas-without-training)

## TL;DR
- **I read this because.. :** meta-learning. NAS인데 학습 안하는 거?! 지도교수한테 추천받음 
- **task :** Neural Architecture Search
- **problem :** 딥러닝 모델 만드는데 공수가 너무 많이 들고 그래서 이를 해결하기 위한 NAS는 결국 학습을 해야해서 search가 너무 느리다. 
- **idea :** 학습을 하지 않고 initialized model을 가지고 최종 성능을 예측할 수 있을까? -> mini batch N개의 sample에서 activation되는 영역을 나누어 code book을 만들고 이걸 데이터간 hamming distance을 통해 N x N Matrix를 만듦. 
- **input/output :** model -> score(or rank)
- **architecture :** NAS-Bench-201 이건 결국 CNN 기반인 것 같긴 하다
- **baseline :** cell 예측 기반 NAS(REINFORCE, BOHB), weight share해서 search 시간 줄인 NAS(RSPS, ...)
- **data :**  NAS-Bench-201, NDS-DARTS
- **evaluation :** best model의 CIFAR-10, CIFAR-100, ImageNet-16-120의 성능 
- **result :** 학습을 안하고 성능 예측 가능. CIFAR-10에 대해서 정해진 search space에서 30초만에 NAS-Bench-201 search space에 있는 것들 중에 92.81%정확도를 가진애를 찾을 수 있었음
- **contribution :** 최초의 학습 안하고 성능 예측 (?) 거의 이건 예술의 영역인데.. 
- **etc. :**

## Details
- NAS-BENCH-201 : https://arxiv.org/abs/2001.00326
search space를 아예 박아놓구 Rank만 측정하도록 한 벤치마크인듯 하다 
<img width="583" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1e78178f-29d8-4046-9674-dd22e4908889">


- linear regions에서 binary activation codes 
<img width="713" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7c1475c1-4b6e-4fba-a1d7-5b62a68eed34">

- activation 
activation code들 시각화 
<img width="736" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ca0b5f40-8840-472a-a39e-84f049a687f3">

correlation이 낮을수록 성능이 좋을 것이다 라는 가정 -> 실제로 CIFAR-10 정확도가 높은 애일 수록 하얌
여기서의 intuition은 이러함 
비슷한 binary code를 가진애들은 sample간 더 linear하게 구분하기 어려울 것이고 반대로 input이 잘 구분이 된다면 학습이 더 쉬울 것이다 라고 가정!

<img width="411" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1b1df1f2-2bf5-43b2-8753-aa50dbba4d7c">

score는 아래과 같이 쓸 수있음 
<img width="266" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5474b0a6-ac89-4743-ae4d-f25715a61a6e">

## ablation
- score와 학습 후 정확도의 positive correlation
<img width="722" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/30b785f9-9893-4353-b21d-fb142838da38">

- 다른 measure들과의 비교. 순위 상관계수가 높다.
<img width="745" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b514a53a-17d5-48e0-bd4a-a1b42cb5f594">

- 1) sample image 2) 초기화 방법 3) bs 와 상관없이 ordinal이 동일하게 유지됨을 확인 
<img width="298" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2a29d71e-a61e-4599-ac5d-97a7c7d5a47c">

- 학습 중에도 rank가 유지됨을 확인
<img width="348" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d94313ab-47aa-434e-8688-a847b18df422">

- 위의 score를 가지고 NAS를 하면 ?
<img width="326" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/42bfa852-950a-43d0-a0f8-9bfa829aeab2">

- 최종 성능 : sota는 아니다. search 시간이 매우 작다! 
<img width="726" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/27d92a46-65db-47ea-b9e6-e6942dd15f1e">
