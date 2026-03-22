---
title: "[94] Recipe for a General, Powerful, Scalable Graph Transformer"
date: 2023-01-03
tags: ['long', 'NeurIPS', 'graph', '25min', 'transformer']
paper: "https://arxiv.org/pdf/2205.12454.pdf"
issue: 103
issueUrl: "https://github.com/long8v/PTIR/issues/103"
---

<img width="572" alt="image" src="https://user-images.githubusercontent.com/46675408/210287030-20596ed6-f959-4411-8e45-266debe5090e.png">

[paper](https://arxiv.org/pdf/2205.12454.pdf)

## TL;DR
- **I read this because.. :** NeurIPS 2023
- **task :** graph representation 
- **problem :** message passing 접근론들(MPNN)은 NLP의 long-term dependency와 비슷한 문제인 over-smoothing, over-squashing 문제가 있음. transformer를 graph에 바로 넣으면 global attention을 하기에 node 들이 많아질 경우 연산량이 quadratic. 
- **idea :** MPNN + Transformer, 기존에 있었던 Positional Embedding과 Structural Embedding을 정리하고 각각이 MPNN에 얼마나 영향을 미치는지 봄.
- **architecture :** global attention + MPNN 한다
- **baseline :** GCN, GAT, SAN, Graphormer, ... 
- **data :** ZINC, PATTERN, CLIST, MNIST, CIFAR10, .... 
- **evaluation :** MAE, Accuracy, ...
- **result :** benchmark 중 몇개 sota, 준수한 성적

<img width="876" alt="image" src="https://user-images.githubusercontent.com/46675408/210287417-f1bb1927-c40b-4086-acdd-2b9f261371fc.png">

## Details
### Related work 
first fully transformer graph netowrk
https://arxiv.org/pdf/2012.09699.pdf

### Positional Encoding(PE)
- local
node cluster 내에서의 position을 아는 것. 
- global 
graph 내에서의 position을 아는 것
- relative
노드 pair 끼리의 상대적인 거리를 아는 것.

### Structural Encoding(SE)
graph나 subgraph의 구조를 임베딩해서 GNN의 표현력과 일반화를 늘리려는 목표
<img width="587" alt="image" src="https://user-images.githubusercontent.com/46675408/210287407-833f7c09-d0eb-43b4-83fb-ef00cb9130ab.png">

### GPS Layer: an MPNN + Transformer Hybrid
<img width="554" alt="image" src="https://user-images.githubusercontent.com/46675408/210287529-da5f9531-57db-42e6-b064-08f0d3b2767a.png">

- $A\in\mathbb{R}^{N\times N}$ : adjacency matric of a graph with N nodes and E edges
- $X^l\in \mathbb{R}^{N\times d_l}$ : $d_l$ 차원의 node feature
- $E^l\in \mathbb{R}^{N\times d_l}$ : $d_l$ 차원의 edge feature


### Result
<img width="886" alt="image" src="https://user-images.githubusercontent.com/46675408/210287759-c3e9557d-911a-4eed-80a8-a89e21b23125.png">

<img width="878" alt="image" src="https://user-images.githubusercontent.com/46675408/210287766-4b6461b4-494f-4ea6-8e4e-930db8f16524.png">

### Ablation
<img width="890" alt="image" src="https://user-images.githubusercontent.com/46675408/210287747-8b5b016f-322f-4a59-9da6-8773201cbaa9.png">
