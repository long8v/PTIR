---
title: "[94] Recipe for a General, Powerful, Scalable Graph Transformer"
date: 2023-01-03
tags: ['long', 'NeurIPS', 'graph', '25min', 'transformer']
paper: "https://arxiv.org/pdf/2205.12454.pdf"
issue: 103
issueUrl: "https://github.com/long8v/PTIR/issues/103"
summary: "NeurIPS 2023 - Several of the benchmarks sota, compliant grades"
---

<img width="572" alt="image" src="https://user-images.githubusercontent.com/46675408/210287030-20596ed6-f959-4411-8e45-266debe5090e.png">

[paper](https://arxiv.org/pdf/2205.12454.pdf)

## TL;DR
- **I read this because.. :** NeurIPS 2023
- **task :** graph representation 
- **problem :** message passing approaches (MPNN) suffer from over-smoothing and over-squashing, a problem similar to long-term dependency in NLP. Putting the transformer directly into the graph can lead to quadratic computation when there are too many nodes for global attention.
- Idea :** MPNN + Transformer, clean up the existing Positional Embedding and Structural Embedding and see how each affects MPNN.
- **architecture :** global attention + MPNN does
- **baseline :** GCN, GAT, SAN, Graphormer, ... 
- **data :** ZINC, PATTERN, CLIST, MNIST, CIFAR10, .... 
- **evaluation :** MAE, Accuracy, ...
- **result :** Several of the benchmarks SOTA, compliant grades

<img width="876" alt="image" src="https://user-images.githubusercontent.com/46675408/210287417-f1bb1927-c40b-4086-acdd-2b9f261371fc.png">

## Details
### Related work 
first fully transformer graph netowrk
https://arxiv.org/pdf/2012.09699.pdf

### Positional Encoding(PE)
- local
Knowing your position in the node cluster.
- global 
Knowing your position in the graph
- relative
Knowing the relative distance between a pair of nodes.

### Structural Encoding(SE)
Aiming to increase the expressiveness and generalization of GNNs by embedding the structure of graphs or subgraphs
<img width="587" alt="image" src="https://user-images.githubusercontent.com/46675408/210287407-833f7c09-d0eb-43b4-83fb-ef00cb9130ab.png">

### GPS Layer: an MPNN + Transformer Hybrid
<img width="554" alt="image" src="https://user-images.githubusercontent.com/46675408/210287529-da5f9531-57db-42e6-b064-08f0d3b2767a.png">

- $A\in\mathbb{R}^{N\times N}$ : adjacency matric of a graph with N nodes and E edges
- X^l\in \mathbb{R}^{N\times d_l}$ : $d_l$ dimensional node feature
- Edge feature in $E^l\in \mathbb{R}^{N\times d_l}$ : $d_l$ dimensions


### Result
<img width="886" alt="image" src="https://user-images.githubusercontent.com/46675408/210287759-c3e9557d-911a-4eed-80a8-a89e21b23125.png">

<img width="878" alt="image" src="https://user-images.githubusercontent.com/46675408/210287766-4b6461b4-494f-4ea6-8e4e-930db8f16524.png">

### Ablation
<img width="890" alt="image" src="https://user-images.githubusercontent.com/46675408/210287747-8b5b016f-322f-4a59-9da6-8773201cbaa9.png">
