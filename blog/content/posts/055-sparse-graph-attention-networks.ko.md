---
title: "[49] Sparse Graph Attention Networks"
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
- **problem :** Graph를 표현하기 위해 attention을 사용하는 GAT(Graph Attention Network) 모델들이 있지만, 실제 그래프는 매우 크고 noisy하기 때문에 일반화되기 어렵다.  
- **idea :** 어떤 edge가 중요한지를 선택하는 attention score를 모든 레이어에서 하나만 선택하고 나머지는 다 0으로 두자.
- **architecture :** GAT인데 attention score를 한개만 선택함.
- **objective :** cross entropy loss와 edge의 개수에 대한 loss
- **baseline :** GCN, GAT, GraphSage
- **data :** Cora, Citesser, Pubmed, Amazon computer, Amazon Photo, PPI, Reddit
- **result :** GAT와 유사한 성능. layer 별로 하나만 선택되기 때문에 더 해석 가능함.
- **contribution :** 최초로 spare한 GNN이 그렇지 않은 GNN만큼의 성능이 나온다는 것을 보임
- **limitation or 이해 안되는 부분 :** GNN이 transductive 하다는데 이해를 확실히 못함. $z_{ij}$는 어떻게 학습이 되는건지?

## Details
### GNN in general
- $G$ = ( $V$, $E$ ) 그래프는 node( $V$ )와 edge ( $E$ )로 구성
- node들은 feature $X$로 표현됨. 차원은 $N$(노드 개수) x $D$(feature 차원)
- adjacency matrix $A$는 edge로 연결되어 있으면 1, 아니면 0인 matrix임. 차원은 $N$x$N$ 
우리 결국 하고자 하는 것은 feature $X$와 $A$를 받고 강화된 node 표현 $H$를 만드는 것이다. 이때 함수는 보통 이렇게 정의된다.
<img width="250" alt="image" src="https://user-images.githubusercontent.com/46675408/183783907-2a8facf7-e3ac-4453-a2b7-9ddb87e70037.png">

- $f$는 그래프를 인코딩 하는 함수다. 
- 여기서 loss는 node 분류 태스크와 같은 걸 한다면 cross entropy loss가 걸리게 된다
- 결국 GNN의 다양한 variants들은 $f$를 어떻게 구성할까?가 문제다.

### Neighbor Aggregation Methods
graph learning을 할 때 가장 효율적인 방법 중 하나가 neighbor aggregation mechanism인데, feature vector $x_i$와 그 neighbor인 j들에 대해서 feature vector를 aggregate하는 것이다. 
가령 Graph Convolution Network(GCN)도 그 종류들 중 하난데, 식을 아래와 같이 쓸 수 있다.
<img width="250" alt="image" src="https://user-images.githubusercontent.com/46675408/183783929-73c5578e-cb51-4e9c-88ac-7b973db5f9ae.png">
<img width="250" alt="image" src="https://user-images.githubusercontent.com/46675408/183783978-23eac389-deb1-4316-84d4-181af489879f.png">

이걸 조금 더 general 하게 쓰면 아래와 같이 쓸 수 있다.
<img width="250" alt="image" src="https://user-images.githubusercontent.com/46675408/183783810-f8576754-babe-4df3-9d97-7a9fad3220a7.png">

하지만 GCN은 transductive 하게 밖에 못쓰는데, 그래프 구조가 바뀌면 새로 학습을 해줘야한다. 

### Graph Attention Networks(GAT)
GCN과 유사하게 neighborhood를 aggregate하는데, attention 을 사용해서 어떤 ege에 집중할지를 attention score를 구하게 되면 GAT가 된다.
<img width="250" alt="image" src="https://user-images.githubusercontent.com/46675408/183784095-284bff2d-f486-47f5-bb71-0b940bc276bb.png">

그런데 이 경우에, attention score를 각 edge별 중요도라고 볼 수 있는데 layer마다 attention score가 달라지기 때문에 해석은 어렵다. 
그래프를 만들 때 noisy/task-irrevalent한 edge들을 정리하기 위해 SGAT를 제안한다!

### SparseGAT(SGAT)
중요한 edge만 남기기 위해서 binary gate $z_{ij}$를 각 ege 별로 추가한다. 이 $z_{ij}$는 edge $e_{ij}$를 사용할지 말지에 대한 bianry masking을 하게 된다. 
<img width="250" alt="image" src="https://user-images.githubusercontent.com/46675408/183784225-7c9dc9be-b704-45df-8920-9757df91cd6b.png">

최대한 적은 edge를 남기기 위해 loss term에 L0 loss를 추가한다. $z_{ij}$ 가 1이면 1 아니면 0인걸 sum하는 term이다.(edge 개수에 대한 loss)
<img width="400" alt="image" src="https://user-images.githubusercontent.com/46675408/183784260-052aec62-9536-426e-add4-06b1e29cad6e.png">

attention based aggregation function은 아래와 같이 쓸 수 있는데 (GAT)와 다른 게 없음
<img width="250" alt="image" src="https://user-images.githubusercontent.com/46675408/183784276-b0fe0aae-f1d9-481e-ab9f-056299e048ee.png">

이때 attention score를 아래와 같이 구한다.
<img width="300" alt="image" src="https://user-images.githubusercontent.com/46675408/183784920-67941571-e9c7-4053-9296-9a8f731c2bda.png">

-> $z_{ij}$는 어떻게 학습이 되는건지?

이렇게 sparse 하게 구성하게 된 시작은 attention score에 대한 head별 layer 별 분산을 구해봤는데 아래와 같이 거의 0에 가까웠기 때문임.
<img width="250" alt="image" src="https://user-images.githubusercontent.com/46675408/183785088-26b0760f-25f9-4eca-80db-3118d5fbc495.png">


