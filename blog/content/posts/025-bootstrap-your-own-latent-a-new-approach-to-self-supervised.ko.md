---
title: "[23] Bootstrap Your Own Latent: A New Approach to Self-Supervised Learning"
date: 2022-04-25
tags: ['SSL', '2020Q2', 'google', 'DeepMind']
paper: "https://arxiv.org/pdf/2006.07733.pdf"
issue: 25
issueUrl: "https://github.com/long8v/PTIR/issues/25"
---
<img width="1315" alt="image" src="https://user-images.githubusercontent.com/46675408/165007714-be3ba72c-c55f-46d2-99cf-5ca149c3517e.png">

[paper](https://arxiv.org/pdf/2006.07733.pdf), [code](https://github.com/deepmind/deepmind-research/tree/master/byol) 

## Introduction
Bootstrap* Your Own Latent(BYOL)은 online network, target network 두 네트워크가 상호작용하고 서로 학습하도록 설계되었다. 한 이미지를 어그멘테이션 시킨 것을 online network에 넣어서 같은 이미지를 다르게 어그멘테이션 시킨 것을 target network에 넣었을 때의 표현을 나타내도록 학습한다. 동시에 우리는 online 네트워크의 slow-moving average로 target 네트워크를 학습시킨다. 현재 SOTA 모델들은 negative pair를 사용하지만, BYOL은 이 없이 새로운 SOTA를 달성하였다. 
> *bootstrap은 ML용어가 아니라 그 자체의 뜻인 `to improve your situation or become more successful, without help from others or without advantages that others have`로 쓰였다.

<img width="500" alt="image" src="https://user-images.githubusercontent.com/46675408/165009094-da1b237f-2879-4daf-9335-61346bb0520c.png">

- 이전의 연구들은 pseudo-label을 쓰거나, cluster indicies를 쓰거나, handful label을 썼지만, 우리의 연구는 바로 representation을 bootstrap한다. 
- 우리의 연구는 negative pair를 쓰지 않아 이미지 어그멘테이션에 강건하다. 
- #9 같은 방법론들은 이미지와 어그멘트된 이미지들을 같은 이미지로 예측하면서 학습되었는데, representation space에 prediction problem을 주면 representation collapse가 생긴다. 이를 방지하기 뒤해, 같은 이미지를 어그멘트한 것과 다른 이미지를 어그멘트 한것의 차이를 예측하는 방법론을 적용하였으나, 이는 굉장히 많은 negative sample을 제시하여야하는 한계가 있다. 
- negative sample 없이 collapse를 방지하기 위하여, 단순한 해결책은 고정된 랜덤의 네트워크를 우리의 예측을 하기 위한 타겟이 되도록 만드는 것이다. 이러한 방법은 collapse를 방지하긴 하지만, 성능은 낮다. 그러나 놀라운 점은 그냥 random initialized network를 linear evaluation 하는 것은 1.4%의 정확도를 가지지만, fixed random initialized network의 output을 예측하게 하면 18.8%의 정확도를 얻는다. 이 실험이 BYOL의 motivation이 되었다.
- representation(=target network)이 주어졌을 때, 우리는 새로운 online network를 target representation을 예측하도록 학습할 수있다. 그로부터 우리는 이러한 절차를 반복함에 따라 더 높은 퀄리티의 표현을 학습할 수 있고, 더 학습하기 위해 다음의 online network를 새로운 target network로 설정하여 학습할 수 있다. 실제로는 online network의 moving exponential average를 사용하여 bootstrap 절차를 밟았다. 

## BYOL 
<img width="879" alt="image" src="https://user-images.githubusercontent.com/46675408/165012396-ef00bab5-064a-4b98-89e0-55e12284a161.png">
 
- online network는 encoder, projector, predictor로 구성되어 있고 weight \theta를 가지고 있다. 
- target network는 online과 같은 구조를 가지고 있지만, 다른 weight인 \psi를 가지고 있고, online network의 target을 제공하는 역할을 한다. 이때, 파라미터 \psi는 online parameter \theta의 moving average이다. 

<img width="793" alt="image" src="https://user-images.githubusercontent.com/46675408/165014337-6a8913bc-2fb8-4c36-abe3-521db0705175.png">

한 이미지에 대해 어그멘테이션 시킨 \nu, \nu'를 만들고 각각의 네트워크를 태운다. 이후 online의 마지막 prediction의 output을 target의 projection 결과와 MSE를 구한다. 
<img width="802" alt="image" src="https://user-images.githubusercontent.com/46675408/165014437-5da700e3-c2ea-4d46-a4ae-0805a109bded.png">

이후 다시 online network에 어그멘테이션 된 \nu, \nu' 반대로 넣고, loss를 구한다. 그리고 loss를 합한뒤 \theta에 대해서만 minimize를 한다.  
<img width="1028" alt="image" src="https://user-images.githubusercontent.com/46675408/165014961-53b8bc5f-0484-4bac-a0af-c2854aaed725.png">

## Implementation details
- Image Augmentation
#9 과 같은 augmentation set을 사용. 랜덤 패치로 select 224 x 224 random horizontal flip ...
- Architecture
ResNet-50 for encoder, average pooling for representaion layer, MLP(4096 -> ReLU -> 256) for prediction layer. no batch norm.
- Optimization : LARS, cosine decay, ...

## Result
- linear evaluation in ImageNet
<img width="1012" alt="image" src="https://user-images.githubusercontent.com/46675408/165015701-fceebd10-8615-4393-a66e-ea470835a151.png">

- Finetuning(=Semi-supervised training) in ImageNet
<img width="1038" alt="image" src="https://user-images.githubusercontent.com/46675408/165015748-678b2a8b-7e21-48d1-899f-7a5927ebc51d.png">

- Transfer to other classification task
<img width="1073" alt="image" src="https://user-images.githubusercontent.com/46675408/165015814-1f3070e9-5ec7-4cf7-87ae-d3443fe2c3df.png">

- Transfer to other vision task
<img width="1055" alt="image" src="https://user-images.githubusercontent.com/46675408/165015891-55ef4c91-c591-4bfd-bb89-17547cb61c14.png">

## Ablation
<img width="981" alt="image" src="https://user-images.githubusercontent.com/46675408/165017025-34705ec0-ac1e-4516-9f40-7e2d0b0d7489.png">

simCLR과 비교해봤을 때 batch_size를 줄이고 augmentation을 줄임에 따라 성능 하락이 덜했다. 

<img width="514" alt="image" src="https://user-images.githubusercontent.com/46675408/165017069-2b81d97e-ac95-4eb9-8938-78589078d74e.png">

moving average를 사용하는 것이 의미가 있었다. 

<img width="468" alt="image" src="https://user-images.githubusercontent.com/46675408/165017130-2ed391bf-0fda-4b3c-ac3d-bf96a61351e3.png">

target netork를 두는 것이 의미가 있었다.
