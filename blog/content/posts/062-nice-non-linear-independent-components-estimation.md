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
- Problem :** You want to create a representation that describes important distributions in your data, and a good representation should be easy to model and factorize.
- **idea :** Let's use the change of variable rule to represent the data x by making any transformation h=f(x) the inverse function x=f^(-1)(h).
- **architecture :** split the hidden layer in half, mlp the first half and the second half directly sum with the first half mlped, this transformation is called additive coupling layer and this mlped half is alternated for each layer.
- **objective :** log-likelihood 
- **baseline :** Deep MFA, GRBM
- **data :** MNIST, Toronto Face Dataset(TFD), Street View House Numbers dataset(SVHN), CIFAR-10
- **result :** high likelihood. h sample and put it into the inverse function, it is generated.
- **contribution :** As a pioneering work among flow based models
- **Limitations or things I don't understand :**

## Details
[notion](https://long8v.notion.site/nice-f9a36980ad1449dfb781cc453b22063d)