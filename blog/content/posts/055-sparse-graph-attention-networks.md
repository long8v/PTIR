---
title: "Sparse Graph Attention Networks"
date: 2022-08-10
tags: ['2019', 'graph', 'IEEE']
paper: "https://arxiv.org/pdf/1912.00552.pdf"
issue: 55
issueUrl: "https://github.com/long8v/PTIR/issues/55"
---
![image](https://user-images.githubusercontent.com/46675408/183781983-e394eab8-8fbf-4284-9a7d-65057b404e4b.png)

[paper](https://arxiv.org/pdf/1912.00552.pdf), [code](https://github.com/Yangyeeee/SGAT)

## TL;DR
- **task :** graph representation
- **problem :** There are Graph Attention Network (GAT) models that use attention to represent graphs, but they are hard to generalize because real graphs are very large and noisy.
- **IDEA:** Let's have one attention score across all layers that chooses which edges are important and leave all others at 0.
- **architecture :** GAT, but only one attention score is selected.
- **objective :** cross entropy loss and loss for the number of edges
- **baseline :** GCN, GAT, GraphSage
- **data :** Cora, Citesser, Pubmed, Amazon computer, Amazon Photo, PPI, Reddit
- **result :** Similar performance to GAT. More interpretable because only one is selected per layer.
- **contribution :** Shows that GNNs that spare first perform as well as GNNs that do not.
- **Limitations or things I don't understand :** GNN is transductive, but I'm not sure I understand. How is $z_{ij}$ learned?

## Details
### GNN in general
- Graph $G$ = ( $V$, $E$ ) consists of nodes ( $V$ ) and edges ( $E$ )
- nodes are represented by feature $X$. The dimensionality is $N$ (number of nodes) x $D$ (feature dimension)
- The adjacency matrix $A$ is a matrix that is 1 if it is connected by edges, and 0 otherwise. The dimension is $N$x$N$
What we eventually want to do is take features $X$ and $A$ and create an enriched node representation $H$. A function is usually defined like this
<img width="250" alt="image" src="https://user-images.githubusercontent.com/46675408/183783907-2a8facf7-e3ac-4453-a2b7-9ddb87e70037.png">

- Let $f$ be a function that encodes the graph.
- where loss is the cross entropy loss if you're doing something like a node classification task
- In the end, the question is: how do the different variants of GNN organize $f$?

### Neighbor Aggregation Methods
One of the most efficient methods for graph learning is the neighbor aggregation mechanism, which aggregates feature vectors over feature vector $x_i$ and its neighbors, j.
For example, Graph Convolution Network (GCN) is one of them, and you can write the expression like this
<img width="250" alt="image" src="https://user-images.githubusercontent.com/46675408/183783929-73c5578e-cb51-4e9c-88ac-7b973db5f9ae.png">
<img width="250" alt="image" src="https://user-images.githubusercontent.com/46675408/183783978-23eac389-deb1-4316-84d4-181af489879f.png">

A more generalized version of this would look like this
<img width="250" alt="image" src="https://user-images.githubusercontent.com/46675408/183783810-f8576754-babe-4df3-9d97-7a9fad3220a7.png">

However, GCN can only be used transductively, which means that it needs to be retrained when the graph structure changes.

### Graph Attention Networks(GAT)
Similar to GCN, we aggregate neighborhoods, which becomes GAT when we use attention to get an attention score to determine which ege to focus on.
<img width="250" alt="image" src="https://user-images.githubusercontent.com/46675408/183784095-284bff2d-f486-47f5-bb71-0b940bc276bb.png">

However, in this case, the attention score can be viewed as the importance of each edge, which is difficult to interpret because the attention score is different for each layer.
Suggest SGAT to clean up noisy/task-irrelevant edges when creating graphs!

### SparseGAT(SGAT)
To keep only the important edges, we add a binary gate $z_{ij}$ for each ege. This $z_{ij}$ will do binary masking on whether to use edge $e_{ij}$ or not.
<img width="250" alt="image" src="https://user-images.githubusercontent.com/46675408/183784225-7c9dc9be-b704-45df-8920-9757df91cd6b.png">

Add L0 loss to the loss term to leave as few edges as possible. If $z_{ij}$ is 1, then $z_{ij}$ is the term that sums to 1 or 0. (loss over the number of edges)
<img width="400" alt="image" src="https://user-images.githubusercontent.com/46675408/183784260-052aec62-9536-426e-add4-06b1e29cad6e.png">

An attention based aggregation function can be written as follows, which is no different from (GAT)
<img width="250" alt="image" src="https://user-images.githubusercontent.com/46675408/183784276-b0fe0aae-f1d9-481e-ab9f-056299e048ee.png">

We get the attention score as follows
<img width="300" alt="image" src="https://user-images.githubusercontent.com/46675408/183784920-67941571-e9c7-4053-9296-9a8f731c2bda.png">

-> How is $z_{ij}$ learned?

The reason for this sparse configuration is that I tried to get the variance per layer per head for attention score and it was almost zero, as shown below.
<img width="250" alt="image" src="https://user-images.githubusercontent.com/46675408/183785088-26b0760f-25f9-4eca-80db-3118d5fbc495.png">


