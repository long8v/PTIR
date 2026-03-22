---
title: "[89] Relational Attention: Generalizing Transformers for Graph-Structured Tasks"
date: 2022-12-15
tags: ['microsoft', 'graph', '2022Q4', 'transformer']
paper: "https://arxiv.org/abs/2210.05062"
issue: 98
issueUrl: "https://github.com/long8v/PTIR/issues/98"
summary: "I read it because the title seems to be about the concept of extracting relations through attention and his methodology is 'woo' - SOTA"
---
![image](https://user-images.githubusercontent.com/46675408/207773112-434689ed-fdc7-46ac-9dad-b7c326a1f088.png)

[paper](https://arxiv.org/abs/2210.05062)

## TL;DR
- **I read this because.. :** I read it because the title seems to be about the concept of pulling relations through attention and his methodology sounds `wow`.
- **task :** Graph representation
- **problem :** Represent the graph with a transformer. Unlike graphs, transformers take an unordered set as input, and unlike GNNs, they have no relational inductive bias.
- **idea :** Concatenate edge and node to get Q, K, V
- **architecture :** transformer + edge update for neighbor nodes and edges
- **baseline :** Deep Sets, Graph ATtention network, Message Passing Neural Network, Pointer Graph Networks
- **data :** [CLRS-30](https://github.com/deepmind/clrs) This seems to be a benchmark for solving algorithms with graphs.
- **result :** SOTA 
- **limitation/things I cannot understand :** No this access really didn't exist? lol
## Details
### motivation
![image](https://user-images.githubusercontent.com/46675408/207773154-5cf86777-a956-4d90-bdf9-8dfe7fd4b4dd.png)

You can think of a transformer as a model that takes a set, a graph without edges, and represents it.
Add an edge to the transformer

## Previous work
<img width="905" alt="image" src="https://user-images.githubusercontent.com/46675408/208278936-f70e6867-886d-48a9-8950-0b1c07996d70.png">

https://arxiv.org/pdf/2207.02505.pdf

### Graph Neural Networks
notation description.
- A graph G consists of nodes $N$ and edges $\varepsilon$.
- $N$ : consisting of the set of unordered node vectors $n_i\in \mathbb{R}^{d_n}$
- $\varepsilon$ : consists of the set of edge vectors $e_{ij}\in\mathbb{R}^{d_e}$
- At each layer $l$, take a graph $G^l$ and return $G^{l+1}$ with the same structure.
![image](https://user-images.githubusercontent.com/46675408/207775141-b774c047-8c04-40cd-bf0d-0b0c2d91846d.png)
- $\phi$ : update function
- $\oplus$ : aggregation function 
- $L_i$ : neighbors of the i-th node
- The basic GNN is $e_{ij}^{l+1}=e_{ij}^l$ on all edges (i, j)

### Relational Transformer
Elegant and simple... edge node concat and write it as x in qkv projection
![image](https://user-images.githubusercontent.com/46675408/207776464-20f030b7-2c8e-4d09-9e1a-92e6e0904bf9.png)

To simplify the math, we truncate the matrix to look like this
![image](https://user-images.githubusercontent.com/46675408/207776527-b0ddce7a-2829-4903-8c91-b4b013062c8a.png)

To illustrate, here's what it looks like
![image](https://user-images.githubusercontent.com/46675408/207776483-cb536d3a-be79-4b97-a909-5c90dfb662ba.png)

### Edge update 
If we update the edge for all nodes and all edges, the complexity is $O(n^3)$, so we only aggregate message passing for four things: two neighboring nodes, ourselves, and an edge going in the opposite direction.
![image](https://user-images.githubusercontent.com/46675408/207776556-0c7e8083-3c27-4fce-94ec-3761f40f18e1.png)

![image](https://user-images.githubusercontent.com/46675408/207776773-064bce0f-ba93-4dc1-a467-6b32d97a5dde.png)

![image](https://user-images.githubusercontent.com/46675408/207776795-f98c7e71-d1ac-4fec-9a11-dc3320c68750.png)

