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
In our experiments, the training set is image-label pairs, and we say that d and d′ are "adjacent" when, given (image, label), we have a particular pair for d and no such pair for d′.

The idea behind basic differential privacy
![image](https://user-images.githubusercontent.com/46675408/161470144-d54f49a4-3112-4cfd-bcdf-55adc62e4b45.png)
The difference in results should not be large (less than epsilon) when certain data is present or absent.

![image](https://user-images.githubusercontent.com/46675408/161466007-0ce3e2a5-6484-47dc-878b-d34a12c06d1e.png)
The original definition did not have a final \delta term, but we added one to account for the possibility that \epsilon differential privacy could be broken with a probability of \delta.

To define such a function f from D -> R, a common methodology is to add a scaled noise to f's sensitivity. This sensitivity is defined as the maximum of |f(d) - f(d')|.

It consists of 1) differentially private SGD 2) moments accountant 3) hyper-parameter tuning.
- **differentially private SGD**
![image](https://user-images.githubusercontent.com/46675408/161468916-7a6c98db-a54d-4390-8144-a511b0b0b05e.png)

- moments accountant


- hyper-parameter tuning


**material**
https://www.youtube.com/watch?v=YHvY4en8XkU 
