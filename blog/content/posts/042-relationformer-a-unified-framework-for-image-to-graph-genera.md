---
title: "Relationformer: A Unified Framework for Image-to-Graph Generation"
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
- **problem :** The two-stage image-to-graph generation model is also complex and has a complexity of O(n**2).
- **idea :** Instead of pair-wise interaction of entities (=>O(n**2)), let's use interaction of relation token and entity.
![image](https://user-images.githubusercontent.com/46675408/180105525-fb3f9ebe-f912-441c-814d-843644ff1296.png)
- **architecture :** CNN backbone + deformable DETR(Encoder, Decoder with N + 1(=relation) tokens) + Object Detection Head and Relation Prediction Head.
![image](https://user-images.githubusercontent.com/46675408/180105773-fbd02b9f-55e8-4bbc-828e-b2275e7948b8.png)
- **objective :** bbox loss(gIOU + regression loss) + cross-entropy for entity class + cross-entropy loss for relation to object picked as hungarian.
- **baseline :** two-stage models, FCSGG, #40 
- **data :** Toulouse, 20 US Cities, DeepVesselNet, and Visual Genome.
- **result :** SGG) without the extra features (glove vector of words, knowledge graph), the SOTA
- **contribution :** simple architecture with inductive bias!

## Details
### Parameter 
<img width="866" alt="image" src="https://user-images.githubusercontent.com/46675408/195288348-d76dee53-77f3-4644-bcb8-18106dbebd07.png">

<img width="865" alt="image" src="https://user-images.githubusercontent.com/46675408/195288426-a6651beb-5168-4989-977a-d3540ac307d4.png">

Added log softmax, frequency-bias.

<img width="904" alt="image" src="https://user-images.githubusercontent.com/46675408/195288781-471b27bb-ebeb-444b-b9c0-4156f5544b21.png">


### Relation Prediction Head
pair-wise [obj] token, shared [rln]-token
-> $MLP_{rln}({o^i, r, o^j})_{i!=j}$
- For k objects drawn from object detection, concat the output of the [rln] token for k(k-1) pairs with a 3-layer FCN run to get the relation. -> still $O(n^2)$!
 
MLP -> 3 layer FCN + LN 
In cases like SGG, order determines subject, object

### The authors' claims about `[rln]` tokens
- object has a higher order topology than the object, so it requires additional expressive capacity
- [obj] tokens to reduce the burden of pulling relation
- [obj] tokens engage in global semantic reasoning as [rln] tokens compete for attention with [obj] tokens

### Compared to SGTR,
- No distinction between entity and subject / object -> LOSS for entity only once!
- In SGTR, the image feature was still explicitly put into the model, which is not the case here.

### Loss
#### Stochastic Relation Loss
![image](https://user-images.githubusercontent.com/46675408/180107692-8a0802cc-3dcd-4ade-88d6-9beced8c940c.png)

For the objects matched with gt object by hungarian matcher, we got the cross entropy loss for pair-wise relation.
I have a relation called valid if it exists and background if it doesn't, and since I have a lot of backgrounds, I've made it a 1:3 ratio.

### Ablation
#### [rln] ablation for token with and without
<img width="520" alt="image" src="https://user-images.githubusercontent.com/46675408/195288222-6232b3a3-16c6-4703-9dc2-bc38e35a9fb4.png">


Large performance differences


### Results
![image](https://user-images.githubusercontent.com/46675408/180107082-5cfc8fbf-d581-4080-bc95-c7a446aa4f64.png)

