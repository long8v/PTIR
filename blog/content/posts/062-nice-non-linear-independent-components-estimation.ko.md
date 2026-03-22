---
title: "[56] NICE: Non-linear Independent Components Estimation"
date: 2022-08-27
tags: ['fundamental', 'generative', '2014']
paper: "https://arxiv.org/pdf/1410.8516.pdf"
issue: 62
issueUrl: "https://github.com/long8v/PTIR/issues/62"
---
![image](https://user-images.githubusercontent.com/46675408/187016042-2d79fe17-3bff-41c4-976f-5edf3288e18f.png)

[paper](https://arxiv.org/pdf/1410.8516.pdf), [code](https://github.com/paultsw/nice_pytorch/)

## TL;DR
- **task :** representation learning / generative model
- **problem :** 데이터의 중요한 분포를 잘 설명하는 representation을 만들고 싶은데, 좋은 representation이란 모델링하기 쉬워야 하고, factorize 가능 해야한다. 
- **idea :** change of variable rule을 사용하여 어떤 transformation h=f(x)를 역함수 x=f^(-1)(h)로 만들어서 데이터 x를 표현해보도록 하자
- **architecture :** hidden layer를 반갈 하고 첫번째 반을 mlp, 나머지 반은 mlp한 첫번째 반과 바로 합, 이런 변환을 additive coupling layer라고 하고 이 mlp 하는 반을 레이어마다 번갈아가면서 함. 
- **objective :** log-likelihood 
- **baseline :** Deep MFA, GRBM
- **data :** MNIST, Toronto Face Dataset(TFD), Street View House Numbers dataset(SVHN), CIFAR-10
- **result :** 높은 likelihood. h 샘플 뽑고 inverse 함수에 넣으면 생성은 됨. 
- **contribution :** flow based model들 중 선행연구인듯
- **limitation or 이해 안되는 부분 :** 

## Details
[notion](https://long8v.notion.site/nice-f9a36980ad1449dfb781cc453b22063d)