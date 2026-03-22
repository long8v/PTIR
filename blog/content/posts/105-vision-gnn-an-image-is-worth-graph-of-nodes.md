---
title: "Vision GNN: An Image is Worth Graph of Nodes"
date: 2023-01-05
tags: ['backbone', '2022Q1', 'NeurIPS', 'graph']
paper: "https://arxiv.org/pdf/2206.00272.pdf"
issue: 105
issueUrl: "https://github.com/long8v/PTIR/issues/105"
summary: "NeurIPS2023 — first gnn model for image representation"
---
<img width="1099" alt="image" src="https://user-images.githubusercontent.com/46675408/210682025-b056eb18-00e1-4259-ba5b-3cf8024b31e3.png">


[paper](https://arxiv.org/pdf/2206.00272.pdf), [code](https://github.com/huawei-noah/Efficient-AI-Backbones)

## TL;DR
- **I read this because.. :** NeurIPS2023
- **task :** image classification, object detection 
- **problem :** CNN has a sliding window and ViT cuts image patches and puts them in sequentially, but I want something more fluid.
- **idea :** Cut the image patch and view it as a node and use GNN
- **architecture :** multi-head max relative GCN + linear + BN + relu + linear + BN + FFN stacked in multiple layers.
- **baseline :** ResNet, CycleMLP, Swin-T
- **data :** ImageNet ILSVRC 2012, COCO2017
- **RESULT :** SOTA with similar flops compared to the TINY model.
- **contribution :** first gnn model for image representation 
- **limitation/things I cannot understand :** I'm not sure what's good about it compared to ViT ;; Anyway, cutting it into patch is the same and entering it sequentially, but connectivity can be done with SA.. khmmm.

## Details
### motivation
<img width="700" alt="image" src="https://user-images.githubusercontent.com/46675408/210679374-e9d82a1c-0067-4495-914d-fa381c6a2694.png">

### Preliminaries 
- GNN in general
https://github.com/long8v/PTIR/issues/55

- over-smoothing problem
Node embeddings become more similar as layers get deeper
<img width="300" alt="image" src="https://user-images.githubusercontent.com/46675408/210680797-6b7c216c-3ec8-4f93-add4-3230676ec9ce.png">

https://ydy8989.github.io/2021-03-03-GAT/


### Architecture
#### Graph Structure of Image
Divide $H \times W \times 3$ into $N$ patches.
Represent each patch as a feature vector $\mathrm{x}_i \in \mathbb{R}^D$ to get $X=[\mathrm{x}_1, \mathrm{x}_2, ... \mathrm{x}_N]$.
This feature can be represented as an unordered node $\mathcal{V}={v_1, v_2, ... v_N}$.
For each node $v_i$, find the K nearest neighbors $\mathcal{N}(\mathcal{v}_i)$ and add an edge $e_ij$.
Then we get the graph $\mathcal{G}=(\mathcal{V},\mathcal{E})$, which we can pass through the GNN!
We will write the graph construction $\mathcal{G}=G(X)$.

- Advantages of representing with Graph
1) A graph is a very generalized representation of structure! A grid in CNN or a sequence in ViT can be seen as a specific kind of graph.
2) Graphs may have advantages over grids and sequences for representing complex objects with variable shapes
3) objects can be viewed as a combination of parts (head torso arms legs in the case of a person), so they may have more strength in combining these parts
4) Leverage the latest GNN architecture

#### Graph-level processing
<img width="800" alt="image" src="https://user-images.githubusercontent.com/46675408/210681975-18b87ece-2a46-4a2f-876c-7fb9a5809575.png">

Starting with feature $X \in \mathbb{R}^{n\times D}$, pick a graph based feature $\mathcal{G}=G(X)$.
Graph convolutional layer exchanges information while aggregating features between neighboring nodes
<img width="310" alt="image" src="https://user-images.githubusercontent.com/46675408/210683410-b7352cb4-f4ce-49e2-9e2e-812811a7c51d.png">

