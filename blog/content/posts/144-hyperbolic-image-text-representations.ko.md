---
title: "[132] Hyperbolic Image-Text Representations"
date: 2023-09-26
tags: ['ICML', 'CLIP', '2023Q2', 'meta']
paper: "https://arxiv.org/abs/2304.09172"
issue: 144
issueUrl: "https://github.com/long8v/PTIR/issues/144"
---
<img width="715" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/a9219b68-f1ad-4ad7-bf87-d4521f817143">

[paper](https://arxiv.org/abs/2304.09172), [code](https://github.com/facebookresearch/meru)

## TL;DR
- **I read this because.. :** 언급되어. 한 이미지를 표현하는 텍스트가 여러개가 될 수 있음. 이에 대한 ambiguity?!(송강호, 남자 배우, 남자)
- **task :** contrastive learning 
- **problem :** 한 이미지에 대해 텍스트가 표현할 때 다양한 층위에서 표현될 수 있음(`개가 눈 위에 서 있다`, `강아지`, `ㄱㅇㅇ~`)
- **idea :** CLIP의 임베딩 공간을 euclidean 공간이 아니라 hyperbolic 공간으로 옮기자
- **input/output :** image/text -> score
- **architecture :** CLIP과 같음
- **objective :** contrastive + entailment loss 
- **baseline :** CLIP trained with YFCC-100M(by SLIP)
- **data :** YFCC-100M
- **evaluation :** image text retrieval, zs-image classification
- **result :** 개선된 성능. 특정 이미지에서 [ROOT]에 대해 traverse 하면서 나오는 text가 점점 generic해진걸 보임.
- **contribution :** 아마 CLIP을 hyperbolic space에서 한 첫 work?
- **etc. :**

## Details
### Motivation 
<img width="408" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/dbf3ae16-51f5-4e87-bd9f-9d8d76635547">


### Arch
<img width="388" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/f935c80e-67c5-4932-876d-72f5b9a642f6">


### Lifting embeddings onto the hyperboloid
CLIP encoder를 통과하면 각각의 이미지, 텍스트 벡터는 n차원의 벡터로 나오고 여기에 origin 0벡터를 추가하는 transformation을 적용
$v =[v_{enc}, 0]\in\mathbb{R}^{n+1}$ 이 origin O의 tangent space에 들어가게 되고, 이러면 0과 내적하면 0이되는 조건을 충족하게 된다.
Lorents 모델의 space 공간에 대해서만 계산하게 되면 된다. 
그럴 경우에 x 벡터에 대한 exponential map(tangent space -> manifold로 투영하는 map vectors)은 아래와 같이 정리된다.
<img width="315" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/7c3d4554-2428-4b6f-a9d2-450fed946a75">

<img width="234" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/0db991b1-075e-4a9c-b26e-9479f92ededd">

즉 CLIP encoder에서 나온 임베딩에다가 저 transformation을 적용하면 hyperbolic space로 가게 된다.

Lorents inner product는 아래와 같으므로 내적을 통해 similiarity를 구하고 contrastive loss를 추가하면 된다
<img width="259" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/08d5c01a-a940-45b3-9a06-ba4fb29ed122">


### Entailment loss
<img width="338" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/c484e682-93c8-46ec-9502-5ca4a473fe44">

아래와 같은 loss를 contrastive loss에 추가해줌
수학적 이해는 잘 모르겠고 이 loss를 추가하는 직관은 {Text-image}페어가 있을 때 text가 image를 entail 해야 함. 
<img width="227" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/9b96acb0-23a7-41b9-9166-787401312beb">

<img width="344" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b8c08755-2b08-46ad-b01b-1609426eca71">

## Results
<img width="827" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/d48d9d71-091b-484c-8aa3-ac49ada63eb3">

<img width="409" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/8c16b0b2-08cc-4e29-b609-1437d5e5b94a">

- 텍스트가 좀 더 generic 하고 널리 분포되어 있음
- 둘의 공간이 아예 분리 되어 있음

### Ablations
<img width="411" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/4bf0110a-5b2f-4f72-aafc-ece205095737">
<img width="402" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/313e6e78-1535-47bc-ac98-cb8c1475f2a9">


### Image Traverse
<img width="830" alt="image" src="https://github.com/long8v/PTIR/assets/46675408/b07c7eee-cf0d-4b75-90fb-9d929cc78564">
