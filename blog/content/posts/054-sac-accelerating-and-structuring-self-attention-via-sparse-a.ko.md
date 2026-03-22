---
title: "[48] SAC: Accelerating and Structuring Self-Attention via Sparse Adaptive Connection"
date: 2022-08-09
tags: ['2020Q1', 'long', 'NeurIPS', 'graph', '25min']
paper: "https://proceedings.neurips.cc/paper/2020/file/c5c1bda1194f9423d744e0ef67df94ee-Paper.pdf"
issue: 54
issueUrl: "https://github.com/long8v/PTIR/issues/54"
---
![image](https://user-images.githubusercontent.com/46675408/183547259-871e00a3-5f71-46f8-8153-56b3a8894b4f.png)

[paper](https://proceedings.neurips.cc/paper/2020/file/c5c1bda1194f9423d744e0ef67df94ee-Paper.pdf)

## TL;DR
- **task :** efficient Transformer -> Machine Translation, Language Modeling, Representation leaning in Graph, Image Classification
- **problem :** self-attention 연산의 $O(n^2)$이 비효율적이다
- **idea :** 인풋 시퀀스를 그래프로 보고 attention 연산을 연결된 node에 대해서만 하자
- **architecture :** LSTM을 통해 source node가 주어졌을 때 target edge predicting, 이후 연결된 edge들에 대해서만 self-attention 수행
- **objective :** ground truth edge를 알 수 없기 때문에 edge training을 할 때에는 self-attention 까지 한 후의 성능을 reward로 주는 policy gradient 를 적용. self-attention의 경우 각 task에 맞는 loss.
- **baseline :** Transformer, [Sparse Graph Attention Networks](https://arxiv.org/abs/1912.00552), Reformer 
- **data :** newstest2013(WMT), Enwiki8/Text8(LM), CIFAR100/ImageNet(Image Classification)
- **result :** SOTA와 견줘볼만한 성능. memory cost는 매우 줄임.
- **contribution :** 트랜스포머의 quadratic을 graph로 바꾼 점
- **limitation or 이해 안되는 부분 :** 학습이 엄청 까다로울 것 같다. LSTM에서 edge prediction 할 때 latency가 엄청 생기지 않을까?

## Details
![image](https://user-images.githubusercontent.com/46675408/183548622-be1eebe9-5400-4c79-bc03-d09d78f36310.png)

![image](https://user-images.githubusercontent.com/46675408/183548716-4e911f41-ac0b-4848-9713-9fbb6f9daeb2.png)

