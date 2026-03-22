---
title: "[18] Deep Learning with Differential Privacy"
date: 2022-04-04
tags: ['WIP', 'privacy', '2016', 'google']
paper: "https://arxiv.org/pdf/1607.00133.pdf"
issue: 18
issueUrl: "https://github.com/long8v/PTIR/issues/18"
---
![image](https://user-images.githubusercontent.com/46675408/161464669-ac87d975-807f-4f93-b908-a43cb6282391.png)
[paper](https://arxiv.org/pdf/1607.00133.pdf)

**Differential Privacy(DP)**
우리의 실험에서 학습 set은 image-label pair이고, (image, label)이 있을 때, d에 대해서는 특정 pair가 있고 d'에 대해서는 해당 pair가 없을 때, 우리는 d와 d'가 "인접"(adjacent)하다고 한다. 

기본 Differential Privacy의 아이디어
![image](https://user-images.githubusercontent.com/46675408/161470144-d54f49a4-3112-4cfd-bcdf-55adc62e4b45.png)
특정 데이터가 존재하거나, 하지 않을 때 결과 차이는 크지 않아야(epsilon보다 작아야)한다.

![image](https://user-images.githubusercontent.com/46675408/161466007-0ce3e2a5-6484-47dc-878b-d34a12c06d1e.png)
원래의 정의에서는 마지막 \delta항이 없었으나, \delta의 확률로 \epsilon differential privacy가 깨질수도 있는 항을 추가하였다.

이러한 D -> R로 가는 함수인 f를 정의하기 위해서 일반적인 방법론은 f의 sensitivity에 조정된 noise를 추가하는 것이다. 이대 sensitivity는 |f(d) - f(d')|의 최대값으로 정의된다. 

1) differentially private SGD 2) moments accountant 3) hyper-parameter tuning으로 구성된다.
- **differentially private SGD**
![image](https://user-images.githubusercontent.com/46675408/161468916-7a6c98db-a54d-4390-8144-a511b0b0b05e.png)

- moments accountant


- hyper-parameter tuning


**material**
https://www.youtube.com/watch?v=YHvY4en8XkU 
