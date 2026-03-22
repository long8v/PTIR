---
title: "[87] Bipartite Graph Network with Adaptive Message Passing for Unbiased Scene Graph Generation"
date: 2022-12-08
tags: ['2021Q4', 'CVPR', 'SGG', 'imbalance']
paper: "https://arxiv.org/abs/2104.00308"
issue: 96
issueUrl: "https://github.com/long8v/PTIR/issues/96"
---
<img width="902" alt="image" src="https://user-images.githubusercontent.com/46675408/206342606-3fa8f4b6-67a0-4452-a60e-0d49d0b6695d.png">

[paper](https://arxiv.org/abs/2104.00308)

## TL;DR
- **I read this because.. :** #75 에서 성능 향상이 꽤 있었음. 최근 AAAI에 나온 논문 중에 baseline이 해당 논문인게 있었음.
- **task :** two-stage SGG
- **problem :** sgg 데이터가 long-tail.
- **idea :** confidence-aware bipartite graph neural network 제안. bi-level data resampling strategy.
- **architecture :** relationship confidence estimation(RCE)와 confidence-aware message propagation(CMP)의 조합
- **objective :** predicate와 entity의 ce loss, loss for relation confidence estimation(class-specific / overall)
- **baseline :** graph-RCNN, GPS-Net, Motif, ...
- **data :** Visual Genome, Open Images V4/6
- **evaluation :** PredCls, SGCls, SGGen(head, body, tail), OI evaluation 
- **result :** sota. tail 점수가 많이 좋아짐. 
- **contribution :** confidence aware? gnn for sgg 논문들을 잘 몰라서 뭐가 contribution인지 모르겠음
- **limitation / things I cannot understand :** confidence가 무슨 역할을 하는지? confidence에 loss를 직접적으로 준 것 같은데 어떻게 준건지? graph-RCNN에서 "relatedness" 준 것 처럼 준건가? 

# Details
## Architecture
<img width="899" alt="image" src="https://user-images.githubusercontent.com/46675408/206344201-b0d99065-3dd0-4007-8b61-f369caff6abf.png">

### Proposal generation network
Faster RCNN으로 object들 뽑고 거기서 visual feature $v_i$, geometric feature $g_i$, class word embedding feature $w_i$를 가지고 entity 표현 $e_i$를 만듦
<img width="200" alt="image" src="https://user-images.githubusercontent.com/46675408/206344577-8dc6d4be-6509-4c6d-813f-9a2313136d15.png">

relation representation $r_{i->j}$는 entity 표현 $e_i$, $e_j$를 결함해서 만듦. $u_i,j$는 두 entity의 union region의 convolutional feature.
<img width="251" alt="image" src="https://user-images.githubusercontent.com/46675408/206344586-7fd852e9-1bb9-4c8b-bbcd-3d71218e2b32.png">

### Bipartite Graph Neural Network
1) Relationship Confidence Estimation Module 
각 entity $e_i$, $e_j$의 class probability를 가지고 confidence를 구함.
<img width="288" alt="image" src="https://user-images.githubusercontent.com/46675408/206344837-67e4f864-8843-446a-9851-8b236ff877b1.png">

(???) 이부분 이해가 안됨 어느 점에서 global인지?
<img width="400" alt="image" src="https://user-images.githubusercontent.com/46675408/206345183-ba6c5ef9-b764-4b16-86ed-fe52d0bd086c.png">

2) Confidence-aware message 
<img width="400" alt="image" src="https://user-images.githubusercontent.com/46675408/206345271-ee56e614-186c-4f58-bafb-2977ea0b5f71.png">
- entity-to-predicate
<img width="400" alt="image" src="https://user-images.githubusercontent.com/46675408/206345326-59c2d721-21f0-40ee-af27-54c1f22ba8d3.png">

- predicate-to-entity 
<img width="400" alt="image" src="https://user-images.githubusercontent.com/46675408/206345344-309ebe76-9f06-45ab-b486-92dd3a6c4e81.png">

$\alpha$, $\beta$는 theshold parameter. 

each entity node $e_i$ by aggregating neighbors' messages
<img width="400" alt="image" src="https://user-images.githubusercontent.com/46675408/206345533-20170fdd-2819-4787-ab8b-d0999cca8376.png">

### Scene Graph Prediction
<img width="400" alt="image" src="https://user-images.githubusercontent.com/46675408/206345608-d45cbb45-88e5-478a-9990-018ae83c6174.png">

<img width="400" alt="image" src="https://user-images.githubusercontent.com/46675408/206345626-2005cb27-468f-4ece-9cef-5b79ab3cad01.png">


## Bi-level Resampling
<img width="400" alt="image" src="https://user-images.githubusercontent.com/46675408/206343509-7fb5e45e-59a2-486b-b57c-87bd5e2a79b3.png">

1) image-level over-sampling
repeat factor를 구해서 안나온 class에 대한 이미지가 들어있으면 그 이미지 더 많이 뽑은듯.
$r^c=max(1, \sqrt(t/f^c))$
- $c$ : category
- $f_c$ : frequency of category c on the entire dataset
- $t$ : hyperparam

2) instance-level under-sampling
각 이미지의 다른 predicate class에 따라 instance를 없앤듯. -> Iterative SGG는 one-stage인데 이거 어떻게 했지? gt label에서 그냥 지운건가 

## Result
<img width="800" alt="image" src="https://user-images.githubusercontent.com/46675408/206345678-506e61d6-7a89-4b58-920c-44b114916bcb.png">

<img width="500" alt="image" src="https://user-images.githubusercontent.com/46675408/206345749-5f8d8db4-c11e-4be5-bf13-182bce4d8c77.png">


<img width="413" alt="image" src="https://user-images.githubusercontent.com/46675408/206345692-df31b162-bee5-4f26-9bea-c6ba0004c026.png">
