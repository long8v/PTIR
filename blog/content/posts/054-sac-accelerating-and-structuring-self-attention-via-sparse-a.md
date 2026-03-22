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
- **problem :** $O(n^2)$ of self-attention operations are inefficient
- **IDEA :** Graph the input sequence and perform attention operations only on the connected nodes.
- **architecture :** LSTM to predict target edge given source node, then perform self-attention only on connected edges
- **objective :** Apply a policy gradient that rewards performance after self-attention when training edges because the ground truth edges are unknown. For self-attention, use a loss that is specific to each task.
- **baseline :** Transformer, [Sparse Graph Attention Networks](https://arxiv.org/abs/1912.00552), Reformer 
- **data :** newstest2013(WMT), Enwiki8/Text8(LM), CIFAR100/ImageNet(Image Classification)
- **result :** Performance comparable to SOTA. Very low memory cost.
- **contribution :** Replacing quadratic with graph in the transformer.
- Limitations or things I don't understand :** Learning seems to be really tricky. Wouldn't LSTM introduce a lot of latency when predicting edges?

## Details
![image](https://user-images.githubusercontent.com/46675408/183548622-be1eebe9-5400-4c79-bc03-d09d78f36310.png)

![image](https://user-images.githubusercontent.com/46675408/183548716-4e911f41-ac0b-4848-9713-9fbb6f9daeb2.png)

