---
title: "[86] Graph R-CNN for Scene Graph Generation"
date: 2022-12-06
tags: ['2018', 'SGG', 'graph', 'two-stage']
paper: "https://arxiv.org/pdf/1808.00191.pdf"
issue: 95
issueUrl: "https://github.com/long8v/PTIR/issues/95"
---
<img width="1056" alt="image" src="https://user-images.githubusercontent.com/46675408/205799708-bcd96d1e-3ed7-4f90-bc14-f2dd79973af6.png">

[paper](https://arxiv.org/pdf/1808.00191.pdf)

## TL;DR
- **I read this because.. :** sgg 초기 논문
- **task :** Scene Graph Generation
- **problem :** object 뽑고 quadratic한 relation을 잘 다뤄보자. 강화된 그래프 표현을 만들어보자.
- **idea :** object 간의 relation을 pruning하는 모듈을 중간에 넣자. attentional GCN을 적용하자.
- **architecture :** 1) Faster RCNN으로 Object 뽑고 2) object cls logit 값들 concat해서 relation pruning 3) attentional GCN을 적용해서 object, relation 노드의 표현을 강화 -> 각 subject, object, relation 표현에 classifier 붙여서 예측한듯? 
- **objective :** 1) bbox loss + cls loss 2) bce for relationship score 3) ce for object cls and predicate cls
- **baseline :** IMP, MSDN, NeuralMotif
- **data :** Visual Genome
- **evaluation :** PredCls, PhrCls, SGGen, SGGen+(proposed in this paper)
- **result :** SOTA
- **contribution :** 아마 GCN을 적용한 최초의 논문이 아닐런지?
- **limitation / things I cannot understand :** SGG은 정말 GCN을 쓸 정도로 graph 적인 특성을 가지고 있는가?

## Details
### Architecture
<img width="726" alt="image" src="https://user-images.githubusercontent.com/46675408/205802104-66ce1c38-3030-47bf-87d1-cfdddd0f6020.png">

<img width="705" alt="image" src="https://user-images.githubusercontent.com/46675408/205802166-8aa08cd2-9f4b-45e9-acf8-e74dc42ce967.png">

<img width="511" alt="image" src="https://user-images.githubusercontent.com/46675408/205802198-6ba1f40c-bf06-4bfc-82d7-f7ffac9a239b.png">

3단계로 나눔
1) Object Region Proposal : image가 주어졌을 때 node(=vertex, V)들 뽑기 => Faster RCNN
2) Relationship Proposal : image와 node가 주어졌을 때 모든 경우의 수 n*(n-1)에서 있을만한 relation pruning
3) Graph Labeling : image, node, edge가 주어졌을 때 relation과 object 찾기

### Relation Proposal Network
object의 class logit을 사용하여 "relatedness"를 측정.
일종의 soft한 prior를 주는 형식(가령, `person-ride-chicken`은 될 수 없으니?)
<img width="340" alt="image" src="https://user-images.githubusercontent.com/46675408/205803827-2ff062c8-64cc-4c67-bc69-6fda5590f5ea.png">

구현은 cat한 뒤에 MLP 쌓음.
score를 매겨서 sorting을 한 뒤에 K개의 pair를 뽑음. Faster RCNN이기 때문에 많이 나올거라서 pair에 대한 NMS를 해서 top m개의 pair만 남김
<img width="393" alt="image" src="https://user-images.githubusercontent.com/46675408/205804138-8bc7d66c-d60a-46ad-9998-63ffa774bd71.png">

### Attentional GCN
Vanilla GCN은 아래와 같음
<img width="365" alt="image" src="https://user-images.githubusercontent.com/46675408/205804181-63170107-bbd5-48fa-922a-8cad9ef9120c.png">

- $z_i$ : i번째 node의 표현
- $N(i)$ : i번째 node의 neighbor들
- $\alpha_{ij}$ : i와 j의 adjacency matrix에 의해 만들어지는 connection coefficient

이를 $Z\in \mathbb{R}^{d\times T_n}$라는 matrix로 표현하면 
<img width="248" alt="image" src="https://user-images.githubusercontent.com/46675408/205804619-62933a91-375b-4396-985c-05c4e291a544.png">

우리는 여기서 $\alpha_{ij}$를 주어지는게 아니라 학습하려고 함
<img width="260" alt="image" src="https://user-images.githubusercontent.com/46675408/205804674-d6e1303b-03c1-420d-bf8a-28f9d25b819b.png">

2 layer MLP + softmax로 $\alpha_{ij}$가 학습

#### aGCN for SGG
N개의 Object region들과 m개의 relationship을 각각 node로 만들고 위의 네트워크에서 나온걸로 edge들을 연결해줌. 추가적으로 object간에는 direct edge들을 추가해줌. 

object node에 대한 표현은 아래와 같음
<img width="493" alt="image" src="https://user-images.githubusercontent.com/46675408/205804918-14e93b1b-2a12-45f3-b5d7-b2058f1dc136.png">

relation node에 대한 표현은 아래와 같음. 
<img width="397" alt="image" src="https://user-images.githubusercontent.com/46675408/205804933-44f7458f-587d-4ac1-b826-38b1b3aeace0.png">

### Result
<img width="731" alt="image" src="https://user-images.githubusercontent.com/46675408/205805119-4eaacf85-68a4-4d93-bee1-335b09239545.png">

<img width="726" alt="image" src="https://user-images.githubusercontent.com/46675408/205805243-b5d40574-f5eb-4fc0-9ef3-528e95dd642d.png">

### Ablation for modules
<img width="719" alt="image" src="https://user-images.githubusercontent.com/46675408/205805201-87bba58c-ced2-4c3b-8b20-eb9aee139674.png">

![image](https://user-images.githubusercontent.com/46675408/205806346-985a43a7-780b-48d3-b8d4-0ef1d1c6c0ee.png)

