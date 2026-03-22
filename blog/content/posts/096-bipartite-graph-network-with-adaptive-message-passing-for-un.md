---
title: "[87] Bipartite Graph Network with Adaptive Message Passing for Unbiased Scene Graph Generation"
date: 2022-12-08
tags: ['2021Q4', 'CVPR', 'SGG', 'imbalance']
paper: "https://arxiv.org/abs/2104.00308"
issue: 96
issueUrl: "https://github.com/long8v/PTIR/issues/96"
summary: "There was a significant performance improvement in #75. There was a paper recently published in AAAI with that paper as baseline. - confidence aware? gnn for sgg I'm not familiar with the papers, so I don't know what's the contribution"
---
<img width="902" alt="image" src="https://user-images.githubusercontent.com/46675408/206342606-3fa8f4b6-67a0-4452-a60e-0d49d0b6695d.png">

[paper](https://arxiv.org/abs/2104.00308)

## TL;DR
- **I read this because.. :** #75 had quite a bit of performance improvement. There was a paper in AAAI recently where this was the baseline.
- **task :** two-stage SGG
- **PROBLEM :** SGG data is long-tailed.
- **idea :** confidence-aware bipartite graph neural network proposal. bi-level data resampling strategy.
- architecture :** A combination of relationship confidence estimation (RCE) and confidence-aware message propagation (CMP)
- **objective :** ce loss of predicate and entity, loss for relation confidence estimation(class-specific / overall)
- **baseline :** graph-RCNN, GPS-Net, Motif, ...
- **data :** Visual Genome, Open Images V4/6
- **evaluation :** PredCls, SGCls, SGGen(head, body, tail), OI evaluation 
- **result :** sota. tail score improved a lot.
- **contribution :** confidence aware? gnn for sgg I'm not familiar with the papers, so I don't know what is a contribution
- **limitation / things I cannot understand :** What does confidence do? It looks like you gave loss directly to confidence, but how did you give it? Did you give it like "relatedness" in graph-RCNN?

# Details
## Architecture
<img width="899" alt="image" src="https://user-images.githubusercontent.com/46675408/206344201-b0d99065-3dd0-4007-8b61-f369caff6abf.png">

### Proposal generation network
Select objects with Faster RCNN and create an entity representation $e_i$ from them with visual feature $v_i$, geometric feature $g_i$, and class word embedding feature $w_i$.
<img width="200" alt="image" src="https://user-images.githubusercontent.com/46675408/206344577-8dc6d4be-6509-4c6d-813f-9a2313136d15.png">

The relation representation $r_{i->j}$ is constructed by defecting the entity representations $e_i$, $e_j$. Let $u_i,j$ be the convolutional feature of the union region of two entities.
<img width="251" alt="image" src="https://user-images.githubusercontent.com/46675408/206344586-7fd852e9-1bb9-4c8b-bbcd-3d71218e2b32.png">

### Bipartite Graph Neural Network
1) Relationship Confidence Estimation Module 
Find the confidence given the class probability of each entity $e_i$, $e_j$.
<img width="288" alt="image" src="https://user-images.githubusercontent.com/46675408/206344837-67e4f864-8843-446a-9851-8b236ff877b1.png">

(???) I don't understand this part, at what point is it global?
<img width="400" alt="image" src="https://user-images.githubusercontent.com/46675408/206345183-ba6c5ef9-b764-4b16-86ed-fe52d0bd086c.png">

2) Confidence-aware message 
<img width="400" alt="image" src="https://user-images.githubusercontent.com/46675408/206345271-ee56e614-186c-4f58-bafb-2977ea0b5f71.png">
- entity-to-predicate
<img width="400" alt="image" src="https://user-images.githubusercontent.com/46675408/206345326-59c2d721-21f0-40ee-af27-54c1f22ba8d3.png">

- predicate-to-entity 
<img width="400" alt="image" src="https://user-images.githubusercontent.com/46675408/206345344-309ebe76-9f06-45ab-b486-92dd3a6c4e81.png">

The $\alpha$, $\beta$ are theshold parameter.

each entity node $e_i$ by aggregating neighbors' messages
<img width="400" alt="image" src="https://user-images.githubusercontent.com/46675408/206345533-20170fdd-2819-4787-ab8b-d0999cca8376.png">

### Scene Graph Prediction
<img width="400" alt="image" src="https://user-images.githubusercontent.com/46675408/206345608-d45cbb45-88e5-478a-9990-018ae83c6174.png">

<img width="400" alt="image" src="https://user-images.githubusercontent.com/46675408/206345626-2005cb27-468f-4ece-9cef-5b79ab3cad01.png">


## Bi-level Resampling
<img width="400" alt="image" src="https://user-images.githubusercontent.com/46675408/206343509-7fb5e45e-59a2-486b-b57c-87bd5e2a79b3.png">

1) image-level over-sampling
Like getting the repeat factor and pulling more images for a class that didn't appear.
$r^c=max(1, \sqrt(t/f^c))$
- $c$ : category
- $f_c$ : frequency of category c on the entire dataset
- $t$ : hyperparam

2) instance-level under-sampling
Like removing instances based on different predicate classes for each image. -> Iterative SGG is one-stage, how did you do this? Did you just remove it from the gt label?

## Result
<img width="800" alt="image" src="https://user-images.githubusercontent.com/46675408/206345678-506e61d6-7a89-4b58-920c-44b114916bcb.png">

<img width="500" alt="image" src="https://user-images.githubusercontent.com/46675408/206345749-5f8d8db4-c11e-4be5-bf13-182bce4d8c77.png">


<img width="413" alt="image" src="https://user-images.githubusercontent.com/46675408/206345692-df31b162-bee5-4f26-9bea-c6ba0004c026.png">