A more specific way to write this is to aggregate the neighbor information for node $x_i$ to create $x_i'$.
We will use max-relative graph convolution
<img width="500" alt="image" src="https://user-images.githubusercontent.com/46675408/210683965-f1c0e4ed-948e-480b-89dd-16c6a84c07b2.png">

When aggregating, take the max of the difference between features to aggregate

Trying to write multi-head operation here. Introduced because of feature diversity.
<img width="500" alt="image" src="https://user-images.githubusercontent.com/46675408/210683997-fb610ba7-39ed-4b60-ac38-3f3249c30ba5.png">

#### ViG block
In the case of the previous GC, the differences between node features were lost as the graph convolution layer repeatedly progressed, resulting in performance degradation.
<img width="300" alt="image" src="https://user-images.githubusercontent.com/46675408/210684153-86e386f4-c194-4daa-8c44-ea6895b247b4.png">

So the ViG block wants to add more feature transformation and nonlinear activation.
Put linear layer after GCN layer and also put nonlinear activation. + FFN also added
<img width="458" alt="image" src="https://user-images.githubusercontent.com/46675408/210684360-680debe1-04c4-4fc3-93f4-74cb5263855d.png">
<img width="288" alt="image" src="https://user-images.githubusercontent.com/46675408/210684375-5294eed7-1c6e-4352-89f1-b53cd20e1b3e.png">

This resulted in better diversity than ResGCN. (figure 3 above)

### Network Architecture
#### Isotropic architecture
Models like ViT or ResMLP where features are all the same size
<img width="728" alt="image" src="https://user-images.githubusercontent.com/46675408/210685336-bda52b8a-b1ae-4a22-bddf-68460887071c.png">

#### Pyamid architecture
Features are getting smaller and smaller, like ResNet and PVT.

<img width="729" alt="image" src="https://user-images.githubusercontent.com/46675408/210685357-16d3d959-7c0d-4bcc-b82e-bd716926fa3f.png">

#### PE

<img width="153" alt="image" src="https://user-images.githubusercontent.com/46675408/210685406-67662806-49a2-4afa-afff-169eeda7ba7b.png">
absolute pe plus

### Result
#### Experiment detail
<img width="589" alt="image" src="https://user-images.githubusercontent.com/46675408/210685069-c8b21e02-f358-49f8-a0ad-d5e2fbe70149.png">

#### Result for isotropic
<img width="1024" alt="image" src="https://user-images.githubusercontent.com/46675408/210685144-3ed42751-6fcb-459c-b284-4762425cf1b6.png">

#### Result for Pyramid
<img width="807" alt="image" src="https://user-images.githubusercontent.com/46675408/210685202-2c1012f7-a2b2-4dd3-a6a6-ddc46843ccf2.png">

#### Object Detection result

<img width="728" alt="image" src="https://user-images.githubusercontent.com/46675408/210685561-3765fa9f-1a18-48ab-a6c6-9145fbaf741c.png">

### visualization
<img width="739" alt="image" src="https://user-images.githubusercontent.com/46675408/210685474-7d0b1eb7-ce50-4e00-8f0d-3a74dbe7ae63.png">


### etc


- max relative graph convolution

DeepGCNs: Can GCNs Go as Deep as CNNs? Suggested by https://arxiv.org/pdf/1904.03751.pdf
Similar to ResNet, but most GCN models were 4 layers or less due to the over-smoothing above.
To address this, we wrote a paper on How do I deepen my GCN?
1) residual / dense connection 
<img width="506" alt="image" src="https://user-images.githubusercontent.com/46675408/211227213-99e1b5e6-16a7-4aed-bd61-505d56f78b73.png">

2) dilation
<img width="501" alt="image" src="https://user-images.githubusercontent.com/46675408/211227225-1b31b571-edbb-4405-ac54-ea8732038099.png">
