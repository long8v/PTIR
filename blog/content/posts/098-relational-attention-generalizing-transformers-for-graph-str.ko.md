---
title: "[89] Relational Attention: Generalizing Transformers for Graph-Structured Tasks"
date: 2022-12-15
tags: ['microsoft', 'graph', '2022Q4', 'transformer']
paper: "https://arxiv.org/abs/2210.05062"
issue: 98
issueUrl: "https://github.com/long8v/PTIR/issues/98"
---
![image](https://user-images.githubusercontent.com/46675408/207773112-434689ed-fdc7-46ac-9dad-b7c326a1f088.png)

[paper](https://arxiv.org/abs/2210.05062)

## TL;DR
- **I read this because.. :** 제목이 attention을 통해 relation 뽑겠다는 개념인 것 같고 자기 방법론이 `우아`하다고 해서 읽음
- **task :** Graph representation
- **problem :** transformer로 그래프 표현해보자. 트랜스포머는 그래프와 달리 순서가 없는 set을 input으로 받고 GNN과 달리 relational한 inductive bias가 없다.
- **idea :** edge와 node를 concat해서 Q, K, V로 사용하자
- **architecture :** transformer + edge update for neighbor nodes and edges
- **baseline :** Deep Sets, Graph ATtention network, Message Passing Neural Network, Pointer Graph Networks
- **data :** [CLRS-30](https://github.com/deepmind/clrs) graph로 알고리즘 푸는 벤치마크인 듯하다.
- **result :** SOTA 
- **limitation / things I cannot understand :** 아니 이 접근이 정말 없었나? ㅋㅋ 
## Details
### motivation
![image](https://user-images.githubusercontent.com/46675408/207773154-5cf86777-a956-4d90-bdf9-8dfe7fd4b4dd.png)

transformer는 edge가 없는 graph인 set을 받고 이를 표현하는 모델이라고 생각할 수 있음.
transformer에 edge까지 넣어보자

## Previous work
<img width="905" alt="image" src="https://user-images.githubusercontent.com/46675408/208278936-f70e6867-886d-48a9-8950-0b1c07996d70.png">

https://arxiv.org/pdf/2207.02505.pdf

### Graph Neural Networks
notation 설명. 
- graph G는 node $N$과 edge $\varepsilon$으로 구성됨
  - $N$ : 순서가 없는 node vectors $n_i\in \mathbb{R}^{d_n}$ set으로 구성됨
  - $\varepsilon$ : edge vector $e_{ij}\in\mathbb{R}^{d_e}$ 셋으로 구성됨
- 각 레이어 $l$에서는 그래프 $G^l$을 받고 같은 구조의 $G^{l+1}$을 return.
![image](https://user-images.githubusercontent.com/46675408/207775141-b774c047-8c04-40cd-bf0d-0b0c2d91846d.png)
- $\phi$ : update function
- $\oplus$ : aggregation function 
- $L_i$ : i번째 node의 neighbor들
- 기본적인 GNN은 모든 Edge (i, j)에서 $e_{ij}^{l+1}=e_{ij}^l$임

### Relational Transformer
우아..하면서 간단.. edge node concat해서 qkv projection의 x로 쓰자
![image](https://user-images.githubusercontent.com/46675408/207776464-20f030b7-2c8e-4d09-9e1a-92e6e0904bf9.png)

연산 간단히 하려고 행렬 잘라서 아래와 같이 표현
![image](https://user-images.githubusercontent.com/46675408/207776527-b0ddce7a-2829-4903-8c91-b4b013062c8a.png)

그림으로 표현하면 이렇다.
![image](https://user-images.githubusercontent.com/46675408/207776483-cb536d3a-be79-4b97-a909-5c90dfb662ba.png)

### Edge update 
edge를 모든 node, 모든 edge들에 대해서 업데이트를 하면 복잡도가 $O(n^3)$이 되니 인접한 두개의 노드, 자기 자신, 반대 방향으로 가는 Edge 이렇게 4가지에 대해서만 aggregation해서 message passing을 한다.
![image](https://user-images.githubusercontent.com/46675408/207776556-0c7e8083-3c27-4fce-94ec-3761f40f18e1.png)

![image](https://user-images.githubusercontent.com/46675408/207776773-064bce0f-ba93-4dc1-a467-6b32d97a5dde.png)

![image](https://user-images.githubusercontent.com/46675408/207776795-f98c7e71-d1ac-4fec-9a11-dc3320c68750.png)

