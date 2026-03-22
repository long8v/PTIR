---
title: "[122] Neural Architecture Search without Training "
date: 2023-06-28
tags: ['ICML', '2020Q2', 'NAS']
paper: "https://arxiv.org/abs/2006.04647"
issue: 133
issueUrl: "https://github.com/long8v/PTIR/issues/133"
summary: "meta-learning. NAS인데 학습 안하는 거?! Recommended by my supervisor - first performance prediction without learning (?) Almost this is an art form..."
---

<img width="723" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f038beb0-290a-431e-9f65-f804424150cf">

[paper](https://arxiv.org/abs/2006.04647), [code](https://github.com/BayesWatch/nas-without-training)

## TL;DR
- **I read this because.. :** meta-learning. NAS인데 학습 안하는 거?! Recommended by my advisor
- **task :** Neural Architecture Search
- **problem :** It takes too much labor to create a deep learning model, so the NAS to solve it eventually has to learn, which makes search too slow.
- **idea :** Can we predict the final performance with the initialized model without training? -> Create a code book by dividing the regions that are activated in mini batch N samples and create an N x N matrix with hamming distance between the data.
- **input/output :** model -> score(or rank)
- **architecture :** NAS-Bench-201 This seems to be CNN-based after all.
- **baseline :** NAS(REINFORCE, BOHB) based on cell prediction, NAS(RSPS, ...) with weight sharing to reduce search time
- **data :**  NAS-Bench-201, NDS-DARTS
- **evaluation :** performance of CIFAR-10, CIFAR-100, ImageNet-16-120 on best model
- **result :** Predictable performance without training. In 30 seconds in a defined search space for CIFAR-10, it was able to find a child in the NAS-Bench-201 search space with 92.81% accuracy
- **contribution :** Predicting performance without first learning (?) This is almost an art form.
- **etc. :**

## Details
- NAS-BENCH-201 : https://arxiv.org/abs/2001.00326
It seems like a benchmark that completely ignores search space and only measures Rank.
<img width="583" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1e78178f-29d8-4046-9674-dd22e4908889">


- binary activation codes in linear regions
<img width="713" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7c1475c1-4b6e-4fba-a1d7-5b62a68eed34">

- activation 
Visualize activation codes
<img width="736" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/ca0b5f40-8840-472a-a39e-84f049a687f3">

Assumption that the lower the correlation, the better the performance -> in fact, the higher the CIFAR-10 accuracy, the whiter the performance
The intuition here is that
Assuming that kids with similar binary code will have a harder time distinguishing between samples in a more linear way, and conversely, learning will be easier if the input is well differentiated!

<img width="411" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/1b1df1f2-2bf5-43b2-8753-aa50dbba4d7c">

score can be written like this
<img width="266" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/5474b0a6-ac89-4743-ae4d-f25715a61a6e">

## ablation
- Positive correlation between score and post-training accuracy
<img width="722" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/30b785f9-9893-4353-b21d-fb142838da38">

- Comparison with other measures. High rank correlation coefficient.
<img width="745" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b514a53a-17d5-48e0-bd4a-a1b42cb5f594">

- 1) sample image 2) initialization method 3) verify that ordinal remains the same regardless of bs
<img width="298" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/2a29d71e-a61e-4599-ac5d-97a7c7d5a47c">

- Verify that rank is maintained while learning
<img width="348" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d94313ab-47aa-434e-8688-a847b18df422">

- With the above score, a NAS with ?
<img width="326" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/42bfa852-950a-43d0-a0f8-9bfa829aeab2">

- Final performance: not SOTA, the search time is very small!
<img width="726" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/27d92a46-65db-47ea-b9e6-e6942dd15f1e">
