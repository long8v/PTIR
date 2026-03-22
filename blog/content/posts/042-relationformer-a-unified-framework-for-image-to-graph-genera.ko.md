---
title: "[37] Relationformer: A Unified Framework for Image-to-Graph Generation"
date: 2022-07-21
tags: ['2022Q1', 'SGG', 'graph', 'one-stage', 'ECCV']
paper: "https://arxiv.org/pdf/2203.10202.pdf"
issue: 42
issueUrl: "https://github.com/long8v/PTIR/issues/42"
---
![image](https://user-images.githubusercontent.com/46675408/180104715-9562dec8-1dbd-4054-82d9-13802102f774.png)

[paper](https://arxiv.org/pdf/2203.10202.pdf), [code](https://github.com/suprosanna/relationformer)

## TL;DR
- **task :** image-to-graph generation
- **problem :** two-stage image-to-graph generation 모델도 복잡하고 복잡도도 O(n**2).
- **idea :** entity들의 pair-wise interaction(=>O(n**2)) 대신 relation token과 entity의 interaction을 사용하도록 하자.
![image](https://user-images.githubusercontent.com/46675408/180105525-fb3f9ebe-f912-441c-814d-843644ff1296.png)
- **architecture :** CNN backbone + deformable DETR(Encoder, Decoder with N + 1(=relation) tokens) + Object Detection Head and Relation Prediction Head.
![image](https://user-images.githubusercontent.com/46675408/180105773-fbd02b9f-55e8-4bbc-828e-b2275e7948b8.png)
- **objective :** bbox loss(gIOU + regression loss) + cross-entropy for entity class + hungarian으로 뽑힌 object에 대한 relation에 대한 cross-entropy loss.
- **baseline :** two-stage models, FCSGG, #40 
- **data :** Toulouse, 20 US Cities, DeepVesselNet, and Visual Genome.
- **result :** SGG) extra feature(단어의 glove vector, knowledge graph)를 안쓴 것들 중에서는 SOTA
- **contribution :** simple architecture with inductive bias!

## Details
### Parameter 
<img width="866" alt="image" src="https://user-images.githubusercontent.com/46675408/195288348-d76dee53-77f3-4644-bcb8-18106dbebd07.png">

<img width="865" alt="image" src="https://user-images.githubusercontent.com/46675408/195288426-a6651beb-5168-4989-977a-d3540ac307d4.png">

log softmax, frequency-bias 넣어줬음.

<img width="904" alt="image" src="https://user-images.githubusercontent.com/46675408/195288781-471b27bb-ebeb-444b-b9c0-4156f5544b21.png">


### Relation Prediction Head
pair-wise [obj] token, shared [rln]-token
-> $MLP_{rln}({o^i, r, o^j})_{i!=j}$
-  object detection에서 뽑은 k개의 object에 대해 k(k-1)개의 pair에 대해 [rln] 토큰의 output을 3-layer FCN 돌린거랑 concat해서 relation 뽑음. -> 여전히 $O(n^2)$임!
 
MLP -> 3 layer FCN + LN 
SGG 같은 경우엔 order가 subject, object를 결정함 

### `[rln]` 토큰들에 대한 저자들의 주장
- object에 비해 higher order topological를 가지고 있어서 expressive capacity가 추가적으로 필요하다 
- [obj] 토큰들이 relation까지 뽑아야하는 burden을 줄인다
- [obj] 토큰들이 [rln]토큰들과 attention이 걸리면서 global semantic reasoning을 한다

### SGTR과 비교했을 때,
- entity와 subject / object 가 구분되지 않음 -> entity에 대한 loss는 한번만!
- SGTR에서는 image feature를 계속 명시적으로 모델에게 넣어줬는데 여기는 그러지 않음.

### Loss
#### Stochastic Relation Loss
![image](https://user-images.githubusercontent.com/46675408/180107692-8a0802cc-3dcd-4ade-88d6-9beced8c940c.png)

hungarian matcher에 의해 gt object와 매칭된 object들에 대해서 pair-wise relation에 대해 cross entropy loss를 구했다. 
relation이 있으면 valid, 없으면 background라는 relation을 두었는데 background가 많으므로 1:3 비율로 맞췄다.

### Ablation
#### [rln] 토큰 있고 없고에 대한 ablation
<img width="520" alt="image" src="https://user-images.githubusercontent.com/46675408/195288222-6232b3a3-16c6-4703-9dc2-bc38e35a9fb4.png">


성능 차이가 많이 난다


### Results
![image](https://user-images.githubusercontent.com/46675408/180107082-5cfc8fbf-d581-4080-bc95-c7a446aa4f64.png)

