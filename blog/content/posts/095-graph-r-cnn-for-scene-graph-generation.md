---
title: "[86] Graph R-CNN for Scene Graph Generation"
date: 2022-12-06
tags: ['2018', 'SGG', 'graph', 'two-stage']
paper: "https://arxiv.org/pdf/1808.00191.pdf"
issue: 95
issueUrl: "https://github.com/long8v/PTIR/issues/95"
summary: "Early SGG paper - probably the first paper to apply GCN?"
---
<img width="1056" alt="image" src="https://user-images.githubusercontent.com/46675408/205799708-bcd96d1e-3ed7-4f90-bc14-f2dd79973af6.png">

[paper](https://arxiv.org/pdf/1808.00191.pdf)

## TL;DR
- **I read this because.. :** SGG Early Papers
- **task :** Scene Graph Generation
- **problem :** Pick an object and handle quadratic relations well. Create an enhanced graph representation.
- **idea :** Put a module in the middle that prunes the relation between objects. apply an attentive GCN.
- **architecture :** 1) Extract object with Faster RCNN 2) concat object cls logit values to prune relation 3) apply attentive GCN to enrich the representation of object, relation node -> attach classifier to each subject, object, relation representation as predicted?
- **objective :** 1) bbox loss + cls loss 2) bce for relationship score 3) ce for object cls and predicate cls
- **baseline :** IMP, MSDN, NeuralMotif
- **data :** Visual Genome
- **evaluation :** PredCls, PhrCls, SGGen, SGGen+(proposed in this paper)
- **result :** SOTA
- **contribution :** Probably the first paper to apply GCN?
- **limitation/things I can't understand :** Does SGG really have such graphical characteristics that I should write GCN?

## Details
### Architecture
<img width="726" alt="image" src="https://user-images.githubusercontent.com/46675408/205802104-66ce1c38-3030-47bf-87d1-cfdddd0f6020.png">

<img width="705" alt="image" src="https://user-images.githubusercontent.com/46675408/205802166-8aa08cd2-9f4b-45e9-acf8-e74dc42ce967.png">

<img width="511" alt="image" src="https://user-images.githubusercontent.com/46675408/205802198-6ba1f40c-bf06-4bfc-82d7-f7ffac9a239b.png">

Break it down into 3 steps
1) Object Region Proposal : Select nodes(=vertex, V) when given an image => Faster RCNN
2) Relationship Proposal : Given an image and a node, prune the relation that exists in all cases n*(n-1)
3) Graph Labeling: Finding relation and object given image, node, and edge

### Relation Proposal Network
Measure "relatedness" using the object's class logit.
Give some sort of soft prior (e.g., can't be `person-ride-chicken`?)
<img width="340" alt="image" src="https://user-images.githubusercontent.com/46675408/205803827-2ff062c8-64cc-4c67-bc69-6fda5590f5ea.png">

The implementation catches and then stacks MLPs.
After scoring and sorting, we pick out K pairs. Since it is a faster RCNN, there will be a lot of pairs, so we do NMS on the pairs to keep only the top m pairs.
<img width="393" alt="image" src="https://user-images.githubusercontent.com/46675408/205804138-8bc7d66c-d60a-46ad-9998-63ffa774bd71.png">

### Attentional GCN
Vanilla GCN looks like this
<img width="365" alt="image" src="https://user-images.githubusercontent.com/46675408/205804181-63170107-bbd5-48fa-922a-8cad9ef9120c.png">

- $z_i$ : Representation of the i-th node
- $N(i)$ : neighbors of the ith node
- $\alpha_{ij}$: connection coefficient created by the adjacency matrix of i and j

If we express this as a matrix called $Z\in \mathbb{R}^{d\times T_n}$, then we get
<img width="248" alt="image" src="https://user-images.githubusercontent.com/46675408/205804619-62933a91-375b-4396-985c-05c4e291a544.png">

We are trying to learn $\alpha_{ij}$ here, not given it
<img width="260" alt="image" src="https://user-images.githubusercontent.com/46675408/205804674-d6e1303b-03c1-420d-bf8a-28f9d25b819b.png">

2-layer MLP + softmax to learn $\alpha_{ij}$

#### aGCN for SGG
Create N object regions and m relationships, each with a node, and connect the edges from the network above. Additionally, add direct edges between objects.

The representation for an object node is as follows
<img width="493" alt="image" src="https://user-images.githubusercontent.com/46675408/205804918-14e93b1b-2a12-45f3-b5d7-b2058f1dc136.png">

The representation for a relation node is shown below.
<img width="397" alt="image" src="https://user-images.githubusercontent.com/46675408/205804933-44f7458f-587d-4ac1-b826-38b1b3aeace0.png">

### Result
<img width="731" alt="image" src="https://user-images.githubusercontent.com/46675408/205805119-4eaacf85-68a4-4d93-bee1-335b09239545.png">

<img width="726" alt="image" src="https://user-images.githubusercontent.com/46675408/205805243-b5d40574-f5eb-4fc0-9ef3-528e95dd642d.png">

### Ablation for modules
<img width="719" alt="image" src="https://user-images.githubusercontent.com/46675408/205805201-87bba58c-ced2-4c3b-8b20-eb9aee139674.png">

![image](https://user-images.githubusercontent.com/46675408/205806346-985a43a7-780b-48d3-b8d4-0ef1d1c6c0ee.png)

