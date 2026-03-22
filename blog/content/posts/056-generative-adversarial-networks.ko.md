---
title: "[50] Generative Adversarial Networks"
date: 2022-08-13
tags: ['fundamental', 'generative', 're-read', '2014']
paper: "https://arxiv.org/abs/1406.2661"
issue: 56
issueUrl: "https://github.com/long8v/PTIR/issues/56"
---
![image](https://user-images.githubusercontent.com/46675408/184517292-daf88e97-b4ff-49c7-a01b-d92faa5d5635.png)

[paper](https://arxiv.org/abs/1406.2661)

## TL;DR
- **task :** generative model
- **problem :** discriminative 모델들에 비해 generative는 back-prop을 통해 maximum likelihood로 intractable probability를 근사하는게 어려워 성능이 한정적이다. 
- **idea :** discriminator를 도입해서 adversarial 하게 학습하자.
- **architecture :** generator도 MLP discriminator도 MLP
- **objective :** discriminator는 generated 데이터와 실제 데이터를 잘 구분하도록 분류기를 학습, generator는 discriminator가 잘 구분 못하도록 데이터를 만듦. 
- **baseline :** restricted Boltzmann machines(RBM), deep Boltzmann Machines(DBM), deep Belief network(DBN)
- **data :** mnist, Toronto Face Database, CIFAR10
- **result :** Paren window-based log-likelihood estimates 기준 SOTA
- **contribution :** RBM과 달리 markov chain을 사용하지 않고 gradient만으로 학습 가능.
- **limitation or 이해 안되는 부분 :** 4.2. Convergence of Algorithm 1이 이해가 안됨

## Details
[notion](https://long8v.notion.site/GAN-0f05e9a5f3ca4435b27b6405073538c2)
